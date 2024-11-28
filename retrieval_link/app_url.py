import rag_with_url
import streamlit as st

st.set_page_config(page_title="RAG with URL", page_icon="🧠", layout="wide")
st.title("RAG with URL")
st.divider()

col_input, col_rag, col_normal = st.columns([1, 4, 1])
with col_input:
    target_url = st.text_input("URL", placeholder="Drop a URL here")
    st.divider()
    prompt = st.text_input("Prompt", placeholder="What's up?", key="url_prompt")
    st.divider()
    summit_btn = st.button(label="Submit", key="url_btn")

    if summit_btn:
        with col_rag:
            with st.spinner("Processing..."):
                st.success("Response: ")
                response = rag_with_url.rag_with_url(target_url, prompt)
                st.markdown(response)
                st.divider()
            with col_normal:
                with st.spinner("Processing..."):
                    st.info("Response: ")
                    response = rag_with_url.ask_chatbot(prompt)
                    st.markdown(response)
                    st.divider()
