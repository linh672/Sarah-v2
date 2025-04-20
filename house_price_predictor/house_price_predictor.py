import joblib
from word2number import w2n
import pandas as pd

# Load the trained pipeline (includes preprocessing and model)
model_pipeline = joblib.load('house_price_predictor\house_price_pipeline_01.pkl')

# Define the features dictionary
user_inputs = {
    'longitude': None,
    'latitude': None,
    'housing_median_age': None,
    'total_rooms': None,
    'total_bedrooms': None,
    'population': None,
    'households': None,
    'median_income': None,
    'ocean_proximity': None  # Will be string like 'INLAND', 'NEAR BAY', etc.
}

# Map spoken variations for ocean_proximity
OCEAN_PROXIMITY_MAP = {
    'inland': 'INLAND',
    'in land': 'INLAND',
    'near bay': 'NEAR BAY',
    'near the bay': 'NEAR BAY',
    'ne bay': 'NEAR BAY',
    'island': 'ISLAND',
    'near ocean': 'NEAR OCEAN',
    'near the ocean': 'NEAR OCEAN',
    '<1h ocean': '<1H OCEAN',
    'less than one hour to ocean': '<1H OCEAN',
    'less than 1 hour to ocean': '<1H OCEAN',
    'one hour to ocean': '<1H OCEAN',
    'under an hour to ocean': '<1H OCEAN',
}

def make_prediction(user_input):
    global user_inputs

    # Start prediction mode
    if 'predict house price' in user_input.lower():
        return "Great! Let's begin. What is the longitude?"
    
    user_input = user_input.lower()

    # Collect features from user
    for key in user_inputs:
        if f"change {key.replace('_', ' ')}" in user_input:
            user_inputs[key] = None
            return f"Okay, please tell me the value again for {key.replace('_', ' ')}."

    if any(value is None for value in user_inputs.values()):
        try:
            user_input = user_input.replace(',', '')

            for key in user_inputs:
                if user_inputs[key] is None:
                    if key == 'ocean_proximity':
                        ocean_input = user_input.strip().lower()
                        mapped_value = OCEAN_PROXIMITY_MAP.get(ocean_input, ocean_input.upper())
                        user_inputs[key] = mapped_value
                        return f"Set {key.replace('_', ' ')} to {mapped_value}"
                    else:
                        number = w2n.word_to_num(user_input)
                        user_inputs[key] = number
                        return f"Set {key.replace('_', ' ')} to {number}"
        except ValueError:
            return "I expected a number. Please try again."

    # If all inputs are collected, make prediction
    if all(value is not None for value in user_inputs.values()):
        user_inputs['bedroom_ratio'] = user_inputs['total_bedrooms'] / user_inputs['total_rooms']
        user_inputs['households_rooms'] = user_inputs['total_rooms'] / user_inputs['households']

        input_df = pd.DataFrame([{
            'longitude': user_inputs['longitude'],
            'latitude': user_inputs['latitude'],
            'housing_median_age': user_inputs['housing_median_age'],
            'total_rooms': user_inputs['total_rooms'],
            'total_bedrooms': user_inputs['total_bedrooms'],
            'population': user_inputs['population'],
            'households': user_inputs['households'],
            'median_income': user_inputs['median_income'],
            'bedroom_ratio': user_inputs['bedroom_ratio'],
            'households_rooms': user_inputs['households_rooms'],
            'ocean_proximity': user_inputs['ocean_proximity']
        }])

        predicted_price = model_pipeline.predict(input_df)[0]
        user_inputs = {key: None for key in user_inputs}  # Reset after prediction
        return f"Based on your inputs, the predicted house price is ${predicted_price:,.2f}"

    # If not all inputs are filled, ask for the next one
    for key in user_inputs:
        if user_inputs[key] is None:
            return f"What is the value for {key.replace('_', ' ')}?"
