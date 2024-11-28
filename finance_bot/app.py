import streamlit as st
from define_agent import define_agent
from langchain_core.messages import HumanMessage

st.title("Test Trading Chatbot")
st.write("Ask me anything about finance")

user_input = st.text_input("You:", "")
finance_agent = define_agent()


def generate_response(agent, user_input):
    """
    Generate a response to a query using the initialized finance agent.
    """
    query = HumanMessage(content=user_input)
    response = agent({"input": query.content})
    return response


if user_input:
    response = generate_response(finance_agent, user_input)
    st.write("Assistant:", response)
