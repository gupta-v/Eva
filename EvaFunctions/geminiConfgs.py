import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from sr_tts import takeCommand, say

# Folder and file to store user information
INFORMATION_FOLDER = 'Information'
USER_INFO_FILE = os.path.join(INFORMATION_FOLDER, 'user_info.json')
load_dotenv()



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
chat_session = None

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



def Answer(query):
            print("\nChatting..\n", flush=True)
            results= aichat(query)
            print("Eva: " + results, flush=True)
            say(results)

def AiChat(query):            
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

def AIGenerator(query):
            AI(prompt=query)
            title=(' '.join(query.split('intelligence')[1:]).strip())
            print(f"\nEva: You can view the AI response for {title} generated by me in the AI_Responses.",flush=True)
            say(f"You can view the AI response for {title}")
            say("generated by me in the AI_Responses.")



user_info =get_user_info()  # Get the user info (ask if first time, else load from file)
configure_genai(user_info) 