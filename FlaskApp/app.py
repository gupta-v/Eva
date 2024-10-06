import os
import subprocess
from flask import Flask, render_template, Response, jsonify, request
import sys

# Import the AI_Responses path from path.py
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))  # Ensure the parent directory is in the path
import path  # Import the path.py file

app = Flask(__name__)

eva_process = None  # Global variable to track the eva.py process

# Use the path from path.py for the AI_Responses folder
AI_Responses_FOLDER = path.PATH_TO_AI_RESPONSES

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to run eva.py
@app.route('/run_eva')
def run_eva():
    global eva_process
    if eva_process is None or eva_process.poll() is not None:
        # Dynamically get the path to eva.py
        eva_py_path = os.path.join(os.path.dirname(__file__), '..', 'eva.py')
        
        # Start eva.py only if it's not running
        eva_process = subprocess.Popen(
            ['python','-u', eva_py_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
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
            eva_process.stdout.close()
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
