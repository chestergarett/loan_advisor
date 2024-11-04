import pandas as pd
import numpy as np
import os
# from constants.filepaths import TABULAR_PATH

TABULAR_PATH = r'./data/inputs/parquets'
directory = TABULAR_PATH
files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.parquet')]

def load_parquets(files):
    dfs = {}
    for file in files:
        filename = file.split('./data/inputs/parquets/')[1]
        filename = filename.split('.parquet')[0]
        df = pd.read_parquet(file)
        dfs[filename] = df

    return dfs

if __name__=='__main__':
    dfs = load_parquets(files)
    print(dfs['LOAN_Q42023_Q12024'].columns())
