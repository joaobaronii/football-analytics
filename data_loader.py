import pandas as pd

def load_brasileirao():
    columns = ["Season", "Date", "Home", "Away", "HG", "AG", "Res"]
    # HG = home goals; AG = away goals; Res = result
    print("Loading Brasileirao datas into the dataframe...")
    df = pd.read_csv("data/brasileirao.csv", usecols=columns)
    print("Data loaded successfully!")

    df = df.set_index("Season")

    return df