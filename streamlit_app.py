import streamlit as st
import pandas as pd
from train import train_model
from predictor import get_computer_move
import streamlit.components.v1 as components

# Play sound using HTML audio
def play_sound(url):
    components.html(f'''
    <audio autoplay>
        <source src="{url}" type="audio/mp3">
    </audio>
    ''', height=0)

# Theme selection (dark/light mode)
theme = st.sidebar.radio("🎨 Select Theme", ["Dark Mode 🌙", "Light Mode ☀️"])

if theme == "Dark Mode 🌙":
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background-color: #121212;
            color: white;
        }
        [data-testid="stSidebar"] {
            background-color: #1E1E1E;
        }
        </style>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background-color: #FFFFFF;
            color: #000000;
        }
        [data-testid="stSidebar"] {
            background-color: #F0F2F6;
        }
        </style>
        """, unsafe_allow_html=True)

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
if "rules_shown" not in st.session_state:
    st.session_state.rules_shown = False

# Game setup
moves = ["rock", "paper", "scissors"]
emojis = {"rock": "✊", "paper": "✋", "scissors": "✌️"}
beats = {"paper": "rock", "scissors": "paper", "rock": "scissors"}

# UI title
st.markdown("<h1 style='text-align: center;'>🧠 Rock, Paper, Scissors - ML Powered 🎮</h1>", unsafe_allow_html=True)

# Popup dialog for game rules
if not st.session_state.rules_shown:
    st.info("""
    🎯 **Welcome to the ML-Powered Rock, Paper, Scissors!**

    ### Game Rules:
    - **Rock (✊)** beats **Scissors (✌️)**
    - **Scissors (✌️)** beats **Paper (✋)**
    - **Paper (✋)** beats **Rock (✊)**

    - First player to reach **5 wins** 🏆 wins the game.
    - Enter your name below to start playing!

    Good luck and have fun! 🎉
    """)
    if st.button("👍 Got it, Let's Play!"):
        st.session_state.rules_shown = True
        st.rerun()
    st.stop()

# Name input screen
if not st.session_state.player_name:
    name = st.text_input("Enter your name to begin:")
    if name and st.button("Start Game 🚀"):
        st.session_state.player_name = name
        st.rerun()
    st.stop()

# Game End Conditions
if st.session_state.score["player"] >= 5:
    st.balloons()
    st.success(f"🏆 {st.session_state.player_name} wins the game!")
    play_sound("https://www.soundjay.com/human/sounds/applause-8.mp3")
    st.session_state.game_over = True

if st.session_state.score["computer"] >= 5:
    st.error("💻 Computer wins the game! Better luck next time!")
    play_sound("https://www.soundjay.com/button/sounds/button-10.mp3")
    st.session_state.game_over = True

# Game Interface
if not st.session_state.game_over:
    st.subheader(f"Welcome, {st.session_state.player_name} 👋")
    user_move = st.radio("Choose your move:", moves, horizontal=True)

    if st.button("Play Round 🔥"):
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
            play_sound("https://www.soundjay.com/button/beep-05.mp3")
        elif beats[user_move] == comp_move:
            st.session_state.score["player"] += 1
            st.session_state.win_streak += 1
            st.session_state.last_result = "🎉 You win!"
            play_sound("https://www.soundjay.com/button/sounds/button-4.mp3")
        else:
            st.session_state.score["computer"] += 1
            st.session_state.win_streak = 0
            st.session_state.last_result = "💻 Computer wins!"
            play_sound("https://www.soundjay.com/button/sounds/button-10.mp3")

    st.markdown(f"### {st.session_state.last_result}")
    st.write(f"🔥 **Win Streak:** {st.session_state.win_streak}")

    # Reaction GIFs
    if "🎉" in st.session_state.last_result:
        st.image("https://media.giphy.com/media/3o6Zt6ML6BklcajjsA/giphy.gif", width=300)
    elif "Computer wins" in st.session_state.last_result:
        st.image("https://media.giphy.com/media/9Y5BbDSkSTiY8/giphy.gif", width=200)

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

    if st.button("Quit Game ❌"):
        st.session_state.game_over = True
        st.write("👋 Game Over. Thanks for playing!")

# Game Over State
else:
    st.header("🚪 Game Ended")
    st.write("Final scores:")
    st.write(st.session_state.score)
    if st.button("Play Again 🔄"):
        st.session_state.history = []
        st.session_state.score = {"player": 0, "computer": 0, "ties": 0, "rounds": 0}
        st.session_state.last_move = "rock"
        st.session_state.game_over = False
        st.session_state.win_streak = 0
        st.session_state.last_result = ""
        st.rerun()
