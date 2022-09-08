"""file.file module"""

import json
import logging


def read_json_file(filename: str) -> dict:
    """Return content from json-file."""
    try:
        with open(filename, "r", encoding="UTF-8") as file:
            data = json.load(file)
        return data
    except json.decoder.JSONDecodeError:
        logging.error("JSON file empty!")
        return ""
    except FileNotFoundError:
        logging.error("File %s not found!", filename)
        return ""


def read_file(filename: str) -> str:
    """Return content from file."""
    with open(filename, "r", encoding="UTF-8") as file:
        file_str = file.read()
    return file_str


def write_json_file(filename: str, content: dict) -> None:
    """Write content into json file by given filename."""
    with open(filename, "w", encoding="UTF-8") as file:
        json.dump(content, file, indent=4)


def check_file_format(filename: str, file_format: str) -> bool:
    """Check if file_format in filename and return bool."""
    if file_format in filename:
        return True
