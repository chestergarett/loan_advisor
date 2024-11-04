import pandas as pd
import numpy as np
import os
# from constants.filepaths import TABULAR_PATH

TABULAR_PATH = r'./data/inputs/parquets'
directory = TABULAR_PATH
files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.parquet')]

def load_parquets(files):
    dfs = []
    for file in files:
        filename = file.split('.parquet')[0]
        df = pd.read_parquet(file)
        dfs.append({filename: df})

        print(df)



