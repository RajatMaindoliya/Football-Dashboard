from django.db import models
import pickle

class FootballPredictor:
    def __init__(self):
        with open('Model/neural_network_model.pkl', 'rb') as f:
            self.model = pickle.load(f)
            
    def predict_outcome(self, team_performance, weather_conditions):
        prediction = self.model.predict([team_performance, weather_conditions])
        return prediction