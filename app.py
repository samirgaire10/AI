from flask import Flask, request
from flask_cors import CORS  # Import CORS
import subprocess



app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/execute', methods=['POST'])
def execute_command():
    command = request.json.get('command')
    try:
        output = subprocess.check_output(command, shell=True, text=True)
        return {'output': output, 'error': None}, 200
    except subprocess.CalledProcessError as e:
        return {'output': None, 'error': str(e)}, 400

if __name__ == '__main__':
    app.run(port=5000)



