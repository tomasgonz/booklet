import json

# Specify the path to the JSON file
file_path = 'cache/quotes.json'

# Load the quotes from the JSON file
def load_quotes():
    with open(file_path, 'r') as file:
        quotes = json.load(file)
    return quotes

quotes = load_quotes()

