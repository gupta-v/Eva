import speech_recognition as sr
import win32com.client
import webbrowser
import subprocess
import datetime
import google.generativeai as genai
import random
import os
import pyttsx3
import path
from dotenv import load_dotenv 

load_dotenv()
# Eva's pre-context
EVA_CONTEXT = """
You are Eva, an advanced AI desktop assistant. Your primary function is to assist and interact with your user, 
whom you should address as "Sir" or "Master". You are helpful, respectful, and always eager to assist. 
Your responses should be concise yet informative, and you should always maintain a polite and professional demeanor.
"""

Chatstr = ""

chat_session = None

def configure_genai():
    global chat_session
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
    }
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro-002",
        generation_config=generation_config,
    )
    
    chat_session = model.start_chat(history=[])
    chat_session.send_message(EVA_CONTEXT)

def aichat(query):
    global Chatstr, chat_session
    print(Chatstr)
    
    if chat_session is None:
        configure_genai()
    
    Chatstr += f"Master: {query}\nEva: "
    response = chat_session.send_message(query)
    result = response.text
    print(result, flush=True)
    say(result)
    Chatstr += f"{result}\n"
    return result

def AI(prompt):
    global chat_session
    if chat_session is None:
        configure_genai()
    
    text = f"AI response for Prompt: {prompt}\n\n{'*' * 75}\n\n"
    response = chat_session.send_message(prompt)
    result = response.text
    text += result

    if not os.path.exists('AI_Responses'):
        os.mkdir("AI_Responses")

    with open(f"AI_Responses/{' '.join(prompt.split('intelligence')[1:]).strip()}.txt", 'w') as f:
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
            print("Listening...", flush=True)
            audio = r.listen(source)  
            try:
                print("Recognizing...", flush=True)
                query = r.recognize_google(audio, language="en-in")
                return query
                
            except sr.UnknownValueError:
                print("Sorry, I couldn't understand what you said.", flush=True)
                continue
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}", flush=True)
                continue




