import streamlit as st
from book_meeting import book_meeting


st.title("Book a Meeting Chatbot")
st.write("Chat with me to book a meeting in Microsoft Teams")

user_input = st.text_input("You:", "")

if user_input:
    response = book_meeting(user_input)
    st.write("Bot:", response)
