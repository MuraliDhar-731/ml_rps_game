import joblib
import random

moves = ["rock", "paper", "scissors"]
beats = {"rock": "paper", "paper": "scissors", "scissors": "rock"}

def get_computer_move(history):
    try:
        model, encoder = joblib.load("models/rps_model.pkl")
    except:
        return random.choice(moves)

    if not history:
        return random.choice(moves)

    last_move = history[-1][1]
    try:
        encoded = encoder.transform([last_move])[0]
        pred = model.predict([[encoded]])[0]
        predicted_user_move = encoder.inverse_transform([pred])[0]
        return beats[predicted_user_move]
    except:
        return random.choice(moves)