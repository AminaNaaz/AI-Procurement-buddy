# AI-Procurement-Buddy

**AI-Procurement-Buddy** is an intelligent AI assistant designed to automate procurement workflows by discovering suppliers, extracting contact details, and drafting quotation emails. Built with Python, Streamlit, LangChain, and LangGraph (optional), this tool streamlines procurement processes leveraging large language models and web scraping techniques.

---

## Features

- **Supplier Discovery:** Search for relevant suppliers based on user queries using Serper API and web scraping.
- **Contact Extraction:** Extract supplier emails, phone numbers, and addresses using regex and LLM-enhanced parsing.
- **Quotation Email Drafting:** Generate professional procurement emails using large language models.
- **Multi-Workflow Agent:** Route user queries intelligently between supplier discovery and email drafting.
- **Streamlit UI:** Simple and interactive web interface for easy use.
- **Extensible:** Optionally integrate LangGraph for orchestrating AI workflows as graphs.

---

## Tech Stack

- Python 3.9+
- Streamlit (for UI)
- LangChain (LLM orchestration)
- LangGraph (optional, for workflow orchestration)
- BeautifulSoup4 (web scraping)
- Requests (HTTP calls)
- Serper API (Google search API alternative)
- OpenAI GPT-4 (LLM backend)

---

## Getting Started

### Prerequisites

- Python 3.9 or higher
- [Serper API Key](https://serper.dev/)
- OpenAI API Key

### Installation

1. **Clone the repo**

git clone https://github.com/AminaNaaz/AI-Procurement-buddy.git
cd AI-Procurement-buddy
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
