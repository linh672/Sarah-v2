#import neccessary librabries
import asyncio
import pyjokes
from sarah_module.speech_to_text import recognize_speech
from sarah_module.text_to_speech import speak_response
from sarah_module.basic_module import get_local_time ,get_weather
from house_price_predictor.house_price_predictor import make_prediction 

while True:
    #transform speech recognition to user input
    user_input = recognize_speech()
    print(f"Recognized text: {user_input}")
    #sarah_brain
    if user_input  == ('wake up Sarah' or 'hi Sarah' or 'hello Sarah'):
        speak_response ('hi, what a good sleep, how can I help you?')
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
    elif 'how to predict the house price' in user_input.lower():
        speak_response("To predict house price, say 'predict house price', then I will ask you for each feature one by one.")
    elif 'predict the house price' in user_input.lower():
        # Call the house price prediction function from the module
        response = make_prediction(user_input)
        speak_response(response)
    else:
        speak_response(f"Sarah don't understand{user_input}, can you say again")



