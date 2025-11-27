from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import math

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# Path to the model
model_path = r'C:\Users\Shrusti\Downloads\Heart-disease-trends-analysis--main\Heart-disease-trends-analysis--main\models\heart_disease_pipeline_model.pkl'

# Global model variable
model = None

def load_model():
    global model
    if model is None:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)

@app.route('/')
def home():
    return "Welcome to the Heart Disease Prediction API!"

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        load_model()  # Ensure model is loaded
        data = request.json
        input_features = data.get('features')

        if not input_features or not isinstance(input_features, list):
            return jsonify({'error': 'Invalid input, features data must be a list'}), 400

        # Ensure input_features is a list with the expected length
        if len(input_features) != 12:
            return jsonify({'error': f'Invalid input, features list must contain 12 elements (got {len(input_features)})'}), 400

        # Create DataFrame with expected column names
        columns = ['Age', 'Sex', 'ChestPainType', 'RestingBP', 'Cholesterol', 'FastingBS', 'RestingECG', 'MaxHR', 'ExerciseAngina', 'Oldpeak', 'ST_Slope', 'zscore_chol']
        
        # Convert numeric strings to numbers
        try:
            features_converted = []
            features_converted.append(float(input_features[0]))  # Age
            features_converted.append(input_features[1])  # Sex
            features_converted.append(input_features[2])  # ChestPainType
            features_converted.append(float(input_features[3]))  # RestingBP
            cholesterol = float(input_features[4])  # Cholesterol
            features_converted.append(cholesterol)
            features_converted.append(int(input_features[5]))  # FastingBS
            features_converted.append(input_features[6])  # RestingECG
            features_converted.append(float(input_features[7]))  # MaxHR
            features_converted.append(input_features[8])  # ExerciseAngina
            features_converted.append(float(input_features[9]))  # Oldpeak
            features_converted.append(input_features[10])  # ST_Slope
            
            # Calculate zscore_chol from cholesterol if not provided
            if input_features[11] is None or (isinstance(input_features[11], float) and math.isnan(input_features[11])) or input_features[11] == '':
                mean_cholesterol = 246.26
                std_cholesterol = 51.83
                zscore_chol = (cholesterol - mean_cholesterol) / std_cholesterol
            else:
                zscore_chol = float(input_features[11])
            
            features_converted.append(zscore_chol)
            
        except (ValueError, IndexError, TypeError) as e:
            return jsonify({'error': f"Error converting features: {str(e)}"}), 400
        
        input_df = pd.DataFrame([features_converted], columns=columns)
        
        # Check for NaN values
        if input_df.isna().any().any():
            return jsonify({'error': 'Input data contains NaN values'}), 400
        
        # Make prediction
        try:
            prediction = model.predict(input_df)
            prediction_proba = model.predict_proba(input_df)
            
            result = {
                'prediction': int(prediction[0]),
                'probability': prediction_proba[0].tolist()
            }
            
            return jsonify(result)
        except Exception as pred_error:
            return jsonify({'error': f"Prediction error: {str(pred_error)}"}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