if __name__ == '__main__':
    print('Eva at your service Sir...', flush=True)
    say("Eva at your service sir")
    while True:
        print("listening.....", flush=True)
        query = takeCommand()
        print(query, flush=True)

        sites = [["Youtube", "https://youtube.com"], ["Google", "https://google.com"],
                 ["Wikipedia", "https://wikipedia.com"],["GPT","https://chat.openai.com"],
                 ["CLM","https://claude.ai"],["LinkedIN","https://www.linkedin.com"],
                 ["Internshala","https://internshala.com"],["GitHub","https://github.com/"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                print(f"Opening {site[0]} sir ..", flush=True)
                say(f"Opening {site[0]} sir ..")
                webbrowser.open(site[1])

        if "Eva quit".lower() in query.lower():
            print("signing off for today,have a nice day sir...", flush=True)
            say("signing off for today         Have a nice day sir...")
            exit()

        elif "Play Music".lower() in query.lower():
            musicPath = "C:/Users/Lenovo/Music/mr_steal_ur_girl.mp3"
            print("Playing Music", flush=True)
            say("Playing Music")
            subprocess.call(["start", musicPath], shell=True)

        elif "Open Spotify".lower() in query.lower():
            pathToSpotify=path.PATH_TO_SPOTIFY
            print("Opening Spotify Sir...", flush=True)
            say("Opening Spotify Sir...")
            subprocess.Popen(pathToSpotify)
            
        elif "Open Opera GX".lower() in query.lower():
            pathToOperaGx=path.PATH_TO_OPERA_GX
            print("Opening Opera GX sir..", flush=True)
            say("Opening Opera GX sir..")
            subprocess.Popen(pathToOperaGx)
            
        elif "Open Brave".lower() in query.lower():
            pathToBrave=path.PATH_TO_BRAVE
            print("Opening Brave sir..", flush=True)
            say("Opening Brave sir..")
            subprocess.Popen(pathToBrave)
            
        elif "Open Thorium".lower() in query.lower():
            pathToThorium=path.PATH_TO_THORIUM
            print("Opening Thorium sir..", flush=True)
            say("Opening Thorium sir..")
            subprocess.Popen(pathToThorium)
            
        elif "Open Firefox".lower() in query.lower():
            pathToFirefox=path.PATH_TO_FIREFOX
            print("Opening Firefox sir..", flush=True)
            say("Opening Firefox sir..")
            subprocess.Popen(pathToFirefox)
            
        elif "Open Edge".lower() in query.lower():
            pathToEdge=path.PATH_TO_EDGE
            print("Opening Edge sir..", flush=True)
            say("Opening Edge sir..")
            subprocess.Popen(pathToEdge)

            
        elif "Open Whatsapp".lower() in query.lower():
             print("Opening Whatsapp Sir...", flush=True)
             say("Opening Whatsapp Sir...")
             os.startfile("whatsapp://")
             
        elif "Open Telegram".lower() in query.lower():
             print("Opening Telegram Sir...", flush=True)
             say("Opening Telegram Sir...")
             os.startfile("tg://")
            
        elif "Open Steam".lower() in query.lower():
            pathToSteam=path.PATH_TO_STEAM
            print("Opening Steam Sir...", flush=True)
            say("Opening Steam Sir...")
            subprocess.Popen(pathToSteam)
            
        elif "Open Riot Client".lower() in query.lower():
            pathToRiot=path.PATH_TO_RIOT
            print("Opening Riot Client Sir...", flush=True)
            say("Opening Riot Client Sir...")
            subprocess.Popen(pathToRiot)
            
        elif "Open Razer Cortex".lower() in query.lower():
            pathToRazerCortex=path.PATH_TO_RAZER_CORTEX
            print("Opening Razer Cortex Sir...", flush=True)
            say("Opening Razer Cortex Sir...")
            subprocess.Popen(pathToRazerCortex)
            
        elif "Open Razer Synapse".lower() in query.lower():
            pathToRazerSynapse=path.PATH_TO_RAZER_SYNAPSE
            print("Opening Razer Synapse Sir...", flush=True)
            say("Opening Razer Synapse Sir...")
            subprocess.Popen(pathToRazerSynapse)
            
        
        elif "the time".lower() in query.lower():
            strf=datetime.datetime.now().strftime("%H:%M:%S")
            print(f"The time is {strf}" , flush=True)
            say("The time is ")
            say(strf)

        elif "Using Artificial Intelligence".lower() in query.lower():
            AI(prompt=query)
            title=(' '.join(query.split('intelligence')[1:]).strip())
            print(f"You can view the AI response for {title} generated by me in the AI_Responses.",flush=True)
            say(f"You can view the AI response for {title}")
            say("generated by me in the AI_Responses.")

        elif "reset chat".lower() in query.lower():
            Chatstr=""

        elif "answer me".lower() in query.lower():
            print("Chatting..\n", flush=True)
            aichat(query)
            
        elif "Web Search".lower() in query.lower():
            if "web search for" in query.lower():
                search_query = query.lower().replace("web search for", "").strip()
            elif "web search" in query.lower(): 
                search_query = query.lower().replace("web search", "").strip()

            search_url = f"https://www.google.com/search?q={search_query}"
            webbrowser.open(search_url)
            print("Searching on the web for:", search_query, flush=True)
            say(f"Searching on the web for:{search_query}" )
            
        elif "Search on web".lower() in query.lower():
            if "search on web for" in query.lower():
                search_query = query.lower().replace("search on web for", "").strip()
            elif "search on web" in query.lower(): 
                search_query = query.lower().replace("search on web", "").strip()

            search_url = f"https://www.google.com/search?q={search_query}"
            webbrowser.open(search_url)
            print("Searching on the web for:", search_query, flush=True)
            say(f"Searching on the web for:{search_query}" )
            
        elif "clear terminal".lower() in query.lower():
            say("Clearing terminal sir...")
            print("Clearing terminal sir...", flush=True)
            if os.name == 'nt':  # For Windows
                os.system('cls')
            else:  # For Linux and MacOS
                os.system('clear')










