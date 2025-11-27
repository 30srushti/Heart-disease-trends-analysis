# AI Coding Agent Instructions - Heart Disease Prediction

## Project Overview
Full-stack ML prediction application: React frontend communicates with Flask backend API that loads a pre-trained scikit-learn Decision Tree model from pickle to predict heart disease risk. The model expects exactly 12 features and returns binary prediction (0=low risk, 1=high risk) with probability scores.

## Architecture & Data Flow
- **Frontend** (`app.js`, `components/`): React with React Router for navigation
  - 3-page flow: HomePage → InputPage (form collection) → ResultPage (display prediction)
  - InputPage converts form dropdowns/inputs to the exact feature order expected by backend
- **Backend** (`app.py`): Flask with CORS enabled for localhost:3000
  - Single prediction endpoint: `POST /api/predict` accepts JSON with 12-element features array
  - Heavy categorical-to-numeric conversion: Sex ('M'/'F'→0/1), ChestPainType (mapped), RestingECG (mapped), ExerciseAngina ('Y'/'N'→1/0), ST_Slope (mapped)
  - Loads pre-trained pipeline from `models/heart_disease_pipeline_model.pkl`
- **Model**: Decision Tree in sklearn Pipeline (includes preprocessing). Accepts DataFrame with column names: `['Age', 'Sex', 'ChestPainType', 'RestingBP', 'Cholesterol', 'FastingBS', 'RestingECG', 'MaxHR', 'ExerciseAngina', 'Oldpeak', 'ST_Slope', 'zscore_chol']`

## Critical Integration Pattern: Feature Encoding
**THE HARDCODED FEATURE ORDER MUST BE MAINTAINED ACROSS ALL FILES:**
1. Age (numeric)
2. Sex (0=F, 1=M) - **frontend uses 'M'/'F' string, backend converts**
3. ChestPainType (0=ASY, 1=NAP, 2=TA, 3=ATA) - string indices mapping in backend
4. RestingBP (numeric)
5. Cholesterol (numeric)
6. FastingBS (0 or 1)
7. RestingECG (0=Normal, 1=ST, 2=LVH) - string indices mapping
8. MaxHR (numeric)
9. ExerciseAngina (0=N, 1=Y) - **note: frontend uses 'N'/'Y', maps to indices 0/1 before sending**
10. Oldpeak (numeric)
11. ST_Slope (0=Up, 1=Flat, 2=Down) - string indices mapping
12. zscore_chol (numeric - pre-computed normalization)

See `components/inputpage.js` lines 28-44 and `app.py` lines 33-78 for exact conversion logic. **All new features must match these mappings exactly.**

## Common Workflows

### Running the Application
1. **Backend**: `python app.py` (runs on http://localhost:5000)
2. **Frontend**: `npm start` (runs on http://localhost:3000, configured in package.json)
3. The frontend CORS is hardcoded to accept only `http://localhost:3000`; changing port requires updating `app.py` line 10

### Testing Predictions
- `test_prediction.py`: Standalone test script for model verification (uses hardcoded inputs)
- Example: `python test_prediction.py` validates model loading and prediction without web server
- Uses same feature columns and categorical mappings as backend

### Updating the Model
- Replace pickle file at `models/heart_disease_pipeline_model.pkl`
- No code changes needed if features remain identical
- If feature count/order changes, update line 10 in `app.py` and feature conversion logic (lines 33-78, 88)

## Project-Specific Conventions

### Error Handling Pattern
- **Backend** logs all errors with `logging.error()` and returns JSON with error message
- **Frontend** displays user-friendly alerts via `window.alert()` and logs to console
- Form validation happens client-side first (NaN checks, -1 for missing enum mappings)

### Files Not to Break
- `models/` directory: model file must be loadable via pickle at hardcoded path (uses absolute Windows path, may need adjustment if moved)
- `data/`: dataset files used for model training (reference only, not loaded at runtime)
- Column order in DataFrame construction (`app.py` line 88) is critical - must match model's training feature order

## Component Responsibility
- **homepage.js**: Landing page (examine for styling/copy only)
- **inputpage.js**: Form with 12 inputs matching feature list above; handles enum-to-index conversion before API call
- **resultpage.js**: Displays `result.prediction` (0 or 1) and `result.probability` array (probabilities for each class)

## Development Tips
- CORS errors: verify frontend port is 3000 and backend is configured for it
- Feature mismatch errors: cross-reference the 12-element order in `inputpage.js`, `app.py`, and model training
- Model loading fails: verify pickle file exists and Python pickle version matches model's serialization version
- Debug with `test_prediction.py` to isolate frontend vs. backend issues
