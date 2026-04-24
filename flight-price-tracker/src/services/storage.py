import json
import os

FILE_PATH = "data/data.json"


# Load existing data
def load_data():
    if not os.path.exists(FILE_PATH):
        return {}

    with open(FILE_PATH, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {}


# Save data back to file
def save_data(data):
    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)


# Get last stored price for a route
def get_last_price(route):
    data = load_data()

    if route in data and len(data[route]["history"]) > 0:
        return data[route]["history"][-1]

    return None


# Add new price to history
def update_price(route, new_price):
    data = load_data()

    if route not in data:
        data[route] = {"history": []}

    data[route]["history"].append(new_price)

    save_data(data)


# Get full history (used for graph)
def get_price_history(route):
    data = load_data()

    if route in data:
        return data[route]["history"]

    return []
