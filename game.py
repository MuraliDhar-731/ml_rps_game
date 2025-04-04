import os
import random
import pandas as pd
from train import train_model
from predictor import get_computer_move
from colorama import Fore, init
import threading
import time
import sys

init(autoreset=True)

moves = ["rock", "paper", "scissors"]
emojis = {"rock": "✊", "paper": "✋", "scissors": "✌️"}
beats = {"rock": "paper", "paper": "scissors", "scissors": "rock"}
history = []

score = {
    "player": 0,
    "computer": 0,
    "ties": 0,
    "rounds": 0
}

timeout_streak = 0
user_input = None

def print_banner():
    print(Fore.CYAN + "="*50)
    print(Fore.YELLOW + "  🧠 ML Rock, Paper, Scissors Game 🎮")
    print(Fore.CYAN + "="*50)

def show_scoreboard():
    print(Fore.MAGENTA + f"\n🔢 Scoreboard:")
    print(Fore.LIGHTGREEN_EX + f"Player: {score['player']} | Computer: {score['computer']} | Ties: {score['ties']} | Rounds: {score['rounds']}")

def timed_input_with_countdown(prompt, timeout=60):
    def get_input():
        global user_input
        user_input = input(prompt)

    def countdown():
        for i in range(timeout, 0, -1):
            sys.stdout.write(Fore.LIGHTCYAN_EX + f"⏳ Time left: {i:2d} sec   \r")
            sys.stdout.flush()
            time.sleep(1)
        # Clear countdown line
        sys.stdout.write(" " * 40 + "\r")
        sys.stdout.flush()

    global user_input
    user_input = None

    input_thread = threading.Thread(target=get_input)
    timer_thread = threading.Thread(target=countdown)

    input_thread.daemon = True
    timer_thread.daemon = True

    input_thread.start()
    timer_thread.start()

    input_thread.join(timeout)
    if input_thread.is_alive():
        return "timeout"
    return user_input.strip().lower() if user_input else None

def play_round():
    global timeout_streak
    print()
    user = timed_input_with_countdown(Fore.GREEN + "Your move (rock/paper/scissors or quit): ", timeout=60)

    if user == "timeout":
        timeout_streak += 1
        print(Fore.RED + "\n⏰ Timeout! Skipping your move.")
        if timeout_streak >= 2:
            print(Fore.RED + "\n🚪 Two consecutive timeouts. Exiting the game.")
            return False
        return True

    timeout_streak = 0  # reset timeout count on valid input

    if user == "quit":
        return False

    if user not in moves:
        print(Fore.RED + "Invalid move. Please choose rock, paper, or scissors.")
        return True

    if history:
        history.append([history[-1][1], user])
    else:
        history.append(["rock", user])  # seed first round

    train_model(history)
    comp = get_computer_move(history)

    print(Fore.BLUE + f"Computer plays: {comp} {emojis[comp]}")

    score["rounds"] += 1

    if comp == user:
        print(Fore.LIGHTYELLOW_EX + "It's a tie!")
        score["ties"] += 1
    elif beats[user] == comp:
        print(Fore.GREEN + "You win! 🎉")
        score["player"] += 1
    else:
        print(Fore.RED + "Computer wins! 🤖")
        score["computer"] += 1

    show_scoreboard()
    return True

if __name__ == "__main__":
    print_banner()
    while play_round():
        pass
    print(Fore.MAGENTA + "\nThanks for playing! Final Scores:")
    show_scoreboard()