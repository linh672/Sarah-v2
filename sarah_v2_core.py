#import neccessary librabries
import asyncio
import pyjokes
import joblib
from word2number import w2n
import pandas as pd
from sarah_module.speech_to_text import recognize_speech
from sarah_module.text_to_speech import speak_response
from sarah_module.basic_module import get_local_time ,get_weather



# Load the trained pipeline (includes preprocessing and model)
model_pipeline = joblib.load('house_price_predictor\house_price_model_xgbregressor.pkl')

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

predict_mode = False


while True:
    #transform speech recognition to user input
    user_input = recognize_speech()
    print(f"Recognized text: {user_input}")
    #sarah_brain
    if user_input  == ('wake up Sarah' or 'hi Sarah' or 'hello Sarah'):
        speak_response ('hi, what a good sleep, how can I help you?')
    elif 'how to predict house price' in user_input.lower():
        speak_response("To predict house price, say 'predict house price', then I will ask you for each feature one by one.")

    elif 'predict house price' in user_input.lower():
        predict_mode = True
        speak_response("Great! Let's begin. What is the longitude?")

    elif predict_mode:
        user_input = user_input.lower()
        for key in user_inputs:
            if f"change {key.replace('_', ' ')}" in user_input:
                user_inputs[key] = None
                speak_response(f"Okay, please tell me the value again for {key.replace('_', ' ')}.")
                break
        else:
            if any(value is None for value in user_inputs.values()):
                try:
                    user_input = user_input.replace(',', '')

                    for key in user_inputs:
                        if user_inputs[key] is None:
                            if key == 'ocean_proximity':
                                ocean_input = user_input.strip().lower()
                                mapped_value = OCEAN_PROXIMITY_MAP.get(ocean_input, ocean_input.upper())                                
                                user_inputs[key] = mapped_value
                                speak_response(f"Set {key.replace('_', ' ')} to {user_input.upper()}")
                            else:
                                number = w2n.word_to_num(user_input)
                                user_inputs[key] = number
                                speak_response(f"Set {key.replace('_', ' ')} to {number}")
                            break
                except ValueError:
                    speak_response("I expected a number. Please try again.")

            for key in user_inputs:
                if user_inputs[key] is None:
                    speak_response(f"What is the value for {key.replace('_', ' ')}?")
                    break
            else:
                # Compute derived features
                user_inputs['bedroom_ratio'] = user_inputs['total_bedrooms'] / user_inputs['total_rooms']
                user_inputs['households_rooms'] = user_inputs['total_rooms'] / user_inputs['households']

                # Create DataFrame
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

                # Predict
                predicted_price = model_pipeline.predict(input_df)[0]
                print(f"The predicted house price is ${predicted_price:,.2f}")
                speak_response(f"Based on your inputs, the predicted house price is ${predicted_price:,.2f}")

                # Reset
                user_inputs = {key: None for key in user_inputs}
                predict_mode = False
    elif 'time' in user_input or 'date' in user_input:
        if 'in' in user_input:
            city = user_input.split('in')[-1].strip()
            try:
                time, date_today = get_local_time(city)
                if 'time' in user_input:
                    speak_response(f"The current time in {city} is {time}")
                elif 'date' in user_input:
                    speak_response (f"Today in {city} is {date_today}")
            except:
                speak_response("Sorry, I couldn't find that city. Please try again.")
        else:
            speak_response("Please specify a city for the time or date.")
    elif 'goodbye' in user_input:
        speak_response ('goodbye, have a nice day')
        break
    elif 'weather' in user_input:
            # Extract city name from recognized text
            if 'in' in user_input:
                city = user_input.split('in')[-1].strip()
                if city:
                    speak_response(asyncio.run(get_weather(city)))
                else:
                    speak_response("Please tell me the name of the city.")
            else:
                speak_response("Please specify a city for the weather.")
    elif 'joke' in user_input:
        speak_response(pyjokes.get_joke())
    elif 'thank you' in user_input:
        speak_response("You're welcome, I love to hear more questions")
    else:
        speak_response(f"Sarah don't understand{user_input}, can you say again")



