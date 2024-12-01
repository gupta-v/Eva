import os
import sys

import webbrowser
import datetime


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'EvaFunctions')))
from EvaFunctions import sr_tts
from EvaFunctions.musicHandling import player   
from EvaFunctions import appLaunch
from EvaFunctions import appHandling
from EvaFunctions import webSearchHandling
from EvaFunctions import geminiConfgs

def say(text):
    s = sr_tts.say(text)
    return s

def takeCommand():
    r = sr_tts.takeCommand()
    return r



def main():
    
    user_info = geminiConfgs.get_user_info()  # Get the user info (ask if first time, else load from file)
    geminiConfgs.configure_genai(user_info)   # Configure Eva with the user's info
    
    print(f"Welcome Back, {user_info['preferred_name']}!",flush=True)
    say(f"Welcome Back, {user_info['preferred_name']}!")
    
    print("\nEva at your service Sir...", flush=True)
    say("Eva at your service sir")
    
    app_paths = appHandling.scan_apps()
    
    while True:
        print("\nlistening.....", flush=True)
        query = takeCommand()
        print(query, flush=True)

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
        
        elif "list noted websites".lower() in query.lower():
            print("\nHere are the noted websites sir...", flush=True)
            say("\nHere are the noted websites sir...")
            idx=1
            for site in sites:
                print(f"\n{idx}: {site[0]}",flush=True)
                say(f"{site[0]}")
                idx+=1
        
        elif "the time".lower() in query.lower():
            strf=datetime.datetime.now().strftime("%H:%M:%S")
            print(f"\nThe time is {strf}" , flush=True)
            say("The time is ")
            say(strf)
                

        elif "play music".lower() in query.lower():
            print("\nPlaying random music from your collection.", flush=True)
            say("Playing random music from your collection.")
            player.shuffle_and_play()
            
        elif "pause music".lower() in query.lower():
            print("\nPausing the music.", flush=True)
            say("Pausing the music")
            player.pause_music()
        
        elif "next song".lower() in query.lower():
            print("\nPlaying next song.", flush=True)
            say("Playing next song.")
            player.next_song()

        elif "previous song".lower() in query.lower():
            print("\nPlaying previous song.", flush=True)
            say("Playing previous song.")
            player.previous_song()

        elif "web"in query.lower() and "search" in query.lower():
           webSearchHandling.webSearch(query)
        
        elif "Open Spotify".lower() in query.lower():
            appLaunch.openSpotify()
            
        elif "Open Opera GX".lower() in query.lower():
            appLaunch.openOperaGx()
            
        elif "Open Brave".lower() in query.lower():
            appLaunch.openBrave()
            
        elif "Open Thorium".lower() in query.lower():
            appLaunch.openThorium
            
        elif "Open Firefox".lower() in query.lower():
            appLaunch.openFirefox()
            
        elif "Open Edge".lower() in query.lower():
            appLaunch.openMsEdge()

            
        elif "Open Whatsapp".lower() in query.lower():
             appLaunch.openWhatsapp()
             
        elif "Open Signal".lower() in query.lower():
             appLaunch.openSignal()
             

        elif "Open Telegram".lower() in query.lower():
             appLaunch.openTelegram()
            
        elif "Open Steam".lower() in query.lower():
            appLaunch.openSteam()
            
        elif "Open Riot Client".lower() in query.lower():
            appLaunch.openRiotClient()
            
        elif "Open Razer Cortex".lower() in query.lower():
            appLaunch.openRazerCortex()
            
        elif "Open Razer Synapse".lower() in query.lower():
            appLaunch.openRazerSynapse()
            
        
        elif "open command prompt".lower() in query.lower() or "open cmd" in query.lower():
            appLaunch.openCmd()
            
        elif "open Powershell".lower() in query.lower():
            appLaunch.openPowershell()

        
        elif "search and launch" in query.lower() or "find application" in query.lower():
            appHandling.findApplication(query,app_paths)
                
        elif "reset chat".lower() in query.lower():
            geminiConfgs.Chatstr=""
        
        elif "answer me".lower() in query.lower():
            geminiConfgs.Answer(query)
        
        elif "Eva Listen".lower() in query.lower() or "Eva Let's Chat".lower() in query.lower():
            geminiConfgs.AiChat(query)
            
            
        elif "Using Artificial Intelligence".lower() in query.lower():
            geminiConfgs.AIGenerator(query)

                    
        elif "clear terminal".lower() in query.lower():
            print("\nClearing terminal sir...", flush=True)
            say("Clearing terminal sir...")
            if os.name == 'nt':  # For Windows
                os.system('cls')
            else:  # For Linux and MacOS
                os.system('clear')


if __name__ == '__main__':
    main()