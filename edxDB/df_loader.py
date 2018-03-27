import os
import pandas as pd
workpath = os.path.dirname(os.path.abspath(__file__))


def local_path(filename):
    return os.path.join(workpath, filename)


df_pool = {}


def load_df(filename):
    if filename in df_pool:
        return df_pool[filename]
    extension = os.path.splitext(filename)[1][1:]
    df = None
    if extension == "csv":
        df = pd.read_csv(local_path(filename))
    elif extension == "pkl":
        df = pd.read_pickle(local_path(filename))
    df_pool[filename] = df
    return df
