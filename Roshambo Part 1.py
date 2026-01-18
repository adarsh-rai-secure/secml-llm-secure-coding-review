# Adarsh Rai
# I used GPT 5.1 to help me write this code.
import random
import sys

def prompt_yes_no():
    while True:
        response = input("Shall we play a game? (Y/N): ").strip().upper()
        if response in ("Y", "N"):
            return response
        print("Response must be Y or N")

def prompt_choice(name):
    prompt = (
        f"Hello {name}, let’s get started. When you are ready, enter your choice.\n"
        "R is for Rock, P is for Paper, S is for Scissors. Q is to Quit. I is for INFO: "
    )
    while True:
        choice = input(prompt).strip().upper()
        if choice in ("R", "P", "S", "Q", "I"):
            return choice
        print("Invalid Response")

def prompt_next_choice():
    prompt = (
        "Enter your choice. R is for Rock, P is for Paper, S is for Scissors. "
        "Q is to Quit. I is for INFO: "
    )
    while True:
        choice = input(prompt).strip().upper()
        if choice in ("R", "P", "S", "Q", "I"):
            return choice
        print("Invalid Response")

def computer_move():
    return random.choice(["R", "P", "S"])

def move_to_word(move):
    return {"R": "Rock", "P": "Paper", "S": "Scissors"}[move]

def determine_outcome(user, comp):
    """
    Returns: outcome, rule_text
    outcome in {"win", "lose", "tie"}
    """
    if user == comp:
        return "tie", None

    # Rules and who wins
    # Paper covers Rock
    # Scissors cut Paper
    # Rock smashes Scissors
    if user == "P" and comp == "R":
        return "win", "Paper covers Rock - Paper Wins!"
    if user == "R" and comp == "P":
        return "lose", "Paper covers Rock - Paper Wins!"

    if user == "S" and comp == "P":
        return "win", "Scissors cut Paper - Scissors Win!"
    if user == "P" and comp == "S":
        return "lose", "Scissors cut Paper - Scissors Win!"

    if user == "R" and comp == "S":
        return "win", "Rock smashes Scissors - Rock Wins!"
    if user == "S" and comp == "R":
        return "lose", "Rock smashes Scissors - Rock Wins!"

    # Should never reach here
    return "tie", None

def print_info(name, overall_stats, choice_stats):
    wins, losses, ties = overall_stats["wins"], overall_stats["losses"], overall_stats["ties"]
    total_decisions = wins + losses
    if total_decisions > 0:
        win_pct = (wins / total_decisions) * 100.0
    else:
        win_pct = 0.0

    print()
    print(f"{name}, here are your statistics:")
    print("Overall:")
    print(f"  Win-Loss-Tie: {wins}-{losses}-{ties}")
    print(f"  Winning percentage (excluding ties): {win_pct:.2f}%")

    print()
    print("By choice:")
    for move, label in [("R", "Rock"), ("P", "Paper"), ("S", "Scissors")]:
        w = choice_stats[move]["wins"]
        l = choice_stats[move]["losses"]
        t = choice_stats[move]["ties"]
        decisions = w + l
        if decisions > 0:
            pct = (w / decisions) * 100.0
        else:
            pct = 0.0
        print(f"  {label}:")
        print(f"    Win-Loss-Tie: {w}-{l}-{t}")
        print(f"    Winning percentage (excluding ties): {pct:.2f}%")
    print()
    print("Let’s play again")

def main():
    response = prompt_yes_no()
    if response == "N":
        print("Goodbye")
        sys.exit(0)

    print("Great, the game is Roshambo! What is your name?")
    name = input("Enter your name: ").strip()
    if not name:
        name = "Player"

    # Initial choice after name
    choice = prompt_choice(name)

    # Statistics
    overall_stats = {"wins": 0, "losses": 0, "ties": 0}
    choice_stats = {
        "R": {"wins": 0, "losses": 0, "ties": 0},
        "P": {"wins": 0, "losses": 0, "ties": 0},
        "S": {"wins": 0, "losses": 0, "ties": 0},
    }

    games_played = 0
    win_streak = 0
    loss_streak = 0
    fifteen_message_shown = False

    while True:
        if choice == "Q":
            print("Goodbye")
            break

        if choice == "I":
            print_info(name, overall_stats, choice_stats)
            choice = prompt_next_choice()
            continue

        # R, P, or S
        user_move = choice
        comp_move = computer_move()

        outcome, rule_text = determine_outcome(user_move, comp_move)

        if outcome == "tie":
            overall_stats["ties"] += 1
            if user_move in choice_stats:
                choice_stats[user_move]["ties"] += 1

            win_streak = 0
            loss_streak = 0

            games_played += 1

            print(f"You chose {move_to_word(user_move)}, computer chose {move_to_word(comp_move)}.")
            print("It’s a tie. A strange game. The only winning move is not to play.")
        elif outcome == "win":
            overall_stats["wins"] += 1
            if user_move in choice_stats:
                choice_stats[user_move]["wins"] += 1

            win_streak += 1
            loss_streak = 0

            games_played += 1

            print(f"You chose {move_to_word(user_move)}, computer chose {move_to_word(comp_move)}.")
            if win_streak == 3:
                print("Wow, hot streak!!")
            print(f"Great job {name}, you win!")
            if rule_text:
                print(rule_text)
        elif outcome == "lose":
            overall_stats["losses"] += 1
            if user_move in choice_stats:
                choice_stats[user_move]["losses"] += 1

            loss_streak += 1
            win_streak = 0

            games_played += 1

            print(f"You chose {move_to_word(user_move)}, computer chose {move_to_word(comp_move)}.")
            if loss_streak == 3:
                print("Lost again, maybe try solitaire!")
            print(f"Sorry {name}, you lose!")
            if rule_text:
                print(rule_text)

        # Fifteen game message
        if games_played == 15 and not fifteen_message_shown:
            print("Don’t you have anything else to do?!")
            fifteen_message_shown = True

        print("Let’s play again")
        choice = prompt_next_choice()

if __name__ == "__main__":
    main()
