from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader # Importing PDF loader from Langchain
from langchain.schema import Document # Importing Document schema from Langchain
from langchain.text_splitter import RecursiveCharacterTextSplitter # Importing text splitter from Langchain
from langchain.vectorstores.chroma import Chroma # Importing Chroma vector store from Langchain
from langchain_community.embeddings import OpenAIEmbeddings # Importing OpenAI embeddings from Langchain
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langsmith import traceable
from langsmith import Client
from langsmith.run_trees import RunTree
from dotenv import load_dotenv
import os
import shutil
import json
import pandas as pd
import re

load_dotenv()
openai_api_key = os.getenv('OPEN_AI_API_KEY')
langchain_tracing = os.getenv('LANGCHAIN_TRACING_V2')
langchain_endpoint = os.getenv('LANGCHAIN_ENDPOINT')
langchain_api_key = os.getenv('LANGCHAIN_API_KEY')
langchain_project = os.getenv('LANGCHAIN_PROJECT')

def load_pdf_documents(DATA_PATH):
  document_loader = PyPDFDirectoryLoader(DATA_PATH)
  return document_loader.load()
    
def load_json_to_documents(file_path: str) -> list[Document]:
    documents = []
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    for url, content_dict in data.items():
        content = content_dict.get('content', "")
        text_splitter = RecursiveCharacterTextSplitter(
          chunk_size=300,
          chunk_overlap=100,
          length_function=len,
          add_start_index=True,
        )
        chunks = text_splitter.split_text(content)
        for chunk in chunks:
            documents.append(Document(page_content=chunk, metadata={"source": url}))
    
    return documents


def split_text(documents: list[Document]):
  text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300, 
    chunk_overlap=100, 
    length_function=len,
    add_start_index=True, 
  )

  chunks = text_splitter.split_documents(documents)
  return chunks

def save_to_chroma(chunks: list[Document],CHROMA_PATH):
  if os.path.exists(CHROMA_PATH):
    db = Chroma(
        collection_name="loan_documents",
        persist_directory=CHROMA_PATH,
        embedding_function=OpenAIEmbeddings(openai_api_key=openai_api_key)
    )
  else:
    db = Chroma.from_documents(
        chunks,
        OpenAIEmbeddings(openai_api_key=openai_api_key),
        persist_directory=CHROMA_PATH,
        collection_name="loan_documents"
    )
    
  # Add new documents to the collection
  db.add_documents(chunks)
  
  # Persist changes
  db.persist()
  print(f"Appended {len(chunks)} chunks to {CHROMA_PATH}.")

#Parquet loader
def load_parquet_documents(parquet_folder_path: str) -> list[Document]:
    documents = []
    for file_name in os.listdir(parquet_folder_path):
        if file_name.endswith(".parquet"):
            file_path = os.path.join(parquet_folder_path, file_name)
            df = pd.read_parquet(file_path)
            id_columns = [col for col in df.columns if col.endswith('_ID')]
            for id_col in id_columns:
               df[id_col] = df[id_col].astype(str)
            df = df.dropna()  
            df = df.drop_duplicates()
            for _, row in df.iterrows():
              content = {key: (value.isoformat() if isinstance(value, pd.Timestamp) else value) for key, value in row.to_dict().items()}
              content_str = json.dumps(content)  # Convert to JSON string
              customer_id = row['CUSTOMER_ID']
              documents.append(Document(page_content=content_str, metadata={"source": file_name, "customer_id": customer_id}))

            df.to_csv(f'data/inputs/csv/{file_name}.csv')
                
    return documents
  
def generate_data_store(DATA_PATH,CHROMA_PATH,data_type):
  if data_type=='PDF':
    documents = load_pdf_documents(DATA_PATH)
    chunks = split_text(documents)
    save_to_chroma(chunks,CHROMA_PATH)
  elif data_type=='JSON':
    documents = load_json_to_documents(DATA_PATH)
    save_to_chroma(documents,CHROMA_PATH)
  elif data_type == 'PARQUET':
    documents = load_parquet_documents(DATA_PATH)
    save_to_chroma(documents,CHROMA_PATH)
  else:
    print("Invalid data type. Please choose from PDF, JSON, PARQUET.")

@traceable(run_type="retriever")
def get_retriever(query_text,CHROMA_PATH):
  embedding_function = OpenAIEmbeddings(openai_api_key=openai_api_key)
  db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function,collection_name="loan_documents")
  customer_id_match = re.search(r"(\d+\.?\d*)", query_text)

  metadata_results = []
  similarity_results = []
  
  if customer_id_match:
    customer_id = customer_id_match.group(1)
    filter_dict = {"customer_id": {"$in": [customer_id]}}
    print(f"Searching for documents with Customer ID: {customer_id}")
    base_retriever = db.as_retriever(search_kwargs={'k': 10, 'filter': filter_dict})
    metadata_results = base_retriever.invoke(query_text)
    metadata_results_final = []
    for metadata_result in metadata_results:
      metadata_results_final.append([metadata_result,1])
    query_text = re.sub(r"Customer ID \d+\.?\d*", "", query_text).strip()

  if query_text:
    print("Performing similarity search on the remaining query...")
    similarity_results = db.similarity_search_with_relevance_scores(query_text, k=20)
  
  print('metadata_results',metadata_results)
  combined_results = metadata_results_final + similarity_results
  
  return combined_results

@traceable(run_type='llm')
def invoke_llm(prompt):
  model = ChatOllama(
  model="llama3.2",
  temperature=0,
)

  messages = [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": prompt}
  ]

  response_text = model.invoke(messages)
  return response_text

@traceable
def query_rag(query_text,CHROMA_PATH):
  results = get_retriever(query_text,CHROMA_PATH)
  if len(results) == 0 or results[0][1] < 0.7:
    print(f"Unable to find matching results.")
    return None, None
  
  context_text = "\n\n - -\n\n".join([doc.page_content for doc, _score in results])
  prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
  prompt = prompt_template.format(context=context_text, question=query_text)

 
  sources = [doc.metadata.get("source", None) for doc, _score in results]
  response_text = invoke_llm(prompt)
  formatted_response = response_text.content
  return formatted_response, response_text

# generate_data_store()
# query_text = "What is the purpose of the data operations engineer?"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:
{context}
 - -
Answer the question based on the above context: {question}
"""

# formatted_response, response_text = query_rag(query_text)
# # and finally, inspect our final response!
# print(response_text)

