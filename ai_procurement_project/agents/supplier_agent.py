from ai_procurement_project.config import llm, serper_api_key as global_serper_api_key
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import time
from langchain.schema import HumanMessage


EXCLUDE_DOMAINS = [
    "yellowpages", "justdial", "manta", "tradeindia", "yelp", "facebook", "linkedin",
    "mapquest", "crunchbase", "tripadvisor", "indeed", "zoominfo", "glassdoor",
    "atninfo", "dubai.ae", "fepy.com", "reachuae.com"
]


class SupplierDiscoveryError(Exception):
    pass


def parse_requested_number(prompt: str, default: int = 3) -> int:
    number_words = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
    }
    digit_match = re.search(r"\b(\d+)\b", prompt)
    if digit_match:
        return int(digit_match.group(1))
    for word, num in number_words.items():
        if word in prompt.lower():
            return num
    return default


def extract_from_text(text):
    # Extract emails
    email_matches = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    email = next((e for e in email_matches if not e.endswith("@gmail.com") and not e.endswith("@yahoo.com")), None)

    # Phone extraction - priority to international numbers starting with +
    raw_numbers = re.findall(r"(?:call(?: us)?|phone|tel(?:ephone)?)[\s:]*([+]*\d[\d\s\-().]{6,})", text, re.I)
    raw_numbers += re.findall(r"(?<!\w)(\+[\d\s\-().]{7,})(?!\w)", text)  # Add standalone +number patterns

    cleaned_numbers = []
    for num in raw_numbers:
        cleaned = re.sub(r"[^\d+]", "", num)
        if len(cleaned) >= 7:
            cleaned_numbers.append(cleaned)

    # Prioritize numbers starting with "+"
    prioritized = next((n for n in cleaned_numbers if n.startswith("+")), None)
    fallback = next(iter(cleaned_numbers), None)

    return {
        "email": email,
        "phone": prioritized or fallback
    }


def clean_supplier_name(title):
    # Remove phrases like "Contact Us", "Contact", "Home" etc.
    cleaned = re.sub(r"(Contact\s*Us|Contact|Home|Page|Official Site|Homepage|\|.*$)", "", title, flags=re.I).strip()
    # Limit length
    return cleaned if cleaned else "Unknown"


def extract_address_with_llm(full_text, location_hint=None):
    prompt = (
        "Extract the full postal address from the following text. "
        "If a location or city is specified, only return the address matching that location. "
        "Return only the address, no extra explanation.\n\n"
        f"Location hint: {location_hint or 'None'}\n\n"
        f"Text:\n{full_text}\n\nAddress:"
    )
    response = llm.generate([[HumanMessage(content=prompt)]])
    address = response.generations[0][0].text.strip()

    if len(address) < 10 or "http" in address.lower():
        return None
    return address


def extract_supplier_info(html_content, base_url=None, location_hint=None):
    soup = BeautifulSoup(html_content, "html.parser")
    # Clean title to get supplier name
    supplier_name = clean_supplier_name(soup.title.string if soup.title else "Unknown")

    contact_info = {
        "supplier_name": supplier_name,
        "email": None,
        "phone": None,
        "address": None,
        "website": base_url
    }

    # Extract email and phone from main page text
    text = soup.get_text(separator=" ", strip=True)
    contact_info.update({k: v for k, v in extract_from_text(text).items() if v})

    # Find contact page link (with "contact" in href or text)
    contact_link = soup.find("a", href=True, string=re.compile(r"contact", re.I))
    if contact_link and base_url:
        contact_url = urljoin(base_url, contact_link["href"])
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(contact_url, headers=headers, timeout=10)
            response.raise_for_status()

            contact_soup = BeautifulSoup(response.text, "html.parser")
            contact_text = contact_soup.get_text(separator=" ", strip=True)

            # Extract email and phone from contact page text (overwrite if found)
            contact_info.update({k: v for k, v in extract_from_text(contact_text).items() if v})

            # Use LLM to extract address from contact page text only
            address = extract_address_with_llm(contact_text, location_hint)
            if address:
                contact_info["address"] = address

        except Exception as e:
            print(f"[Info] Failed to follow contact page {contact_url}: {e}")

    # If no contact page or address not found yet, try LLM on main page text
    if not contact_info["address"]:
        address = extract_address_with_llm(text, location_hint)
        if address:
            contact_info["address"] = address

    return contact_info


def get_supplier_urls_with_serper(query, max_results=10, serper_api_key=None):
    if serper_api_key is None:
        serper_api_key = global_serper_api_key

    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": serper_api_key}
    params = {"q": query, "num": max_results}

    response = requests.get(url, headers=headers, params=params, timeout=10)
    if response.status_code != 200:
        raise SupplierDiscoveryError(f"Serper API failed: {response.status_code} - {response.text}")

    data = response.json()
    urls = []
    for result in data.get("organic", []):
        link = result.get("link")
        if link and not any(domain in link for domain in EXCLUDE_DOMAINS):
            urls.append(link)
        if len(urls) >= max_results:
            break

    return urls


def search_suppliers(prompt: str, max_results: int = None, max_retries=3, serper_api_key=None):
    try:
        if serper_api_key is None:
            serper_api_key = global_serper_api_key

        if max_results is None:
            max_results = parse_requested_number(prompt, default=3)

        # Extract location hint dynamically from prompt (naive approach, improve as needed)
        location_hint_match = re.search(r"in\s+([a-zA-Z\s]+)", prompt, re.I)
        location_hint = location_hint_match.group(1).strip() if location_hint_match else None

        enhanced_query = f"{prompt} supplier manufacturer distributor official contact email phone"
        supplier_urls = get_supplier_urls_with_serper(enhanced_query, max_results=max_results * 5, serper_api_key=serper_api_key)

        results = []
        headers = {"User-Agent": "Mozilla/5.0"}

        attempt = 0
        while attempt < max_retries and len(results) < max_results:
            for url in supplier_urls:
                if len(results) >= max_results:
                    break
                try:
                    response = requests.get(url, headers=headers, timeout=10)
                    response.raise_for_status()

                    contact = extract_supplier_info(response.text, base_url=url, location_hint=location_hint)

                    # Only add if email or phone found
                    if contact["website"] and (contact["email"] or contact["phone"]):
                        # Avoid duplicates by website URL
                        if not any(r["website"] == contact["website"] for r in results):
                            results.append(contact)

                except Exception as e:
                    print(f"[Warning] Failed to scrape {url}: {e}")
                    continue

            if len(results) < max_results:
                print(f"[Info] Retry {attempt+1}: Found {len(results)} suppliers, retrying...")
                attempt += 1
                time.sleep(2)  # Wait a bit before retry

        if not results:
            raise SupplierDiscoveryError("No valid suppliers found with contact details.")

        return results[:max_results]

    except Exception as e:
        raise SupplierDiscoveryError(f"Supplier discovery failed: {str(e)}")
