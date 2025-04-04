import pandas as pd
from train import train_model

df = pd.read_csv("move_history.csv")
history = df.values.tolist()

model, encoder = train_model(history)

if model:
    print("✅ Model trained successfully using sample data!")
else:
    print("⚠️ Not enough data to train the model.")