import streamlit as st
from chatbot import initialize_chatbot

st.set_page_config(page_title="University Chatbot")

st.title("🎓 University Knowledge Assistant")

# Initialize once
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = initialize_chatbot()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Show history
for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        st.write(msg)

# Input
query = st.chat_input("Ask something...")

if query:
    st.session_state.chat_history.append(("user", query))

    answer = st.session_state.qa_chain(query)

    st.session_state.chat_history.append(("assistant", answer))

    with st.chat_message("user"):
        st.write(query)

    with st.chat_message("assistant"):
        st.write(answer)

# Sidebar
if st.sidebar.button("Clear Chat"):
    st.session_state.chat_history = []