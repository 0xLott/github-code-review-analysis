import json
import os


def load_json_file(filename):
    with open(filename, 'r') as file:
        return json.load(file)


def get_last_item(filename):
    data = load_json_file(filename)
    if data:
        return data[-1]  # Return the last item in the array
    return None


def get_json_size(filename):
    return len(load_json_file(filename))


def save_to_json(filename, new_item):
    data = load_json_file(filename)

    data.append(new_item)

    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
