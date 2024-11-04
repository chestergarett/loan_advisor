from langchain.vectorstores.chroma import Chroma # Importing Chroma vector store from Langchain
from langchain_community.embeddings import OpenAIEmbeddings # Importing OpenAI embeddings from Langchain
from dotenv import load_dotenv
import os
openai_api_key = os.getenv('OPEN_AI_API_KEY')

CHROMA_PATH = r'./chroma/'

def get_chroma_docs():
    # Connect to Chroma DB
    embedding_function = OpenAIEmbeddings(openai_api_key=openai_api_key)
    db = Chroma(collection_name='loan_documents',persist_directory=CHROMA_PATH, embedding_function=embedding_function)    # Access the 'loan_documents' collection with persistence
    print(db.get())

if __name__=='__main__':
    get_chroma_docs()