import streamlit as st
from ai_chatbot import get_response

st.title("ShopEasy Customer Support Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if user := st.chat_input("Ask about orders, returns, products..."):
    st.session_state.messages.append({"role": "user", "content": user})
    st.chat_message("user").write(user)

    # Try rule-based first 

    # If nothing matched → LLM with full history
    reply = get_response(user, st.session_state.messages[-10:])  # last 10 turns

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)

# streamlit run web.py