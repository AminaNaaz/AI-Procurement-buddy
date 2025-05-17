# AI-Procurement-Buddy

Welcome to **AI-Procurement-Buddy** — your intelligent AI assistant designed to revolutionize procurement workflows. This project leverages powerful language models, advanced web scraping, and smart workflow orchestration to automate supplier discovery, extract reliable contact information, and generate professional procurement emails — all within an easy-to-use Streamlit interface.

---

## Why AI-Procurement-Buddy?

Procurement teams often face time-consuming tasks such as searching for suppliers, gathering accurate contact details, and crafting formal communication. This assistant simplifies those steps by:

- **Automating supplier discovery** via smart search queries powered by Serper API and advanced filtering to avoid low-quality directories.
- **Extracting accurate contact info** like emails, international phone numbers, and postal addresses using a combination of regex and LLM-powered parsing.
- **Drafting professional quotation emails** tailored to user needs with minimal input.
- **Routing user queries dynamically** between discovery and email drafting workflows to save time and reduce manual effort.
- Providing a **modern, responsive UI** using Streamlit, accessible to non-technical users.
- Optionally supporting **LangGraph** for orchestrating complex AI workflows as modular graphs — making the system highly extensible.

---

## Key Features

| Feature                     | Description                                                                                       |
|-----------------------------|---------------------------------------------------------------------------------------------------|
| Supplier Discovery           | Find suppliers, manufacturers, or distributors by leveraging Google-like search with Serper API.  |
| Contact Information Extraction | Parse and validate emails, international phone numbers, and postal addresses from websites.       |
| Quotation Email Drafting     | Generate clear, professional procurement emails with context-aware prompts.                      |
| Intelligent Query Routing    | Use a routing agent to direct queries to the appropriate workflow automatically.                  |
| Streamlit UI                | Interactive and user-friendly front end to interact with the AI assistant.                         |
| LangGraph Workflow (Optional) | Modular workflow orchestration enabling complex multi-step AI processes.                        |

---

## Technologies Used

- **Python 3.9+**: Core programming language.
- **Streamlit**: For building the interactive UI.
- **LangChain**: To orchestrate calls to large language models.
- **LangGraph (Optional)**: For defining and managing AI workflows as graphs.
- **BeautifulSoup4**: HTML parsing for web scraping.
- **Requests**: HTTP client for making web requests.
- **Serper API**: Google Search API alternative for supplier search.
- **OpenAI GPT-4**: Large Language Model powering text generation and parsing.

---

## Getting Started

### Prerequisites

- Python 3.9 or later installed.
- API keys from:
  - [OpenAI](https://platform.openai.com/)
  - [Serper API](https://serper.dev/)

ai_procurement_project/
├── agents/
│   ├── supplier_agent.py       # Supplier search & contact extraction logic
│   ├── email_agent.py          # Quotation email drafting workflows
│   └── router_agent.py         # Routes user queries to correct workflow
├── config.py                  # Configuration and API keys management
├── langgraph_workflow.py      # (Optional) LangGraph workflow definitions
├── main.py                    # Main orchestrator logic
├── utils.py                   # Helper utility functions
streamlit_app.py              # Streamlit app entrypoint and UI
requirements.txt              # List of Python dependencies
secrets.toml                 # API keys (excluded from git)
README.md                    # This document

# Troubleshooting & Tips
Dependency issues: If you encounter errors installing packages like Pillow, try installing OS-level build tools or pin the package version.

API key errors: Double-check your keys and ensure they are loaded correctly in secrets.toml.

Deployment: For Streamlit Cloud or other platforms, add your secrets via their environment or secrets management UI.

# Contribution
We welcome contributions! Whether it’s fixing bugs, improving documentation, or adding new features, please open an issue or submit a pull request.



Contact
Created by Amina Naaz.
Feel free to reach out for questions, feedback, or collaborations at aminanaazpython@gmail.com.
 
Thank you for checking out AI-Procurement-Buddy! 🚀
