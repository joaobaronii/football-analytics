import services.data_loader as loader
import services.odd_calculator as od

from model.league import League
from model.premier import Premier
from model.brasileirao import Brasileirao


# TODO CLI 


def main():
    df = Brasileirao(loader.load_brasileirao())

    df = df.by_year(2025)

    print(df)

    return


if __name__ == "__main__":
    main()
