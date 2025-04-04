import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

def train_model(history):
    if len(history) < 5:
        return None, None
    df = pd.DataFrame(history, columns=["prev_move", "next_move"])
    encoder = LabelEncoder()
    df = df.fillna("rock")
    X = encoder.fit_transform(df["prev_move"]).reshape(-1, 1)
    y = encoder.transform(df["next_move"])
    model = DecisionTreeClassifier()
    model.fit(X, y)
    os.makedirs("models", exist_ok=True)
    joblib.dump((model, encoder), "models/rps_model.pkl")
    return model, encoder