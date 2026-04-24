import json
import os

FILE_PATH = "data/data.json"


def load_data():
    if not os.path.exists(FILE_PATH):
        return {}

    with open(FILE_PATH, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {}


def save_data(data):
    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)


def get_last_price(route):
    data = load_data()

    if route in data and len(data[route]["history"]) > 0:
        return data[route]["history"][-1]

    return None


def update_price(route, new_price):
    data = load_data()

    if route not in data:
        data[route] = {"history": []}

    data[route]["history"].append(new_price)

    save_data(data)


def get_price_history(route):
    data = load_data()

    if route in data:
        return data[route]["history"]

    return []