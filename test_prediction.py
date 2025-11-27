import pickle
import numpy as np
import pandas as pd

# Path to your model file
model_path = r'C:\Users\Shrusti\Downloads\Heart-disease-trends-analysis--main\Heart-disease-trends-analysis--main\models\heart_disease_pipeline_model.pkl'

# Hardcoded input features (adjust based on your model's expected inputs)
# Ensure this matches the model's expected feature order and type
input_features = [45, 'M', 'ASY', 120, 200, 0, 'Normal', 150, 'N', 1.2, 'Up', 1.5]

# Column names should match the model's expected feature names
columns = ['Age', 'Sex', 'ChestPainType', 'RestingBP', 'Cholesterol', 'FastingBS', 'RestingECG', 'MaxHR', 'ExerciseAngina', 'Oldpeak', 'ST_Slope', 'zscore_chol']

def load_model(model_path):
    """Load the trained model from a pickle file."""
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    return model

def make_prediction(model, features):
    """Use the model to make a prediction."""
    # Convert the input features to a DataFrame
    features_df = pd.DataFrame([features], columns=columns)
    
    # Ensure the model receives the DataFrame in the correct format
    prediction = model.predict(features_df)
    return prediction[0]

if __name__ == "__main__":
    try:
        # Load the model
        model = load_model(model_path)
        
        # Make a prediction
        prediction = make_prediction(model, input_features)
        
        print(f"Prediction: {prediction}")
    except Exception as e:
        print(f"An error occurred: {e}")
