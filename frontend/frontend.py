import streamlit as st
from rag.rag import query_rag
from constants.filepaths import CHROMA_PATH

st.title("MSME Loan Advisor")

def app():
    query_text = st.text_input("Enter your question here:")

    # Add a button for submitting the query
    if st.button('Submit Query'):
        # If the button is clicked and there is a query, process it
        if query_text:
            # Use the spinner to show a loading animation while waiting for a response
            with st.spinner('Processing your query...'):
                formatted_response, response_text = query_rag(query_text,CHROMA_PATH)
            if response_text:
                st.write(f"{formatted_response}")
            else:
                st.write("No relevant documents found.")
        else:
            st.write("Please enter a question.")
