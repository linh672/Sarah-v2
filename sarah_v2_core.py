#import neccessary librabries
import asyncio
import pyjokes
import joblib
from word2number import w2n
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sarah_module.speech_to_text import recognize_speech
from sarah_module.text_to_speech import speak_response
from sarah_module.basic_module import get_local_time ,get_weather

#Load the trained pipeline (includes preprocessing and model)
#house price prediction Model
house_price_model = joblib.load('house_price_predictor\_house_price_model_xgbregressor.pkl')

#flight delay model and its label encoder
flight_delay_model = joblib.load('flight_delay_predictor\_flight_delay_model.pkl')
label_encoder = joblib.load('flight_delay_predictor\label_encoder.pkl')

# Define the features dictionary
house_price_user_input = {
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

flight_delay_user_input = {
    'year': None,
    'month': None,
    'day': None,
    'day_of_week': None,
    'airline': None,
    'scheduled_departure': None,
    'scheduled_arrival': None,
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

airline_name_to_code = {
    'united airlines': 'UA',
    'american airlines': 'AA',
    'us airways': 'US',
    'frontier airlines': 'F9',
    'jetblue airways': 'B6',
    'skywest airlines': 'OO',
    'alaska airlines': 'AS',
    'spirit air lines': 'NK',
    'southwest airlines': 'WN',
    'delta air lines': 'DL',
    'atlantic southeast airlines': 'EV',
    'hawaiian airlines': 'HA',
    'american eagle airlines': 'MQ',
    'virgin america': 'VX'
}

house_price_predict_mode = False
flight_delay_predict_mode = False

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
        house_price_predict_mode = True
        speak_response("Great! Let's begin. What is the longitude?")

    elif house_price_predict_mode:
        user_input = user_input.lower()
        for key in house_price_user_input:
            if f"change {key.replace('_', ' ')}" in user_input:
                house_price_user_input[key] = None
                speak_response(f"Okay, please tell me the value again for {key.replace('_', ' ')}.")
                break
        else:
            if any(value is None for value in house_price_user_input.values()):
                try:
                    user_input = user_input.replace(',', '')

                    for key in house_price_user_input:
                        if house_price_user_input[key] is None:
                            if key == 'ocean_proximity':
                                ocean_input = user_input.strip().lower()
                                mapped_value = OCEAN_PROXIMITY_MAP.get(ocean_input, ocean_input.upper())                                
                                house_price_user_input[key] = mapped_value
                                speak_response(f"Set {key.replace('_', ' ')} to {user_input.upper()}")
                            else:
                                number = w2n.word_to_num(user_input)
                                house_price_user_input[key] = number
                                speak_response(f"Set {key.replace('_', ' ')} to {number}")
                            break
                except ValueError:
                    speak_response("I expected a number. Please try again.")

            for key in house_price_user_input:
                if house_price_user_input[key] is None:
                    speak_response(f"What is the value for {key.replace('_', ' ')}?")
                    break
            else:
                # Compute derived features
                house_price_user_input['bedroom_ratio'] = house_price_user_input['total_bedrooms'] / house_price_user_input['total_rooms']
                house_price_user_input['households_rooms'] = house_price_user_input['total_rooms'] / house_price_user_input['households']

                # Create DataFrame
                input_df = pd.DataFrame([{
                    'longitude': house_price_user_input['longitude'],
                    'latitude': house_price_user_input['latitude'],
                    'housing_median_age': house_price_user_input['housing_median_age'],
                    'total_rooms': house_price_user_input['total_rooms'],
                    'total_bedrooms': house_price_user_input['total_bedrooms'],
                    'population': house_price_user_input['population'],
                    'households': house_price_user_input['households'],
                    'median_income': house_price_user_input['median_income'],
                    'bedroom_ratio': house_price_user_input['bedroom_ratio'],
                    'households_rooms': house_price_user_input['households_rooms'],
                    'ocean_proximity': house_price_user_input['ocean_proximity']
                }])

                # Predict
                predicted_price = house_price_model.predict(input_df)[0]
                print(f"The predicted house price is ${predicted_price:,.2f}")
                speak_response(f"Based on your inputs, the predicted house price is ${predicted_price:,.2f}")

                # Reset
                house_price_user_input = {key: None for key in house_price_user_input}
                house_price_predict_mode = False

    elif 'a flight will be delayed' in user_input.lower():
        speak_response("To predict if a flight will be delayed or not, say 'predict flight delay', then I will ask you for each feature one by one.")

    elif 'predict flight delay' in user_input.lower():
        flight_delay_predict_mode = True
        speak_response("Great! Let's begin. What is the year?")

    elif flight_delay_predict_mode:
        user_input = user_input.lower()
        for key in flight_delay_user_input:
            if f"change {key.replace('_', ' ')}" in user_input:
                flight_delay_user_input[key] = None
                speak_response(f"Okay, please tell me the value again for {key.replace('_', ' ')}.")
                break
        else:
            if any(value is None for value in flight_delay_user_input.values()):
                try:
                    user_input = user_input.replace(',', '')

                    for key in flight_delay_user_input:
                        if flight_delay_user_input[key] is None:
                            if key == 'airline':
                                airline_input = user_input.strip().lower()
                                code_value = airline_name_to_code.get(airline_input, airline_input.upper())                                
                                flight_delay_user_input[key] = code_value
                                speak_response(f"Set {key.replace('_', ' ')} to {user_input.upper()}")
                            else:
                                number = w2n.word_to_num(user_input)
                                flight_delay_user_input[key] = number
                                speak_response(f"Set {key.replace('_', ' ')} to {number}")
                            break
                except ValueError:
                    speak_response("I expected a number. Please try again.")

            for key in flight_delay_user_input:
                if flight_delay_user_input[key] is None:
                    speak_response(f"What is the value for {key.replace('_', ' ')}?")
                    break
            else:
                # Create DataFrame
                input_df = pd.DataFrame([{
                    'YEAR': flight_delay_user_input['year'],
                    'MONTH': flight_delay_user_input['month'],
                    'DAY': flight_delay_user_input['day'],
                    'DAY_OF_WEEK': flight_delay_user_input['day_of_week'],
                    'AIRLINE': flight_delay_user_input['airline'],
                    'SCHEDULED_DEPARTURE': flight_delay_user_input['scheduled_departure'],
                    'SCHEDULED_ARRIVAL': flight_delay_user_input['scheduled_arrival'],
                }])

                # Predict
                predicted_result_encoded = flight_delay_model.predict(input_df)[0]
                predicted_result_label = label_encoder.inverse_transform([predicted_result_encoded])[0]
                print(f"The predicted result is {predicted_result_label.replace('_', ' ').lower()}")
                speak_response(f"Based on your inputs, the predicted result is {predicted_result_label.replace('_', ' ').lower()}")

                # Reset
                flight_delay_user_input = {key: None for key in flight_delay_user_input}
                flight_delay_predict_mode = False

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



