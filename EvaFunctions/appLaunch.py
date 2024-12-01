import os
import sys
import subprocess
import sr_tts
from sr_tts import say
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import path

def openSpotify():
            pathToSpotify=path.PATH_TO_SPOTIFY
            print("\nOpening Spotify Sir...", flush=True)
            say("Opening Spotify Sir...")
            subprocess.Popen(pathToSpotify)
            
def openOperaGx():
            pathToOperaGx=path.PATH_TO_OPERA_GX
            print("\nOpening Opera GX sir..", flush=True)
            say("Opening Opera GX sir..")
            subprocess.Popen(pathToOperaGx)
            
def openBrave():
            pathToBrave=path.PATH_TO_BRAVE
            print("\nOpening Brave sir..", flush=True)
            say("Opening Brave sir..")
            subprocess.Popen(pathToBrave)
            
def openThorium():
            pathToThorium=path.PATH_TO_THORIUM
            print("\nOpening Thorium sir..", flush=True)
            say("Opening Thorium sir..")
            subprocess.Popen(pathToThorium)
            
def openFirefox():
            pathToFirefox=path.PATH_TO_FIREFOX
            print("\nOpening Firefox sir..", flush=True)
            say("Opening Firefox sir..")
            subprocess.Popen(pathToFirefox)
            
def openMsEdge():
            pathToEdge=path.PATH_TO_EDGE
            print("\nOpening Edge sir..", flush=True)
            say("Opening Edge sir..")
            subprocess.Popen(pathToEdge)

            
def openWhatsapp():
             print("\nOpening Whatsapp Sir...", flush=True)
             say("Opening Whatsapp Sir...")
             os.startfile("whatsapp://")
             
def openSignal():
    pathToSignal=path.PATH_TO_SIGNAL
    print("\nOpening Signal Sir...", flush=True)
    say("Opening Signal Sir...")
    subprocess.Popen(pathToSignal)

def openTelegram():
             print("\nOpening Telegram Sir...", flush=True)
             say("Opening Telegram Sir...")
             os.startfile("tg://")
            
def openSteam():
            pathToSteam=path.PATH_TO_STEAM
            print("\nOpening Steam Sir...", flush=True)
            say("Opening Steam Sir...")
            subprocess.Popen(pathToSteam)
            
def openRiotClient():
            pathToRiot=path.PATH_TO_RIOT
            print("\nOpening Riot Client Sir...", flush=True)
            say("Opening Riot Client Sir...")
            subprocess.Popen(pathToRiot)
            
def openRazerCortex():
            pathToRazerCortex=path.PATH_TO_RAZER_CORTEX
            print("\nOpening Razer Cortex Sir...", flush=True)
            say("Opening Razer Cortex Sir...")
            subprocess.Popen(pathToRazerCortex)
            
def openRazerSynapse():
            pathToRazerSynapse=path.PATH_TO_RAZER_SYNAPSE
            print("\nOpening Razer Synapse Sir...", flush=True)
            say("Opening Razer Synapse Sir...")
            subprocess.Popen(pathToRazerSynapse)
            
        
def openCmd():
            pathToCommandPrompt=path.PATH_TO_CMD
            print("\nOpening Command Prompt Sir...", flush=True)
            say("Opening Command Prompt Sir...")
            os.startfile(pathToCommandPrompt) # Open Command Prompt
            
def openPowershell():
            pathToPowershell=path.PATH_TO_POWERSHELL
            print("\nOpening Powershell Sir...", flush=True)
            say("Opening Powershell Sir...")
            os.startfile(pathToPowershell) # Open Command Prompt
            
            
