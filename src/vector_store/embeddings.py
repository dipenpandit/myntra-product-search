import joblib
import os

def get_model():
    MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'model.joblib')
    model = joblib.load(os.path.abspath(MODEL_PATH))
    return model
