import services.data_loader as loader
import sys
import services.odd_calculator as od
import config
import services.handlers as handler

from model.premier import Premier
from model.brasileirao import Brasileirao
from services.dataset_updater import update_csv


# TODO terminar handlers


def main():
    
    league_obj = None
    league_choice = None

    while True:
        if league_obj is None:
            print("\n--- Football analytics ---")
            print("1. Brasileirao(2012 - 2025)")
            print("2. Premier League (25/26)")
            print("0. Exit")
            league_choice = input("Choose a league: ")

            match league_choice:
                case "1":
                    update_csv(config.LEAGUE_CONFIG["brasileirao"])
                    league_obj = Brasileirao(loader.load_brasileirao())
                case "2":
                    update_csv(config.LEAGUE_CONFIG["premier"])
                    league_obj = Premier(loader.load_premier_25_26())
                case "0":
                    print("Exiting...")
                    sys.exit()
                case _:
                    print("Invalid option.")
                    continue
        
        print(f"\n --- Menu:{league_obj.name}  ---")
        print("1. Team Analysis")
        print("2. Head-to-Head(H2H) Analysis")
        print("3. League Analysis")
        print("4. Change league")
        print("0. Exit")

        op = input("Choose an option: ")

        match op:
            case "1":
                calculator_status = input("Use odd calculator ?(Y/N): ").upper()
                if calculator_status == "Y":
                    calculator_status = True
                else: 
                    calculator_status = False
                handler.handle_team(league_obj, calculator_status)
            case "2":
                handler.handle_h2h(league_obj)
            case "3":
                handler.handle_league(league_obj)
            case "4":
                league_obj = None
            case "0":
                print("Exiting...")
                sys.exit()
            case _:
                print("Invalid option.")

        if op != "4":
            league_obj.df = loader.reload_dataframe(league_obj.name) 

    return


if __name__ == "__main__":
    main()
