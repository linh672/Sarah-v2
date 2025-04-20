import speech_recognition as sr

def recognize_speech():
    #Speech recognition
    r = sr.Recognizer()
    with sr.Microphone() as user:
        print("Listening...")
        audio = r.listen(user)
    try:
        recognized_text = r.recognize_google(audio)
    except sr.UnknownValueError:
        print("")
    except sr.RequestError as e:
        recognized_text = "Sarah could not request results from server, please try again"
    return recognized_text