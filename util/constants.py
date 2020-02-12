from os import path, name
from typing import Tuple, Dict, Union, TypeVar, List, Any

from util.file_manager import ReadJSON, ReadType

City = TypeVar("City")
Player = TypeVar("Player")
Route = TypeVar("Route")
Train = TypeVar("Train")
Supply = TypeVar("Supply")

Connection = List[Route]
Queue = List[List[Union[int, Route]]]
ConnectionInfo = List[Tuple[City, int, int]]
FinanceList = Dict[str, Union[List[List[Union[int, Union[Supply, Train, Route]]]]]]
Cargo = Dict[str, List[Supply]]

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
DEPART: str = "departure"
ARRIVE: str = "arrival"

gameData: ReadType = ReadJSON(f"{DATA_PATH}/data.json")
SUPPLIES = gameData["supplies"]
CITIES = gameData["cities"]
TRAINS = gameData["trains"]

mLEVELS: Dict[int, Union[int, float]] = {
    1: 3,
    2: 2.5,
    3: 2,
    4: 1.5,
    5: 1
}
