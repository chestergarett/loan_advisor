import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from rag.rag import generate_data_store
from constants.filepaths import DATA_PATH, CHROMA_PATH

generate_data_store(DATA_PATH,CHROMA_PATH)