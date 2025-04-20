import speech_recognition as sr

def recognize_speech():
    #Speech recognition
    r = sr.Recognizer()
    with sr.Microphone() as user:
        print("Listening...")
        audio = r.listen(user)
    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        return "Sarah could not request results from server, please try again"