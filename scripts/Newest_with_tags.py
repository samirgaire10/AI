import requests
from bs4 import BeautifulSoup
import json
import concurrent.futures

# Function to extract tags for a model
def get_tags(model_name):
    # Generate the tags URL based on the model name
    tags_url = f"https://ollama.com/library/{model_name.replace(' ', '-').lower()}/tags"
    print(f"Fetching tags for model: {model_name} from {tags_url}")
    
    try:
        response = requests.get(tags_url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching tags for {model_name}: {e}")
        return []
    
    # Parse the tags page content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Locate the elements containing the tags
    tag_elements = soup.find_all('div', class_='break-all font-medium text-gray-900 group-hover:underline')
    
    # Extract and return the text from each tag element
    return [tag.get_text(strip=True) for tag in tag_elements]

# URL of the page to scrape
url = "https://ollama.com/library?sort=newest"
file_name = 'scripts/models.json'

# Send a GET request to the URL with timeout for safety
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Will raise an HTTPError if the status code is not 200
except requests.exceptions.RequestException as e:
    print(f"Error while fetching the page: {e}")
else:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Locate the elements for model names and descriptions
    model_elements = soup.find_all('h2', class_='truncate text-xl font-medium underline-offset-2 group-hover:underline md:text-2xl')
    paragraph_elements = soup.find_all('p', class_='max-w-lg break-words text-neutral-800 text-md')

    # Check if we have the correct elements
    if not model_elements or not paragraph_elements:
        print("No models or paragraphs found. Please verify the page structure or class names.")
    else:
        # Extract model names and paragraphs
        models_data = []
        
        # Create a list to store model names for fetching tags in parallel
        model_names = [model.get_text(strip=True) for model in model_elements]
        
        # Use ThreadPoolExecutor to fetch tags in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            # Submit the get_tags function for each model name to be processed in parallel
            tags_results = executor.map(get_tags, model_names)
        
        # Combine the results
        for model, paragraph, tags in zip(model_elements, paragraph_elements, tags_results):
            model_name = model.get_text(strip=True)
            model_paragraph = paragraph.get_text(strip=True)
            
            # Store the model data including tags
            models_data.append({
                "name": model_name,
                "paragraph": model_paragraph,
                "tags": tags
            })

        # Save to JSON file
        with open(file_name, 'w') as json_file:
            json.dump(models_data, json_file, indent=4)

        # Print model names, paragraphs, and tags
        print("Model Names, Paragraphs, and Tags:")
        for model in models_data:
            print(f"Name: {model['name']}")
            print(f"Description: {model['paragraph']}")
            print(f"Tags: {', '.join(model['tags'])}")
            print("-" * 40)
