import streamlit as st
from rag.rag import query_rag
from constants.filepaths import CHROMA_PATH

st.title("MSME Loan Advisor")


def app():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if query_text := st.chat_input("Any help with your loans?"):
        # Append the user's message to session state
        st.session_state.messages.append({"role": "user", "content": query_text})

        # Process the response using your RAG function
        with st.spinner("Processing your query..."):
            # Process the response using your RAG function
            formatted_response, response_text = query_rag(query_text, CHROMA_PATH)

        if formatted_response:
            # Append assistant's response to session state
            st.session_state.messages.append({"role": "assistant", "content": formatted_response})
        else:
            st.session_state.messages.append({"role": "assistant", "content": "No relevant documents found."})

    # Display the entire conversation history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
