import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from rag.rag import generate_data_store
from constants.filepaths import PDF_PATH, CHROMA_PATH, JSON_PATH, PARQUET_PATH

save_pdf_to_chroma = True
save_json_to_chroma = True
save_parquet_to_chroma = True

if save_pdf_to_chroma:
    generate_data_store(PDF_PATH,CHROMA_PATH,'PDF')

if save_json_to_chroma:
    generate_data_store(JSON_PATH,CHROMA_PATH,'JSON')

if save_parquet_to_chroma:
    generate_data_store(PARQUET_PATH,CHROMA_PATH,'PARQUET')