from django.db import models
import joblib

#loads the trained model when an instance of the class is created
class FootballPredictor:
    def __init__(self):
        self.model = joblib.load('Model/random_forest_model.pkl')
            
    #method to make the predictions
    def predict_outcome(self, team_performance):
        prediction = self.model.predict([team_performance])
        return prediction