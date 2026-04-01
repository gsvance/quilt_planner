import json
from pathlib import Path
from typing import Dict, Any


SAVE_LOAD_VERSION = 1

SAVES_DIRECTORY = Path(__file__).resolve().parent / "saves"

QUILT_NAME_MAX_LENGTH = 32
VALID_QUILT_NAME_CHARACTERS = (set("abcdefghijklmnopqrstuvwxyz")
                               | set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
                               | set("1234567890") | set("_"))


def get_save_load_version():
    return SAVE_LOAD_VERSION


def construct_file_name(quilt_name: str) -> Path:
    assert validate_quilt_name(quilt_name)
    return SAVES_DIRECTORY / (quilt_name + ".json")


def validate_quilt_name(quilt_name: str) -> bool:
    return (len(quilt_name) <= QUILT_NAME_MAX_LENGTH
            and set(quilt_name) <= VALID_QUILT_NAME_CHARACTERS)


def save_quilt_data(data: Dict[str, Any], quilt_name: str) -> None:
    file_name = construct_file_name(quilt_name)
    with file_name.open('w') as json_file:
        json.dump(data, json_file)


def load_quilt_data(quilt_name: str) -> Dict[str, Any]:
    file_name = construct_file_name(quilt_name)
    with file_name.open('r') as json_file:
        data: Dict[str, Any] = json.load(json_file)
    return data
