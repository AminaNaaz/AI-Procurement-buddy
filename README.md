## AI-Procurement-Buddy
AI-Procurement-Buddy is an intelligent AI assistant designed to automate procurement workflows by discovering suppliers, extracting contact details, and drafting quotation emails. Built with Python, Streamlit, LangChain, and LangGraph (optional), this tool streamlines procurement processes leveraging large language models and web scraping techniques.

# Features
Supplier Discovery: Search for relevant suppliers based on user queries using Serper API and web scraping.

Contact Extraction: Extract supplier emails, phone numbers, and addresses using regex and LLM-enhanced parsing.

Quotation Email Drafting: Generate professional procurement emails using large language models.

Multi-Workflow Agent: Route user queries intelligently between supplier discovery and email drafting.

Streamlit UI: Simple and interactive web interface for easy use.

Extensible: Optionally integrate LangGraph for orchestrating AI workflows as graphs.

# Tech Stack
Python 3.9+

Streamlit (for UI)

LangChain (LLM orchestration)

LangGraph (optional, for workflow orchestration)

BeautifulSoup4 (web scraping)

Requests (HTTP calls)

Serper API (Google search API alternative)

OpenAI GPT-4 (LLM backend)

# Getting Started
Prerequisites
Python 3.9 or higher

Serper API Key

OpenAI API Key

# Installation
Clone the repo

bash
Copy
Edit
git clone https://github.com/AminaNaaz/AI-Procurement-buddy.git
cd AI-Procurement-buddy
Create a virtual environment

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Set up secrets

Create a secrets.toml file in the root directory (make sure it's in .gitignore) with your API keys:

toml
Copy
Edit
secrets.toml
openai_api_key = "your-openai-api-key"
serper_api_key = "your-serper-api-key"
Usage
Run the Streamlit app
bash
Copy
Edit
streamlit run streamlit_app.py
Open your browser at http://localhost:8501 and interact with the AI Procurement Buddy UI.

# Available workflows
Supplier discovery: Ask the assistant to find suppliers for a product or service in a location.

Quotation email drafting: Request the assistant to generate a professional quotation or procurement email.

# Project Structure
graphql
Copy
Edit
ai_procurement_project/
├── agents/
│   ├── supplier_agent.py         # Supplier search and extraction logic
│   ├── email_agent.py            # Email drafting logic
│   └── router_agent.py           # Routes queries to workflows
├── config.py                    # API keys and LLM configuration
├── langgraph_workflow.py        # (Optional) LangGraph workflow orchestration
├── main.py                      # Core logic orchestrator
└── utils.py                     # Utility functions
streamlit_app.py                # Streamlit UI entry point
requirements.txt                # Dependencies list
secrets.toml                   # API keys (not committed)
README.md                      # This file
LangGraph Integration (Optional)
If you want to use LangGraph for better workflow orchestration:

Add langgraph to your requirements.txt

Define your workflow graph in langgraph_workflow.py

Modify router_agent.py to route queries through LangGraph nodes

This approach modularizes your procurement assistant and makes it easy to add new capabilities.

# Troubleshooting
Pillow build errors: If you see errors installing Pillow on deployment platforms, ensure your environment has necessary build tools or pin Pillow version in requirements.txt.

API key errors: Confirm that your secrets.toml contains valid API keys and the app reads them correctly.

Streamlit Cloud deployment: Make sure secrets are added via Streamlit’s advanced settings if deploying on Streamlit Cloud.

# Contributing
Contributions are welcome! Please open issues or submit pull requests.
