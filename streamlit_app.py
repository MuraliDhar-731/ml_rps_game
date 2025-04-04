import streamlit as st
import pandas as pd
import os
from train import train_model
from predictor import get_computer_move

# Session state initialization
if "history" not in st.session_state:
    st.session_state.history = []
if "score" not in st.session_state:
    st.session_state.score = {"player": 0, "computer": 0, "ties": 0, "rounds": 0}
if "last_move" not in st.session_state:
    st.session_state.last_move = "rock"
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# Game logic
moves = ["rock", "paper", "scissors"]
emojis = {"rock": "✊", "paper": "✋", "scissors": "✌️"}
beats = {"rock": "paper", "paper": "scissors", "scissors": "rock"}

# Layout
st.title("🧠 Rock, Paper, Scissors - ML Powered 🎮")

if not st.session_state.game_over:
    user_move = st.radio("Choose your move:", moves, horizontal=True)
    if st.button("Play Round"):
        prev_move = st.session_state.last_move
        st.session_state.history.append([prev_move, user_move])
        st.session_state.last_move = user_move

        train_model(st.session_state.history)
        comp_move = get_computer_move(st.session_state.history)

        st.write(f"🤖 **Computer plays:** {comp_move} {emojis[comp_move]}")

        st.session_state.score["rounds"] += 1
        if comp_move == user_move:
            st.session_state.score["ties"] += 1
            st.success("It's a tie!")
        elif beats[user_move] == comp_move:
            st.session_state.score["player"] += 1
            st.success("You win! 🎉")
        else:
            st.session_state.score["computer"] += 1
            st.error("Computer wins! 🤖")

        # Scoreboard
        st.subheader("📊 Scoreboard")
        st.write(f"**Player:** {st.session_state.score['player']}")
        st.write(f"**Computer:** {st.session_state.score['computer']}")
        st.write(f"**Ties:** {st.session_state.score['ties']}")
        st.write(f"**Rounds:** {st.session_state.score['rounds']}")

    if st.button("Quit Game"):
        st.session_state.game_over = True
        st.write("👋 Game Over. Thanks for playing!")

else:
    st.header("🚪 Game Ended")
    st.write("You chose to quit. Final scores:")
    st.write(st.session_state.score)
    if st.button("Play Again"):
        st.session_state.history = []
        st.session_state.score = {"player": 0, "computer": 0, "ties": 0, "rounds": 0}
        st.session_state.last_move = "rock"
        st.session_state.game_over = False