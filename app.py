from flask import Flask, request
from flask_cors import CORS  # Import CORS
import subprocess

import requests
from bs4 import BeautifulSoup
import json


# ----------  For getting ollama models from ollama.com     ----------



# URL of the page to scrape
url = "https://ollama.com/library"
file_name = 'models.json'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Locate the elements
    model_elements = soup.find_all('h2', class_='truncate text-xl font-medium underline-offset-2 group-hover:underline md:text-2xl')  # Update class if needed
    paragraph_elements = soup.find_all('p', class_='max-w-lg break-words text-neutral-800 text-md') 

    # Extract model names and paragraphs
    models_data = []
    for model, paragraph in zip(model_elements, paragraph_elements):
        models_data.append({
            "name": model.get_text(strip=True),
            "paragraph": paragraph.get_text(strip=True)
        })

    # Print and save to JSON
    if models_data:
        print("Model Names and Paragraphs:")
        with open(file_name, 'w') as json_file:
            json.dump(models_data, json_file, indent=4)

        for model in models_data:
            print(model["name"], "-", model["paragraph"])

    else:
        print("No models found. Please check the class or the structure of the page.")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")




# --------------- until here is  For getting ollama models from ollama.com ----------





# ----------For downloading ollama MOdels script CMD -------------

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


# ----------  until here is for downloading ollama MOdels script     ----------

