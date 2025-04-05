import streamlit as st
import pandas as pd
from train import train_model
from predictor import get_computer_move

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []
if "score" not in st.session_state:
    st.session_state.score = {"player": 0, "computer": 0, "ties": 0, "rounds": 0}
if "last_move" not in st.session_state:
    st.session_state.last_move = "rock"
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "player_name" not in st.session_state:
    st.session_state.player_name = ""
if "win_streak" not in st.session_state:
    st.session_state.win_streak = 0
if "last_result" not in st.session_state:
    st.session_state.last_result = ""

# Game setup
moves = ["rock", "paper", "scissors"]
emojis = {"rock": "✊", "paper": "✋", "scissors": "✌️"}
beats = {"paper": "rock", "scissors": "paper", "rock": "scissors"}

# UI
st.title("🧠 Rock, Paper, Scissors - ML Powered 🎮")

# Name input screen
if not st.session_state.player_name:
    name = st.text_input("Enter your name to begin:")
    if name and st.button("Start Game"):
        st.session_state.player_name = name
        st.rerun()  # ✅ works in latest Streamlit
    st.stop()

# Game End Conditions
if st.session_state.score["player"] >= 5:
    st.balloons()
    st.success(f"🏆 {st.session_state.player_name} wins the game!")
    st.session_state.game_over = True

if st.session_state.score["computer"] >= 5:
    st.error("💻 Computer wins the game! Better luck next time!")
    st.session_state.game_over = True

# Game Interface
if not st.session_state.game_over:
    st.subheader(f"Welcome, {st.session_state.player_name} 👋")
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
            st.session_state.win_streak = 0
            st.session_state.last_result = "It's a tie! 🤝"
        elif beats[user_move] == comp_move:
            st.session_state.score["player"] += 1
            st.session_state.win_streak += 1
            st.session_state.last_result = "🎉 You win!"
        else:
            st.session_state.score["computer"] += 1
            st.session_state.win_streak = 0
            st.session_state.last_result = "💻 Computer wins!"

    st.markdown(f"### {st.session_state.last_result}")
    st.write(f"🔥 **Win Streak:** {st.session_state.win_streak}")

    # Scoreboard
    st.subheader("📊 Scoreboard")
    st.write(f"**{st.session_state.player_name}:** {st.session_state.score['player']}")
    st.write(f"**Computer:** {st.session_state.score['computer']}")
    st.write(f"**Ties:** {st.session_state.score['ties']}")
    st.write(f"**Rounds Played:** {st.session_state.score['rounds']}")

    # Last 5 rounds table
    if len(st.session_state.history) > 0:
        history_df = pd.DataFrame(st.session_state.history[-5:], columns=["Previous Move", "Your Move"])
        st.subheader("🕹️ Last 5 Rounds")
        st.table(history_df)

    if st.button("Quit Game"):
        st.session_state.game_over = True
        st.write("👋 Game Over. Thanks for playing!")

# Game Over State
else:
    st.header("🚪 Game Ended")
    st.write("Final scores:")
    st.write(st.session_state.score)
    if st.button("Play Again"):
        st.session_state.history = []
        st.session_state.score = {"player": 0, "computer": 0, "ties": 0, "rounds": 0}
        st.session_state.last_move = "rock"
        st.session_state.game_over = False
        st.session_state.win_streak = 0
        st.session_state.last_result = ""
        st.rerun()  # ✅ correct call
