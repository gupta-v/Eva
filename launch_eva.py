import subprocess
import webbrowser
import time

# Define the Flask app location and the localhost port
flask_app_path = "FlaskApp/app.py"
localhost_url = "http://127.0.0.1:5000"  # Flask default port

def launch_flask_app():
    # Run the Flask app in a separate process
    print("Starting the Flask app...")
    subprocess.Popen(["python", flask_app_path])

    # Give Flask some time to start (e.g., 3 seconds)
    time.sleep(3)

    # Open the local Flask app in the default web browser
    print(f"Opening the app in the browser at {localhost_url}")
    webbrowser.open(localhost_url)

if __name__ == "__main__":
    launch_flask_app()
