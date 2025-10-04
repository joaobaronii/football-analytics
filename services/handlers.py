from model.league import League
from model.brasileirao import Brasileirao
import config

def handle_team(league: League, calculator_status: bool):
    pass

def handle_h2h(league: League, calculator_status: bool):
    pass

def handle_year_range(league: League):
    start_year = int(input("Enter start year(2012-2025): "))
    if  not 2012 <= start_year <= 2025:
        print("Year not available.")
        return None, None

    is_range = input("Do you want to specify an end year for a range? (Y/N): ").upper()
    if is_range == "Y":
        end_year = int("Enter the end year(2012-2025): ")
        if  not 2012 <= end_year <=2025:
            print("Year not available.")
            return None, None
        return league.by_year(start_year, end_year)
    
    return league.by_year(year1 = start_year)



def handle_league(league: League):
    while True:
        print(f"\n--- {league.name} Menu  ---")
        print("1. Stat a stat sum")
        print("2. View a stat mean")
        if league.name == "Brasileirao":
            print("3. Apply filter by years")
        print("0. Back to previous menu")

        op = input("Choose an option: ")

        if op == "1" or op == "2":
            stat = None
            while stat not in league.dataset_stats and stat != "0":
                print(f"Stats available {league.dataset_stats}")
                stat = input("Enter a stat: ").upper()
                if stat not in league.dataset_stats:
                    print("stat not in the list")

        match op:
            case "1":
                print(f"{stat} sum: {league.get_stat_sum(stat)}")
            case "2":
                print(f"{stat} per game: {league.get_stat_mean(stat)}")
            case "3":
                if league.name != "Brasileirao":
                    print("Invalid option")
                    continue
                league.df = handle_year_range(league)
            case "0":
                return
            case "_":
                print("Invalid option")

