import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI



# Load environment variables from .env file
load_dotenv()

# Fetch the API key securely
openai_api_key = os.getenv("OPENAI_API_KEY")

# Safety check
if not openai_api_key:
    raise RuntimeError("OPENAI_API_KEY environment variable not set")

# Fetch the Serper API key securely
serper_api_key = os.getenv("SERPER_API_KEY")
if not serper_api_key:
    raise RuntimeError("SERPER_API_KEY environment variable not set")


# Instantiate the GPT-4o model
llm = ChatOpenAI(
    model_name="gpt-4o",
    temperature=0.3,
    openai_api_key=openai_api_key
)
