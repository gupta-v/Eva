import os
import subprocess
from flask import Flask, render_template, Response, jsonify, request, redirect, url_for
import sys
import json

# Import the AI_Responses path from path.py
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))  # Ensure the parent directory is in the path
import path  # Import the path.py file

app = Flask(__name__)

eva_process = None  # Global variable to track the eva.py process

# Use the path from path.py for the AI_Responses folder
AI_Responses_FOLDER = path.PATH_TO_AI_RESPONSES

# Folder and file to store user information
INFORMATION_FOLDER = 'Information'
USER_INFO_FILE = os.path.join(INFORMATION_FOLDER, 'user_info.json')

# Route for the main page
@app.route('/')
def index():
    if not os.path.exists(USER_INFO_FILE):
        return redirect(url_for('ask_info'))  # Redirect to the setup page if user info doesn't exist
    return render_template('index.html')

# Route to ask for user information (First Time Setup)
@app.route('/setup', methods=['GET', 'POST'])
def ask_info():
    if request.method == 'POST':
        # Extract form data
        name = request.form.get('name')
        preferred_name = request.form.get('preferred_name')
        profession = request.form.get('profession')

        # Collect the interests
        interests = []
        for i in range(1, 6):
            interest = request.form.get(f'interest{i}')
            if interest:
                interests.append(interest)

        # Save to user_info.json
        user_info = {
            'name': name,
            'preferred_name': preferred_name,
            'profession': profession,
            'interests': interests  # Save all collected interests
        }

        # Make sure the Information folder exists
        if not os.path.exists(INFORMATION_FOLDER):
            os.makedirs(INFORMATION_FOLDER)

        # Save user information into a JSON file
        with open(USER_INFO_FILE, 'w') as f:
            json.dump(user_info, f, indent=4)

        return redirect('/')  # Redirect back to the main page after setup

    return render_template('ask_info.html')  # Display the form

# Route to run eva.py
@app.route('/run_eva')
def run_eva():
    global eva_process
    if eva_process is None or eva_process.poll() is not None:
        # --- START OF CHANGES ---
        
        # Get the absolute path to the project's root directory
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        
        # Build the full path to the Python executable inside the virtual environment
        python_executable = os.path.join(project_root, 'env', 'Scripts', 'python.exe')
        
        # Dynamically get the path to eva.py
        eva_py_path = os.path.join(project_root, 'eva.py')
        
        # Check if the venv python executable exists
        if not os.path.exists(python_executable):
            # Fallback for safety, though the specific path is preferred
            python_executable = 'python'

        # Start eva.py using the SPECIFIC python from your virtual env
        eva_process = subprocess.Popen(
            [python_executable, '-u', eva_py_path], # Use the full path here
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            cwd=project_root # Set the working directory to the project root
        )
        
        # --- END OF CHANGES ---
        
        return jsonify({'status': 'Eva started'})
    else:
        return jsonify({'status': 'Eva is already running'})

# Route to stop eva.py
@app.route('/stop_eva')
def stop_eva():
    global eva_process
    if eva_process is not None and eva_process.poll() is None:
        # If the process is running, terminate it
        eva_process.terminate()
        eva_process.wait()  # Wait for process to exit
        eva_process = None
        return jsonify({'status': 'Eva stopped'})
    else:
        return jsonify({'status': 'Eva is not running'})

# Route to stream the output of eva.py
@app.route('/stream')
def stream():
    def generate():
        global eva_process
        if eva_process is not None:
            for stdout_line in iter(eva_process.stdout.readline, ""):
                if "Clearing terminal" in stdout_line:
                    yield "data:clear\n\n"  # Send a 'clear' signal to front-end
                else:
                    yield f"data:{stdout_line}\n\n"
        else:
            yield "data:Eva is not running\n\n"

    return Response(generate(), mimetype='text/event-stream')

# Route to list .txt files in AI_Responses directory
@app.route('/files')
def files():
    files = [f for f in os.listdir(AI_Responses_FOLDER) if f.endswith('.txt')]
    return render_template('files.html', files=files)

# Route to open the selected file
@app.route('/open_file')
def open_file():
    file_name = request.args.get('file')  # Get the file name from the request
    file_path = os.path.join(AI_Responses_FOLDER, file_name)

    try:
        with open(file_path, 'r') as file:
            content = file.read()  # Read the file content
        return render_template('display_file.html', file_name=file_name, content=content)  # Render the new template
    except FileNotFoundError:
        return Response("File not found", status=404)
    except Exception as e:
        return Response(f"An error occurred: {str(e)}", status=500)

if __name__ == '__main__':
    app.run(debug=True)
