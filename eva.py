import speech_recognition as sr
import webbrowser
import subprocess
from fuzzywuzzy import process
import datetime
import google.generativeai as genai
import os
import pyttsx3
import path
from searchDir import SEARCH_DIRS
import re
import json
from dotenv import load_dotenv 

load_dotenv()

# Folder and file to store user information
INFORMATION_FOLDER = 'Information'
USER_INFO_FILE = os.path.join(INFORMATION_FOLDER, 'user_info.json')

# Eva's pre-context
def get_eva_context(user_info):
    # Dynamically create the EVA_CONTEXT based on user data
    EVA_CONTEXT = f"""
                You are Eva, an advanced AI desktop assistant. Your primary function is to assist and interact with your user, 
                whom you should address as "{user_info['preferred_name']}" or Sir or Master depending on your response. You are helpful, respectful, and always eager to assist. 
                The user's name is {user_info['name']}. They are a {user_info['profession']} and their areas of interest include:
                {', '.join(user_info['interests'])}.
                You are knowledgeable in areas like AI, Cyber Security and general computing, always eager to assist and create a positive experience.
                Your responses should be concise yet informative, and you should always maintain a polite and professional demeanor.
                """
    return EVA_CONTEXT


def get_user_info():
    # Check if the Information folder exists, if not, create it
    if not os.path.exists(INFORMATION_FOLDER):
        os.mkdir(INFORMATION_FOLDER)

    # Check if user info file exists
    if os.path.exists(USER_INFO_FILE):
        # Load existing data from the file
        with open(USER_INFO_FILE, 'r') as f:
            user_info = json.load(f)    
        return user_info
    else:
        # Ask questions to get user info for the first time
        print("\nHello! Let's get to know you better.\n", flush=True)
        name = input("What's your name? ")
        preferred_name = input("What would you like me to call you? (e.g., User, Sir, Master, Nickname) ")
        profession = input("What's your profession? (Student, Working Professional, AI Enthusiast, etc.) ")
        
        print("Please tell me your areas of interest (you can provide up to 5 interests):")
        interests = []
        for i in range(5):
            interest = input(f"Interest {i+1}: ")
            interests.append(interest)
            more = input("Do you have more interests? (y/n): ")
            if more.lower() != 'y':
                break
        
        # Save the collected information
        user_info = {
            'name': name,
            'preferred_name': preferred_name,  # Store the preferred name
            'profession': profession,
            'interests': interests
        }
        
        # Make sure the Information folder exists
        if not os.path.exists(INFORMATION_FOLDER):
            os.mkdir(INFORMATION_FOLDER)
        
        # Save the user info into the user_info.json file in the Information folder
        with open(USER_INFO_FILE, 'w') as f:
            json.dump(user_info, f, indent=4)
        
        print(f"\nThank you for providing your information, {name}!", flush=True)
        return user_info





chat_session = None


def configure_genai(user_info):
    global chat_session
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
    }
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )
    
    chat_session = model.start_chat(history=[])
    EVA_CONTEXT = get_eva_context(user_info)
    chat_session.send_message(EVA_CONTEXT)

Chatstr = ""
def aichat(query):
    global Chatstr, chat_session
    
    if chat_session is None:
        configure_genai(user_info)
    
    Chatstr += f"Master: {query}\nEva: "
    response = chat_session.send_message(query)
    result = response.text
    Chatstr += f"{result}\n"
    return result

def AI(prompt):
    global chat_session
    if chat_session is None:
        configure_genai(user_info)
    
    text = f"AI response for Prompt: {prompt}\n\n{'*' * 75}\n\n"
    response = chat_session.send_message(prompt)
    result = response.text
    text += result

    if not os.path.exists('AI_Responses'):
        os.mkdir("AI_Responses")

    with open(f"AI_Responses/{' '.join(prompt.split('intelligence')[1:]).strip()}.txt", 'w') as f:
        f.write(text)


# Directories to search for applications
search_dirs = SEARCH_DIRS

# File extensions to consider as executable
executable_exts = [".exe", ".lnk"]

