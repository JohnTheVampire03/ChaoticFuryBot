import json
from pathlib import Path
import emojis


def get_path():
    """
    A function to get the current path to bot.py
    :return: cwd (string): Path to bot.py directory
    """
    cwd = Path(__file__).parents[1]
    cwd = str(cwd)
    return cwd


def read_json(filename):
    """
    A function that reads a json file and returns the data.
    :param filename: The name of the file to read. (string)
    :return: data (dict): A dict of the data in the file.
    """
    cwd = get_path()
    with open(cwd+"/bot_config/"+filename+".json", 'r') as file:
        data = json.load(file)
    return data


def write_json(data, filename):
    """
    A function used to write data to a json file
    :param data: The data to write to the file. (dict)
    :param filename: The name of the file to write to. (string)
    """
    cwd = get_path()
    with open(cwd + "/bot_config/" + filename + ".json", 'w') as file:
        json.dump(data, file, indent=4)
