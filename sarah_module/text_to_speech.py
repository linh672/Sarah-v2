
import pyttsx3

#Text to speech
def speak_response(sarah_response):
    sarah = pyttsx3.init()
    voices = sarah.getProperty('voices')
    sarah.setProperty('voice', voices[1].id)
    sarah.say(sarah_response)
    sarah.runAndWait()
