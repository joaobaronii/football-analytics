from data_loader import load_brasileirao
from data_processor import Brasileirao

# TODO CLI e API
 
def main():

    df = Brasileirao(load_brasileirao())

    return



if __name__ == "__main__":
    main()