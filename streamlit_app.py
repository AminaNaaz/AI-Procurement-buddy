from ai_procurement_project.main import main
import streamlit as st

if __name__ == "__main__":
    # Optionally set environment variables for your keys here if your main.py depends on them being set globally
    import os
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
    os.environ["SERPER_API_KEY"] = st.secrets["SERPER_API_KEY"]

    main()
