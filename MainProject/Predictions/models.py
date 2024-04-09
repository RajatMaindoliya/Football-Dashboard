from django.db import models
import joblib


class FootballPredictor:
    def __init__(self):
        self.model = joblib.load('Model/random_forest_model.pkl')
            
    def predict_outcome(self, team_performance):
        prediction = self.model.predict([team_performance])
        return prediction