import services.odd_calculator as od
from model.league import League


def handle_calculator(mean):
    threshold = float(input("Enter the threshold: "))
    mode = input("Enter the mode(over, under or exactly): ").lower()

    house_odd = None
    edge_status = input("Do you want to calculate the house edge? (Y/N): ").upper()
    if edge_status == "Y":
        house_odd = float(input("Enter the house odd: "))

    prob, fair_odd, house_edge = od.calculate_all(mean, threshold, mode, house_odd)

    return prob, fair_odd, house_edge


def handle_team(league: League, calculator_status: bool):
    team = None
    while team not in league.team_list:
        print(f"Teams available{league.team_list}")
        team = input("Enter a team to analyze: ")
        if team not in league.team_list:
            print("Team not in the dataset.")

    league.df = league.by_team(team)

    while True:
        print(f"\n--- Analysis for {team} ---")
        print("1. View team stats sum")
        print("2. View team stats per game (compute the odd if enabled)")
        print("0. Back to previous menu")

        choice = input("Choose an option: ")

        if choice != "0":
            stat = None
            stats_list = list(league.stat_map.keys())
            if league.name != "Brasileirao":
                stats_list.append("cards")
                stats_list.append("second half goals")

            while stat not in stats_list:
                print(f"Stats available {stats_list}")
                stat = input("Enter a stat: ").lower()
                if stat not in stats_list:
                    print("Stat not in the list")

        match choice:
            case "1":
                stat_sum = None
                if stat == "cards":
                    stat_sum = league.total_cards_sum(team)
                elif stat == "second half goals":
                    stat_sum = league.goals_second_half_sum(team)
                else:
                    stat_sum = league.get_team_stat_sum(team, stat)

                print(f"{stat} sum: {stat_sum}")
            case "2":
                stat_avg = None
                if stat == "cards":
                    stat_avg = league.total_cards_per_game(team)
                elif stat == "second half goals":
                    stat_avg = league.goals_second_half_per_game(team)
                else:
                    stat_avg = league.get_team_stat_mean(team, stat)

                print(f"{stat} per game: {stat_avg}")

                if calculator_status:
                    prob, fair_odd, house_edge = handle_calculator(stat_avg)
                    percent = prob * 100
                    if house_edge:
                        print(
                            f"Won probability = {percent: .2f}%; Fair odd = {fair_odd: .2f}; House edge = {house_edge: .2f}%"
                        )
                    else:
                        print(f"Won probability = {percent: .2f}%; Fair odd = {fair_odd: .2f}")
                    print("THIS NUMBERS DOES NOT CONSIDER EVERY FACTORS TORY INVOLVED IN A ODD, IT JUST LOOK INTO THE AVERAGE.")
                    print("Example of factors not in the math: Home/Away, Teams lineups(injuries, suspensions), Teams form...")
                    
            case "0":
                return
            case _:
                print("Invalid option")


def handle_h2h(league: League):
    print(league.team_list)
    team1 = input("Enter the first team: ")
    team2 = input("Enter the second team: ")
    is_only_home = input(f"Get only matches in {team1}'s home?(Y/N): ").upper()
    if is_only_home == "Y":
        only_home = True
    else:
        only_home = False

    league.df = league.head_to_head(team1, team2, only_home)
    if league.df.empty:
        print(f"\nNo matches found between {team1} and {team2}.")
        return

    summary1 = league.get_result_summary(team1)
    summary2 = league.get_result_summary(team2)


    if league.name == "Brasileirao":
        handle_year_range(league)

    print("\nMatchup Summary:")
    print(f"{team1}: Wins: {summary1['W']}, Losses: {summary1['L']}, Draws: {summary1['D']}")
    print(f"{team2}: Wins: {summary2['W']}, Losses: {summary2['L']}, Draws: {summary2['D']}")


    stat_status = input("Do you want to get some matchup stat? (Y/N): ").upper()

    if stat_status == "Y":
        stat = None
        stats_list = list(league.stat_map.keys())
        while stat not in stats_list:
            print(stats_list)
            stat = input("Enter the stat: ")
            if stat not in stats_list:
                    print("stat not in the list")

        print(f"{stat} in this matchup: {team1} = {league.get_team_stat_sum(team1, stat)}; {team2} = {league.get_team_stat_sum(team2, stat)}")


def handle_year_range(league: League):
    start_year = int(input("Enter start year(2012-2025): "))
    if not 2012 <= start_year <= 2025:
        print("Year not available.")
        return None, None

    is_range = input("Do you want to specify an end year for a range? (Y/N): ").upper()
    if is_range == "Y":
        end_year = int("Enter the end year(2012-2025): ")
        if not 2012 <= end_year <= 2025:
            print("Year not available.")
            return None, None
        return league.by_year(start_year, end_year)

    return league.by_year(year1=start_year)


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
