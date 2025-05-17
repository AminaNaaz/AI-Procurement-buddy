import re
from agents.supplier_agent import search_suppliers, parse_requested_number
from agents.email_agent import draft_email
from utils.error import AgentRoutingError
from utils.logger import logger

from langchain.chat_models import ChatOpenAI


def get_llm(openai_api_key: str):
    # Instantiate LLM with provided API key
    return ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=openai_api_key)


def route_query(full_prompt: str, openai_key: str, serper_key: str = None) -> str:
    """
    Routes user prompt to either supplier discovery or email drafting
    based on inferred intent using the LLM.
    """
    try:
        llm = get_llm(openai_key)

        system_prompt = (
            "You are a smart procurement assistant. "
            "Decide the intent of the following query:\n\n"
            f"{full_prompt}\n\n"
            "Respond with one of: SUPPLIER_DISCOVERY or EMAIL_DRAFTING."
        )
        intent = llm.invoke(system_prompt).content.strip().upper()

        if "SUPPLIER_DISCOVERY" in intent:
            return handle_supplier_discovery(full_prompt, serper_key=serper_key)
        elif "EMAIL_DRAFTING" in intent:
            return handle_email_drafting(full_prompt, llm)
        else:
            raise AgentRoutingError(f"Could not determine intent: {intent}")

    except Exception as e:
        logger.error(f"[Router] Routing failed: {e}")
        raise


def handle_supplier_discovery(user_prompt: str, serper_key: str = None) -> str:
    """
    Handles supplier discovery requests by:
    - Extracting the number of suppliers requested
    - Calling the supplier search agent with Serper key if needed
    - Formatting the response
    """
    try:
        max_results = parse_requested_number(user_prompt)
        suppliers = search_suppliers(user_prompt, max_results=max_results, serper_api_key=serper_key)

        if not suppliers:
            return "No valid suppliers found."

        return "\n\n".join([
            f"""**Supplier {i+1}**
- Name: {s['supplier_name']}
- Email: {s['email'] or 'Not found'}
- Phone: {s['phone'] or 'Not found'}
- Address: {s['address'] or 'Not found'}
- Website: {s['website'] or 'Not found'}"""
            for i, s in enumerate(suppliers)
        ])
    except Exception as e:
        logger.error(f"[Router] Supplier discovery failed: {e}")
        return f"Supplier discovery failed: {str(e)}"


def handle_email_drafting(user_prompt: str, llm) -> str:
    """
    Handles drafting of email by:
    - Extracting supplier email
    - Sending the request to the email drafting agent with the llm instance
    """
    try:
        email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+", user_prompt)
        if not email_match:
            raise AgentRoutingError("No valid email found in query.")

        supplier_email = email_match.group(0)
        product_details = user_prompt.replace(supplier_email, "").strip()

        # Pass the llm instance to draft_email so it uses the correct client
        return draft_email(supplier_email, product_details, llm)

    except Exception as e:
        logger.error(f"[Router] Email drafting failed: {e}")
        return f"Email drafting failed: {str(e)}"
