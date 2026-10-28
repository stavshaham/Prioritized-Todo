# file_handler.py - by Stav Shaham
# This file handles saving and loading data.

import json


def save_data(data):
    """
    Save task data to data.json.

    Time complexity:
        O(n)
    """

    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )


def load_data():
    """
    Load task data from data.json.

    Time complexity:
        O(n)
    """

    with open("data.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    return data