# App paths dictionary (initialized at startup)
app_paths = {}


def scan_apps():
    """Retrieve installed applications."""
    apps = {}
    for directory in search_dirs:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(tuple(executable_exts)):
                    app_name = os.path.splitext(file)[0].lower()
                    apps[app_name] = os.path.join(root, file)
    return apps


def launch_app(path):
    """Launch the application."""
    try:
        subprocess.Popen(path, shell=True)
        print(f"\nLaunching application: {path}", flush=True)
    except Exception as e:
        print("\nFailed to open {path}: {e}", flush=True)


def search(query, app_paths):
    """Search for matching applications."""
    if not query:
        return []
    return process.extract(query.lower(), app_paths.keys(), limit=5)

def extract_choice(command):
    """Extract numeric or ordinal choice from a voice command."""
    # Ordinal words mapping
    ordinal_mapping = {
        "first": 1,
        "second": 2,
        "third": 3,
        "fourth": 4,
        "fifth": 5,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "none": 0,
        "none of the above": 0,  # Added support for "none of the above"
    }

    # Match ordinal words or "none"
    for word, num in ordinal_mapping.items():
        if word in command:
            return num

    # Regex to capture phrases like "option 1," "1st option," etc.
    match = re.search(r"(?:option\s|select\soption\s|^)(\d+)(?:\w*|th|st|nd|rd)?", command)
    if match:
        return int(match.group(1))

    return -1  # Invalid choice

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




