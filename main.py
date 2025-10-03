import data_loader as loader

from model.league import League
from model.premier import Premier
from model.brasileirao import Brasileirao


# TODO CLI e API


def main():
    df = Brasileirao(loader.load_brasileirao())

    return


if __name__ == "__main__":
    main()
