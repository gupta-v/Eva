import os
import speech_recognition as sr
import pyttsx3

def say(text):
    engine = pyttsx3.init()

    # Use the Microsoft Speech API for more voices (Windows)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Change index if needed
    # Set the speech rate (default is usually ~200 words per minute)
    rate = engine.getProperty('rate')  # Get the current rate
    engine.setProperty('rate', rate - 10)  # Decrease the rate for slower speech

    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    while True:
        with sr.Microphone() as source: 
            r.adjust_for_ambient_noise(source)# Adjust for ambient noise
            print("\nListening...", flush=True)
            audio = r.listen(source)  
            try:
                print("\nRecognizing...", flush=True)
                query = r.recognize_google(audio, language="en-in")
                return query
                
            except sr.UnknownValueError:
                print("\nSorry, I couldn't understand what you said.", flush=True)
                continue
            except sr.RequestError as e:
                print(f"\nCould not request results from Google Speech Recognition service; {e}", flush=True)
                continue
            
