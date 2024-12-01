import os
import sys
import subprocess
import re
from fuzzywuzzy import process
from sr_tts import takeCommand, say


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from searchDir import SEARCH_DIRS


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
def findApplication(query,app_paths):
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
            print("No matching applications found.",flush=True)
            say("No matching applications found.")