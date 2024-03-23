import json

# Load data from JSON file
def load_data():
    with open('players.json', 'r') as f:
        data = json.load(f)
    return data

# Save data to JSON file
def save_data(data):
    with open('players.json', 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
