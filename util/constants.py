from os import path, name
from typing import Union

from util.file_manager import FileManager

if name.lower() == "nt":
    CLEAR: str = "cls"
    viewDir: str = "dir /b"
else:
    CLEAR: str = "clear"
    viewDir: str = "ls"

SAVE_PATH: Union[bytes, str] = path.join(path.dirname(__file__), '..', "saves")
DATA_PATH: Union[bytes, str] = path.join(path.dirname(__file__), '..', "data")
SUPPLY: str = "supply"
DEMAND: str = "demand"

# TODO Read data.json and assign variables
