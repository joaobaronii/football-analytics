from data_loader import load_brasileirao
from data_processor import Brasileirao

def main():

    df = Brasileirao(load_brasileirao())

    return



if __name__ == "__main__":
    main()