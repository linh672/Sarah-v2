import joblib
import pyttsx3
import speech_recognition as sr
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

predict_mode = False

# Function to speak back
def speak_response(response):
    sarah = pyttsx3.init()
    voices = sarah.getProperty('voices')
    sarah.setProperty('voice', voices[1].id)
    sarah.say(response)
    sarah.runAndWait()

# Start loop
while True:
    r = sr.Recognizer()
    with sr.Microphone() as user:
        print("Listening...")
        audio = r.listen(user)
    
    try:
        recognized_text = r.recognize_google(audio)
    except sr.UnknownValueError:
        recognized_text = "Sorry, I didn't catch that. Can you please repeat?"
    except sr.RequestError:
        recognized_text = "Sarah could not request results from server, please try again"
    
    print(f"Recognized text: {recognized_text}")

    if recognized_text.lower() == 'wake up sarah':
        speak_response("Hi, what a good sleep, how can I help you?")

    elif 'how to predict house price' in recognized_text.lower():
        speak_response("To predict house price, say 'predict house price', then I will ask you for each feature one by one.")

    elif 'predict house price' in recognized_text.lower():
        predict_mode = True
        speak_response("Great! Let's begin. What is the longitude?")

    elif predict_mode:
        recognized_text = recognized_text.lower()

        for key in user_inputs:
            if f"change {key.replace('_', ' ')}" in recognized_text:
                user_inputs[key] = None
                speak_response(f"Okay, please tell me the value again for {key.replace('_', ' ')}.")
                break
        else:
            if any(value is None for value in user_inputs.values()):
                try:
                    recognized_text = recognized_text.replace(',', '')

                    for key in user_inputs:
                        if user_inputs[key] is None:
                            if key == 'ocean_proximity':
                                user_inputs[key] = recognized_text.upper()
                                speak_response(f"Set {key.replace('_', ' ')} to {recognized_text.upper()}")
                            else:
                                number = w2n.word_to_num(recognized_text)
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
                speak_response(f"Based on your inputs, the predicted house price is ${predicted_price:,.2f}")

                # Reset
                user_inputs = {key: None for key in user_inputs}
                predict_mode = False

    elif 'goodbye' in recognized_text:
        speak_response("Goodbye, have a nice day!")
        break
