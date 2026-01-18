# Adarsh Rai
# I used GPT 5.1 to help me design, optimize, and refactor this code.

import random
from dataclasses import dataclass, field
from typing import Dict, Tuple

# Constants
VALID_MOVES = {"R": "Rock", "P": "Paper", "S": "Scissors"}
VALID_MENU_CHOICES = {"R", "P", "S", "Q", "I"}

# Rule descriptions for outcomes
# Key is a tuple (winner_move, loser_move)
RULE_TEXT: Dict[Tuple[str, str], str] = {
    ("P", "R"): "Paper covers Rock - Paper wins!",
    ("S", "P"): "Scissors cut Paper - Scissors win!",
    ("R", "S"): "Rock smashes Scissors - Rock wins!",
}


@dataclass
class Record:
    wins: int = 0
    losses: int = 0
    ties: int = 0

    def register_win(self) -> None:
        self.wins += 1

    def register_loss(self) -> None:
        self.losses += 1

    def register_tie(self) -> None:
        self.ties += 1

    def decisions(self) -> int:
        return self.wins + self.losses

    def win_percentage(self) -> float:
        dec = self.decisions()
        return (self.wins / dec * 100.0) if dec > 0 else 0.0


@dataclass
class GameState:
    player_name: str
    overall: Record = field(default_factory=Record)
    per_move: Dict[str, Record] = field(default_factory=lambda: {
        "R": Record(),
        "P": Record(),
        "S": Record(),
    })
    games_played: int = 0
    win_streak: int = 0
    loss_streak: int = 0
    fifteen_message_shown: bool = 0


def prompt_yes_no() -> str:
    """Prompt the user with a Y/N question and validate the response."""
    while True:
        response = input("Shall we play a game? (Y/N): ").strip().upper()
        if response in ("Y", "N"):
            return response
        print("Response must be Y or N")


def get_menu_choice(prompt_text: str) -> str:
    """Prompt the user for a menu choice and validate it."""
    while True:
        choice = input(prompt_text).strip().upper()
        if choice in VALID_MENU_CHOICES:
            return choice
        print("Invalid response. Please enter R, P, S, Q, or I.")


def computer_move() -> str:
    """Randomly select the computer's move."""
    # Precompute the keys list once from the dict
    moves = tuple(VALID_MOVES.keys())
    return random.choice(moves)


def move_to_word(move: str) -> str:
    """Convert a move code (R, P, S) to its word representation."""
    if move not in VALID_MOVES:
        raise ValueError(f"Invalid move code: {move!r}")
    return VALID_MOVES[move]


def determine_outcome(user: str, comp: str) -> Tuple[str, str]:
    """
    Determine the outcome of a round.

    Returns:
        outcome: one of "win", "lose", or "tie"
        rule_text: explanatory text such as "Paper covers Rock - Paper wins!"
    """
    if user == comp:
        return "tie", ""

    if (user, comp) in RULE_TEXT:
        return "win", RULE_TEXT[(user, comp)]

    if (comp, user) in RULE_TEXT:
        return "lose", RULE_TEXT[(comp, user)]

    # If this ever happens, the logic or inputs are broken
    raise ValueError(f"Invalid outcome combination: user={user!r}, comp={comp!r}")


def print_info(state: GameState) -> None:
    """Print INFO statistics about the user's performance."""
    name = state.player_name
    overall = state.overall

    print()
    print(f"{name}, here are your statistics:")
    print("Overall:")
    print(f"  Win-Loss-Tie: {overall.wins}-{overall.losses}-{overall.ties}")
    print(f"  Winning percentage (excluding ties): {overall.win_percentage():.2f}%")

    print()
    print("By choice:")
    for move, label in VALID_MOVES.items():
        rec = state.per_move[move]
        print(f"  {label}:")
        print(f"    Win-Loss-Tie: {rec.wins}-{rec.losses}-{rec.ties}")
        print(f"    Winning percentage (excluding ties): {rec.win_percentage():.2f}%")

    print()
    print("Let's play again")


def play_round(state: GameState, user_move: str) -> None:
    """Execute one round of Roshambo given the user's move."""
    comp_move = computer_move()
    outcome, rule_text = determine_outcome(user_move, comp_move)

    user_word = move_to_word(user_move)
    comp_word = move_to_word(comp_move)
    print(f"You chose {user_word}, computer chose {comp_word}.")

    state.games_played += 1
    per_move_rec = state.per_move[user_move]

    if outcome == "tie":
        state.overall.register_tie()
        per_move_rec.register_tie()
        state.win_streak = 0
        state.loss_streak = 0
        print("It is a tie. A strange game. The only winning move is not to play.")
    elif outcome == "win":
        state.overall.register_win()
        per_move_rec.register_win()
        state.win_streak += 1
        state.loss_streak = 0
        if state.win_streak == 3:
            print("Wow, hot streak!!")
        print(f"Great job {state.player_name}, you win!")
        if rule_text:
            print(rule_text)
    else:  # lose
        state.overall.register_loss()
        per_move_rec.register_loss()
        state.loss_streak += 1
        state.win_streak = 0
        if state.loss_streak == 3:
            print("Lost again, maybe try solitaire!")
        print(f"Sorry {state.player_name}, you lose!")
        if rule_text:
            print(rule_text)

    if state.games_played == 15 and not state.fifteen_message_shown:
        print("Don't you have anything else to do?!")
        state.fifteen_message_shown = True


def main() -> None:
    response = prompt_yes_no()
    if response == "N":
        print("Goodbye")
        return

    print("Great, the game is Roshambo! What is your name?")
    name = input("Enter your name: ").strip()
    if not name:
        name = "Player"

    state = GameState(player_name=name)

    first_prompt = (
        f"Hello {name}, let's get started. When you are ready, enter your choice.\n"
        "R is for Rock, P is for Paper, S is for Scissors. Q is to Quit. I is for INFO: "
    )
    next_prompt = (
        "Enter your choice. R is for Rock, P is for Paper, S is for Scissors. "
        "Q is to Quit. I is for INFO: "
    )

    choice = get_menu_choice(first_prompt)

    while True:
        if choice == "Q":
            print("Goodbye")
            break

        if choice == "I":
            print_info(state)
            choice = get_menu_choice(next_prompt)
            continue

        # Must be R, P, or S at this point
        play_round(state, choice)
        print("Let's play again")
        choice = get_menu_choice(next_prompt)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        # Fail somewhat gracefully instead of dumping a raw stack trace
        print("An unexpected error occurred. The game will exit now.")
        print(f"Error details: {exc}")
