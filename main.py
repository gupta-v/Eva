import speech_recognition as sr
import win32com.client
import webbrowser
import subprocess
import datetime
import google.generativeai as genai
import random
import os
import pyttsx3
from dotenv import load_dotenv 

load_dotenv()

Chatstr=""
def aichat(query):
    global Chatstr
    print(Chatstr)
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    Chatstr += f"Master: {query}\nEva: "
    # Set up the model
    generation_configs = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    model = genai.GenerativeModel(model_name="gemini-1.0-pro", generation_config=generation_configs)

    prompt_parts = [query]
    response = model.generate_content(prompt_parts)
    result = response.text
    print(result)
    say(result)
    Chatstr += f"{result}\n"


def AI(prompt):
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    text = f"AI response for Prompt: {prompt}\n\n*****************************************************************************\n\n"

    # Set up the model
    generation_configs = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    model = genai.GenerativeModel(model_name="gemini-1.0-pro", generation_config=generation_configs)

    prompt_parts = [prompt]

    response = model.generate_content(prompt_parts)
    result = response.text
    # print(result)
    text += result

    if not os.path.exists('AI_H'):
        os.mkdir("AI_H")

    # with open(f"AI_H/Prompt- {random.randint(1,212837363537)}",'w') as f:
    with open(f"AI_H/{' '.join(prompt.split('intelligence')[1:]).strip()}.txt",'w') as f:
        f.write(text)




import pyttsx3

def say(text):
    engine = pyttsx3.init()

    # Use the Microsoft Speech API for more voices (Windows)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  #
# Pitch of the voice (50-200)Change index if needed

    engine.say(text)
    engine.runAndWait()

# Example usage


def takeCommand():
    r = sr.Recognizer()
    while True:
        with sr.Microphone() as source: 
            r.adjust_for_ambient_noise(source)# Adjust for ambient noise
            print("Listening...")
            audio = r.listen(source)  
            try:
                print("Recognizing...")
                query = r.recognize_google(audio, language="en-in")
                return query
                
            except sr.UnknownValueError:
                print("Sorry, I couldn't understand what you said.")
                continue
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                continue




if __name__ == '__main__':
    print('Eva at your service Sir...')
    say("Eva at your service sir")
    while True:
        print("listening.....")
        query = takeCommand()

        sites = [["Youtube", "https://youtube.com"], ["Google", "https://google.com"],
                 ["Wikipedia", "https://wikipedia.com"],["GPT","https://chat.openai.com"],
                 ["CLM","https://claude.ai"],["LinkedIN","https://www.linkedin.com"],
                 ["Internshala","https://internshala.com"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir ..")
                webbrowser.open(site[1])

        if "Eva quit".lower() in query.lower():
            print("signing off for today,have a nice day sir...")
            say("signing off for today   Have a nice day sir...")
            exit()

        elif "Play Music".lower() in query.lower():
            musicPath = "C:/Users/Lenovo/Music/Omen.mp3"
            subprocess.call(["start", musicPath], shell=True)

        elif "Open Opera GX".lower() in query.lower():
            pathToOperaGx="C:/Users/Lenovo/AppData/Local/Programs/Opera GX/launcher.exe"
            say("Opening Opera GX sir..")
            subprocess.Popen(pathToOperaGx)

        elif "Open Spotify".lower() in query.lower():
            pathToSpotify="C:/Users/Lenovo/AppData/Roaming/Spotify/Spotify.exe"
            say("Opening Spotify Sir...")
            subprocess.Popen(pathToSpotify)
            
        elif "Open Whatsapp".lower() in query.lower():
             say("Opening Whatsapp Sir...")
             os.startfile("whatsapp://")
             
        elif "Open Telegram".lower() in query.lower():
             say("Opening Telegram Sir...")
             os.startfile("tg://")

        elif "the time".lower() in query.lower():
            strf=datetime.datetime.now().strftime("%H:%M:%S")
            say(strf)

        elif "Using Artificial Intelligence".lower() in query.lower():
            AI(prompt=query)

        elif "reset chat".lower() in query.lower():
            Chatstr=""

        elif "answer me".lower() in query.lower():
            print("Chatting..\n")
            aichat(query)
            
        elif "Web Search".lower() in query.lower():
            search_query = query.lower().replace("search on web", "").strip()
            search_url = f"https://www.google.com/search?q={search_query}"
            webbrowser.open(search_url)
            print("Searching on the web for:", search_query)










