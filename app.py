import pandas as pd
import joblib

model = joblib.load("titanic_model.pkl")
scaler = joblib.load("titanic_scaler.pkl")

data = [[3, 25, 0, 0, 8, 1, 1, 1, 0, 0, 0, 1]]

data = scaler.transform(data)

prediction = model.predict(data)

if prediction[0] == 1:
    print("Passenger Survived")
else:
    print("Passenger Did not Survive")