def main():
    
    user_info = get_user_info()  # Get the user info (ask if first time, else load from file)
    configure_genai(user_info)   # Configure Eva with the user's info
    
    print(f"Welcome Back, {user_info['preferred_name']}!",flush=True)
    say(f"Welcome Back, {user_info['preferred_name']}!")
    
    print("\nEva at your service Sir...", flush=True)
    say("Eva at your service sir")
    
    app_paths = scan_apps()
    
    while True:
        print("\nlistening.....", flush=True)
        query = takeCommand()
        print("\n" + query, flush=True)

        sites = [
                 ["Youtube", "https://youtube.com/"], ["Instagram","https://instagram.com"],
                 ["Google", "https://google.com/"], ["Wikipedia", "https://wikipedia.com/"],
                 ["GPT","https://chat.openai.com/"], ["CLM","https://claude.ai/"],
                 ["Internshala","https://internshala.com/"], ["GitHub","https://github.com/"],
                 ["LinkedIN","https://www.linkedin.com/"]
                 ]

        for site in sites:  
            if f"Open {site[0]}".lower() in query.lower():  
                print(f"\nOpening {site[0]} sir ..", flush=True)
                say(f"Opening {site[0]} sir ..")
                webbrowser.open(site[1])
                
        if "Eva quit".lower() in query.lower() or "Eva exit".lower() in query.lower():
            print("\nsigning off for today,have a nice day sir...", flush=True)
            say("signing off for today         Have a nice day sir...")
            exit()
        
        elif "the time".lower() in query.lower():
            strf=datetime.datetime.now().strftime("%H:%M:%S")
            print(f"\nThe time is {strf}" , flush=True)
            say("The time is ")
            say(strf)
                

        elif "Play Music".lower() in query.lower():
            musicPath = "C:/Users/Lenovo/Music/mr_steal_ur_girl.mp3"
            print("\nPlaying Music", flush=True)
            say("Playing Music")
            subprocess.call(["start", musicPath], shell=True)

        elif "list noted websites".lower() in query.lower():
            print("\nHere are the noted websites sir...", flush=True)
            say("\nHere are the noted websites sir...")
            idx=1
            for site in sites:
                print(f"\n{idx}: {site[0]}",flush=True)
                say(f"{site[0]}")
                idx+=1
        
        elif "web"in query.lower() and "search" in query.lower():
            # Handle multiple possible search phrases
            if "search" in query.lower():
                search_query = query.lower().replace("web search", "").replace("web search for","").replace("search on web for", "").replace("search on the web for", "").replace("search for","").strip()
                
            # Clean up by removing any leading phrase like "Eva"
            search_query = search_query.replace("eva", "").strip()  # Optionally remove "Eva" if it exists
            search_query = search_query.lstrip()  # Strip any leading unwanted words

            if search_query:  # Ensure the search query is not empty
                print("\nSearching on the web for:", search_query, flush=True)
                say(f"Searching on the web for: {search_query}")
                search_url = f"https://www.google.com/search?q={search_query}"
                webbrowser.open(search_url)
            else:
                print("\nNo search query found!", flush=True)
                say("I couldn't find any search query. Please try again.")
        
        elif "Open Spotify".lower() in query.lower():
            pathToSpotify=path.PATH_TO_SPOTIFY
            print("\nOpening Spotify Sir...", flush=True)
            say("Opening Spotify Sir...")
            subprocess.Popen(pathToSpotify)
            
        elif "Open Opera GX".lower() in query.lower():
            pathToOperaGx=path.PATH_TO_OPERA_GX
            print("\nOpening Opera GX sir..", flush=True)
            say("Opening Opera GX sir..")
            subprocess.Popen(pathToOperaGx)
            
        elif "Open Brave".lower() in query.lower():
            pathToBrave=path.PATH_TO_BRAVE
            print("\nOpening Brave sir..", flush=True)
            say("Opening Brave sir..")
            subprocess.Popen(pathToBrave)
            
        elif "Open Thorium".lower() in query.lower():
            pathToThorium=path.PATH_TO_THORIUM
            print("\nOpening Thorium sir..", flush=True)
            say("Opening Thorium sir..")
            subprocess.Popen(pathToThorium)
            
        elif "Open Firefox".lower() in query.lower():
            pathToFirefox=path.PATH_TO_FIREFOX
            print("\nOpening Firefox sir..", flush=True)
            say("Opening Firefox sir..")
            subprocess.Popen(pathToFirefox)
            
        elif "Open Edge".lower() in query.lower():
            pathToEdge=path.PATH_TO_EDGE
            print("\nOpening Edge sir..", flush=True)
            say("Opening Edge sir..")
            subprocess.Popen(pathToEdge)

            
        elif "Open Whatsapp".lower() in query.lower():
             print("\nOpening Whatsapp Sir...", flush=True)
             say("Opening Whatsapp Sir...")
             os.startfile("whatsapp://")
             

        elif "Open Telegram".lower() in query.lower():
             print("\nOpening Telegram Sir...", flush=True)
             say("Opening Telegram Sir...")
             os.startfile("tg://")
            
        elif "Open Steam".lower() in query.lower():
            pathToSteam=path.PATH_TO_STEAM
            print("\nOpening Steam Sir...", flush=True)
            say("Opening Steam Sir...")
            subprocess.Popen(pathToSteam)
            
        elif "Open Riot Client".lower() in query.lower():
            pathToRiot=path.PATH_TO_RIOT
            print("\nOpening Riot Client Sir...", flush=True)
            say("Opening Riot Client Sir...")
            subprocess.Popen(pathToRiot)
            
        elif "Open Razer Cortex".lower() in query.lower():
            pathToRazerCortex=path.PATH_TO_RAZER_CORTEX
            print("\nOpening Razer Cortex Sir...", flush=True)
            say("Opening Razer Cortex Sir...")
            subprocess.Popen(pathToRazerCortex)
            
        elif "Open Razer Synapse".lower() in query.lower():
            pathToRazerSynapse=path.PATH_TO_RAZER_SYNAPSE
            print("\nOpening Razer Synapse Sir...", flush=True)
            say("Opening Razer Synapse Sir...")
            subprocess.Popen(pathToRazerSynapse)
            
        
        elif "open command prompt".lower() in query.lower() or "open cmd" in query.lower():
            pathToCommandPrompt=path.PATH_TO_CMD
            print("\nOpening Command Prompt Sir...", flush=True)
            say("Opening Command Prompt Sir...")
            os.startfile(pathToCommandPrompt) # Open Command Prompt
            
        elif "open Powershell".lower() in query.lower():
            pathToPowershell=path.PATH_TO_POWERSHELL
            print("\nOpening Powershell Sir...", flush=True)
            say("Opening Powershell Sir...")
            os.startfile(pathToPowershell) # Open Command Prompt

        
        elif "search and launch" in query or "find application" in query:
            app_name = query.replace("search and launch", "").replace("find application", "").strip()
            matches = search(app_name, app_paths)
            
            if matches:
                print(f"\nI found the  matches for {app_name}:",flush=True)
                say(f"I found the matches for {app_name}:")
                
                # List options for the user
                for idx, (match, score) in enumerate(matches, start=1):
                    print(f"\n{idx}. {match} (Confidence: {score}%)",flush=True)
                    say(f"Option {idx}: {match}")
                
                # Wait for user to select an option
                print("\nPlease say a choice like first option, option 2, none or none of the above to cancel.",flush=True)
                say("Please say a choice like first option, option 2, none or none of the above to cancel.")
                
                while True:
                    # Listen for user response
                    option_query = takeCommand()
                    print("\n" + option_query,flush=True)
                    choice = extract_choice(option_query)

                    # If user says "none" or "none of the above", cancel the operation
                    if "none" in option_query.lower() or "none of the above" in option_query.lower():
                        print("\nCancelled. No application will be opened.",flush=True)
                        say("Cancelled. No application will be opened.")
                        break  # Cancel the operation

                    # If the choice is valid (1, 2, 3, etc.), launch the selected app
                    elif 1 <= choice <= len(matches):
                        selected_app = matches[choice - 1][0]
                        say(f"Opening {selected_app} now.")
                        launch_app(app_paths[selected_app.lower()])
                        break  # Exit the loop once the app is opened

                    # If the user gives an invalid option, ask again
                    else:
                        print("\nInvalid choice. Please try again.",flush=True)
                        say("Invalid choice. Please try again.")
            else:
                say("No matching applications found.")

                
        elif "reset chat".lower() in query.lower():
            Chatstr=""
        
        elif "answer me".lower() in query.lower():
            print("\nChatting..\n", flush=True)
            results= aichat(query)
            print("Eva: " + results, flush=True)
            say(results)
        
        elif "Eva Listen".lower() in query.lower() or "Eva Let's Chat".lower() in query.lower():
            print("Entering chat mode, To Exit Chat Mode say Eva Quit Chat or Eva Exit Chat", flush=True)
            say("Entering chat mode..., To Exit Chat Mode")
            say("say Eva Quit Chat or Eva Exit Chat")
            while True:
                query = takeCommand()
                print(query, flush=True)
                if "Eva Quit Chat".lower() in query.lower() or "Eva Exit Chat" in query.lower():
                    print("Exiting chat mode...", flush=True)
                    say("Exiting chat mode...")
                    break
                
                elif "Using Artificial Intelligence".lower() in query.lower():
                    AI(prompt=query)
                    title=(' '.join(query.split('intelligence')[1:]).strip())
                    print(f"\nEva: You can view the AI response for {title} generated by me in the AI_Responses.",flush=True)
                    say(f"You can view the AI response for {title}")
                    say("generated by me in the AI_Responses.")
                    
                else:
                    print("\nChatting..\n", flush=True)
                    results = aichat(query)  
                    print("Eva: " + results, flush=True)
                    say(results) 
            
            
        elif "Using Artificial Intelligence".lower() in query.lower():
            AI(prompt=query)
            title=(' '.join(query.split('intelligence')[1:]).strip())
            print(f"\nEva: You can view the AI response for {title} generated by me in the AI_Responses.",flush=True)
            say(f"You can view the AI response for {title}")
            say("generated by me in the AI_Responses.")

                    
        elif "clear terminal".lower() in query.lower():
            say("Clearing terminal sir...")
            print("\nClearing terminal sir...", flush=True)
            if os.name == 'nt':  # For Windows
                os.system('cls')
            else:  # For Linux and MacOS
                os.system('clear')


if __name__ == '__main__':
    main()