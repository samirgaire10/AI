from flask import Flask, request
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/execute', methods=['POST'])
def execute_command():
    command = request.json.get('command')
    try:
        # Run the command in a new cmd window and close the terminal automatically after completion
        full_command = f"start cmd /k \"{command} && exit\""
        
        # Run the command in a new terminal window
        subprocess.Popen(full_command, shell=True)

        return {'output': 'Command executed and terminal closed.', 'error': None}, 200
    except Exception as e:
        return {'output': None, 'error': str(e)}, 400

if __name__ == '__main__':
    app.run(port=5000)
