# Adarsh Rai
# I used GPT 5.1 to help me write and refactor this code.

import random

VALID_MOVES = {"R": "Rock", "P": "Paper", "S": "Scissors"}
VALID_MENU_CHOICES = {"R", "P", "S", "Q", "I"}


def prompt_yes_no():
    while True:
        response = input("Shall we play a game? (Y/N): ").strip().upper()
        if response in ("Y", "N"):
            return response
        print("Response must be Y or N")


def get_menu_choice(prompt_text):
    while True:
        choice = input(prompt_text).strip().upper()
        if choice in VALID_MENU_CHOICES:
            return choice
        print("Invalid Response")


def computer_move():
    return random.choice(list(VALID_MOVES.keys()))


def move_to_word(move):
    try:
        return VALID_MOVES[move]
    except KeyError:
        raise ValueError(f"Invalid move code: {move!r}")


def determine_outcome(user, comp):
    """
    Returns (outcome, rule_text)
    outcome in {"win", "lose", "tie"}
    """
    if user == comp:
        return "tie", None

    rules = {
        ("P", "R"): ("win", "Paper covers Rock - Paper Wins!"),
        ("R", "P"): ("lose", "Paper covers Rock - Paper Wins!"),
        ("S", "P"): ("win", "Scissors cut Paper - Scissors Win!"),
        ("P", "S"): ("lose", "Scissors cut Paper - Scissors Win!"),
        ("R", "S"): ("win", "Rock smashes Scissors - Rock Wins!"),
        ("S", "R"): ("lose", "Rock smashes Scissors - Rock Wins!"),
    }

    try:
        return rules[(user, comp)]
    except KeyError:
        # Explicitly fail if something unexpected happens
        raise ValueError(f"Invalid outcome combination: user={user!r}, comp={comp!r}")


def print_info(name, overall_stats, choice_stats):
    wins = overall_stats["wins"]
    losses = overall_stats["losses"]
    ties = overall_stats["ties"]
    total_decisions = wins + losses

    win_pct = (wins / total_decisions) * 100.0 if total_decisions > 0 else 0.0

    print()
    print(f"{name}, here are your statistics:")
    print("Overall:")
    print(f"  Win-Loss-Tie: {wins}-{losses}-{ties}")
    print(f"  Winning percentage (excluding ties): {win_pct:.2f}%")

    print()
    print("By choice:")
    for move, label in VALID_MOVES.items():
        w = choice_stats[move]["wins"]
        l = choice_stats[move]["losses"]
        t = choice_stats[move]["ties"]
        decisions = w + l
        pct = (w / decisions) * 100.0 if decisions > 0 else 0.0
        print(f"  {label}:")
        print(f"    Win-Loss-Tie: {w}-{l}-{t}")
        print(f"    Winning percentage (excluding ties): {pct:.2f}%")
    print()
    print("Let's play again")


def play_round(user_move, name, overall_stats, choice_stats, win_streak, loss_streak):
    comp_move = computer_move()
    outcome, rule_text = determine_outcome(user_move, comp_move)

    print(f"You chose {move_to_word(user_move)}, computer chose {move_to_word(comp_move)}.")

    if outcome == "tie":
        overall_stats["ties"] += 1
        choice_stats[user_move]["ties"] += 1
        win_streak = 0
        loss_streak = 0
        print("It is a tie. A strange game. The only winning move is not to play.")
    elif outcome == "win":
        overall_stats["wins"] += 1
        choice_stats[user_move]["wins"] += 1
        win_streak += 1
        loss_streak = 0
        if win_streak == 3:
            print("Wow, hot streak!!")
        print(f"Great job {name}, you win!")
        if rule_text:
            print(rule_text)
    else:  # lose
        overall_stats["losses"] += 1
        choice_stats[user_move]["losses"] += 1
        loss_streak += 1
        win_streak = 0
        if loss_streak == 3:
            print("Lost again, maybe try solitaire!")
        print(f"Sorry {name}, you lose!")
        if rule_text:
            print(rule_text)

    return win_streak, loss_streak


def main():
    response = prompt_yes_no()
    if response == "N":
        print("Goodbye")
        return

    print("Great, the game is Roshambo! What is your name?")
    name = input("Enter your name: ").strip()
    if not name:
        name = "Player"

    first_prompt = (
        f"Hello {name}, let's get started. When you are ready, enter your choice.\n"
        "R is for Rock, P is for Paper, S is for Scissors. Q is to Quit. I is for INFO: "
    )
    choice = get_menu_choice(first_prompt)

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

    next_prompt = (
        "Enter your choice. R is for Rock, P is for Paper, S is for Scissors. "
        "Q is to Quit. I is for INFO: "
    )

    while True:
        if choice == "Q":
            print("Goodbye")
            break

        if choice == "I":
            print_info(name, overall_stats, choice_stats)
            choice = get_menu_choice(next_prompt)
            continue

        # R, P, or S
        win_streak, loss_streak = play_round(
            choice, name, overall_stats, choice_stats, win_streak, loss_streak
        )
        games_played += 1

        if games_played == 15 and not fifteen_message_shown:
            print("Don't you have anything else to do?!")
            fifteen_message_shown = True

        print("Let's play again")
        choice = get_menu_choice(next_prompt)


if __name__ == "__main__":
    main()
