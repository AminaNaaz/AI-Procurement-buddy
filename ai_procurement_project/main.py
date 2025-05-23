import streamlit as st
from ai_procurement_project.router_agent import route_query
from ai_procurement_project.utils.logger import logger

def main():
    st.set_page_config(page_title="AI Procurement Assistant", page_icon="📦")
    st.title("📦 AI Procurement Assistant")
    st.caption("An agentic assistant for supplier discovery and email drafting")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("What procurement help do you need?")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        logger.info(f"User input: {prompt}")

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("🔎 Processing your request..."):
            try:
                openai_key = st.secrets["OPENAI_API_KEY"]
                serper_key = st.secrets["SERPER_API_KEY"]

                response = route_query(prompt, openai_key=openai_key, serper_key=serper_key)
                logger.info(f"Generated response: {response[:100]}...")
            except Exception as e:
                response = f"🚨 An error occurred: {str(e)}"
                logger.exception("Critical failure in agent execution.")

        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"Application crashed: {str(e)}", exc_info=True)
        st.error("🚨 The application encountered a critical error.")
