import pandas as pd


def load_brasileirao():
    columns = ["Season", "Date", "Home", "Away", "HG", "AG", "Res"]
    # HG = home goals; AG = away goals; Res = result
    print("Loading Brasileirao data...")
    df = pd.read_csv("data/brasileirao.csv", usecols=columns)
    print("Data successfully loaded!")

    df = df.set_index("Date")

    df = df.rename(columns={"Res": "FTR"})

    return df


def load_premier_25_26():
    columns = [
        "Date",
        "HomeTeam",
        "AwayTeam",
        "FTHG",
        "FTAG",
        "FTR",
        "HTHG",
        "HTAG",
        "Referee",
        "HS",
        "AS",
        "HST",
        "AST",
        "HC",
        "AC",
        "HF",
        "AF",
        "HY",
        "AY",
        "HR",
        "AR",
    ]
    # FTH/AG = full time home/away goals; FTR = full time result; HTH/AG = half time home/away goals; H/AS = home/away shots; H/AST = home/away shots on target;
    # H/AC = home/away corners; H/AF = H/A fouls committed; H/AY = H/A yellow cards; H/AR = H/A red cards

    print("Loading Premier League 25/26 data...")
    df = pd.read_csv("data/premierleague25-26.csv", usecols=columns)
    print("Data successfully loaded!")

    df = df.set_index("Date")
    df = df.rename(columns={"HomeTeam": "Home", "AwayTeam": "Away"})

    return df

def reload_dataframe(league_name):
    if league_name == "Brasileirao":
        return load_brasileirao()
    if league_name == "Premier League":
        return load_premier_25_26()


if __name__ == "__main__":
    df = load_premier_25_26()
    print(df)
