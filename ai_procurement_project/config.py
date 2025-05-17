import streamlit as st
from langchain_openai import ChatOpenAI

# Fetch secrets from .streamlit/secrets.toml
openai_api_key = st.secrets["OPENAI_API_KEY"]
serper_api_key = st.secrets["SERPER_API_KEY"]

# Initialize LLM
llm = ChatOpenAI(
    model_name="gpt-4o",
    temperature=0.3,
    openai_api_key=openai_api_key
)
