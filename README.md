# Eva - Desktop Assistant

Eva is a Python-based desktop assistant designed to streamline various tasks for users through voice commands. Leveraging speech recognition, text-to-speech capabilities, and integration with the Gemini API for advanced AI interactions, Eva offers a wide range of functionalities to enhance productivity and convenience.

## Features

- **Speech Recognition**: Eva utilizes Google Speech Recognition to accurately interpret voice commands.
- **Text-to-Speech**: Communicates responses using pyttsx3, ensuring seamless interaction with users.
- **AI Integration**: Integration with the Gemini API enables Eva to generate AI-based responses for complex queries.
- **Web Browsing**: Eva can open predefined websites, providing quick access to frequently visited pages.
- **Application Management**: Allows users to open specific applications installed on their computer effortlessly.
- **Music Playback**: Eva can play music from a specified path, catering to users' entertainment needs.
- **Time Reporting**: Provides real-time reporting of the current time.
- **Web Search**: Performs web searches using Google, facilitating quick access to information.

## Uses and Scope

Eva serves as a versatile desktop assistant, catering to a wide range of user needs across various domains:

- **Productivity**: Users can utilize Eva to perform tasks such as opening applications, browsing the web, and checking the time, enhancing overall productivity.
- **Entertainment**: Eva enhances the entertainment experience by playing music on command, providing quick access to favorite tunes.
- **Information Retrieval**: With the ability to perform web searches, Eva serves as a valuable tool for retrieving information efficiently.
- **AI Interaction**: The integration with the Gemini API enables users to engage in meaningful conversations with Eva, leveraging advanced AI capabilities.
- **Customization**: Users can customize Eva by adding new websites to the list or modifying the paths for their installed applications.

## Software And Tools Requirements

1. [GitHub Account](https://github.com/)
2. [Gemini Account](https://gemini.google.com/)
3. [Git CLI](https://git-scm.com/book/en/v2/Getting-Started-The-Command-Line)
4. [VSCode IDE](https://code.visualstudio.com/)

## Getting Started

### Prerequisites

- Python 3.7 or higher
- `pip` (Python package manager)

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/gupta-v/Eva.git
   cd Eva
   ```

2. Create and activate a virtual environment (optional but recommended):

   ```sh
   python -m venv env
   source env/bin/activate   # On Windows use `env\Scripts\activate`
   ```

3. Install the required packages:

   ```sh
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
   - Create a `.env` file in the root directory of the project.
   - Add your Gemini API key to the `.env` file:
     ```
     GEMINI_API_KEY=your_gemini_api_key_here
     ```
5. Set up your application paths:
   - Create a `path.py` file in the root directory of the project.
   - Add your application paths to the `path.py` file:
   - Refer to the `path.py.example` file for the structure.
   ```
    APPLICATION_PATH=your_application_path_here
   ```

## Usage

1. Run the main script:

   ```sh
   python eva.py
   ```

2. Eva will start listening for your commands. Here are some examples of what you can say:

   - **Open Websites**: "Open YouTube", "Open Google", "Open Wikipedia"
   - **Control Applications**: "Open Opera GX", "Open Spotify"
   - **Play Music**: "Play Music"
   - **Report Time**: "What is the time?"
   - **AI Interaction**: "Using Artificial Intelligence", "Answer me"
   - **Web Search**: "Search on web for Python tutorials"

3. To quit Eva, say: "Eva quit".

## Adding New Sites

You can customize Eva to open additional websites by modifying the `sites` list in the main script (`eva.py`). Here is an example:

```python
sites = [
    ["Youtube", "https://youtube.com"],
    ["Google", "https://google.com"],
    ["Wikipedia", "https://wikipedia.com"],
    ["GPT", "https://chat.openai.com"],
    ["CLM", "https://claude.ai"],
    ["LinkedIN", "https://www.linkedin.com"],
    ["Internshala", "https://internshala.com"],
    ["YourSiteName", "https://your-site-url.com"]
    # Add your site here
]
```

## Adding New Applications

You can customize Eva to open additional Applications by adding the code in the main script (`eva.py`). Here is an example:

To add a new application, follow these steps:

1. Locate the section in the main script (`eva.py`) where applications are opened. It should look like this:

```python
elif "Open App_name".lower() in query.lower():
    pathToApp = path.PATH_TO_APP
    print("Opening App_name Sir...")
    say("Opening App_name Sir...")
    subprocess.Popen(pathToApp)
```

To add a new application, follow these steps:

1. Add your application paths to the `path.py` file:

   - Refer to the `path.py.example` file for the structure.

   ```python
   APPLICATION_PATH=your_application_path_here
   ```

2. Replace `"Open App_name"` with the name of your application. For example, if your application is named "YourAppName", it would look like this:

   ```python
   elif "Open YourAppName".lower() in query.lower():
   ```

3. Replace the pathToApp variable with the path to your application's executable file. For example:

   ```python
   pathToYourApp = path.PATH_TO_YOURAPP
   ```

4. Update the message to be spoken and printed by Eva to indicate the opening of your application. For example:

   ```python
   print("Opening YourAppName Sir...")
   say("Opening YourAppName Sir...")
   ```

5. Here's how the updated section would look:

   ```python
   elif "Open YourAppName".lower() in query.lower():
      pathToYourApp = path.PATH_TO_YOURAPP
      say("Opening YourAppName Sir...")
      subprocess.Popen(pathToYourApp)
   ```

## Using Artificial Intelligence

Eva utilizes the Gemini API to interact with artificial intelligence. Simply say "Using Artificial Intelligence" followed by your query, and Eva will generate a response using AI.

## Output Folder for AI Responses

Eva saves the AI-generated responses in a folder named AI_H in the root directory of the project. If the folder doesn't exist, it will be created automatically. Each response is saved as a text file.

## Important Notes:

- Ensure that the paths to applications in path.py are valid for your system.

- You can further customize Eva by modifying the main.py file to include additional websites or applications as per your preferences.
