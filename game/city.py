from __future__ import annotations
from typing import Tuple, List, Dict, Union, TypeVar

from game.supply import Supply
from util.functions import DistanceBetween
from util.constants import SUPPLY, DEMAND, CITIES, SUPPLIES

# TODO Introduce a city amount of supplies/demands which corresponds to the size of the city

Player = TypeVar("Player")
START_CITIES: List[City] = []


class City:
    def __init__(
            self,
            name: str,
            phi: float,
            gamma: float,
            size: int,
            supply: List[Supply],
            demand: List[Supply]
    ) -> None:
        self.__name: str = name
        self.__phi: float = phi
        self.__gamma: float = gamma
        self.__size: int = size
        self.__supplies: List[Supply] = supply
        self.__demands: List[Supply] = demand

    @property
    def name(self) -> str:
        return self.__name

    @property
    def sName(self) -> str:
        return self.__name[:3].upper()

    @property
    def coordinates(self) -> Tuple[float, float]:
        return self.__phi, self.__gamma

    @property
    def size(self) -> int:
        return self.__size

    @property
    def supplies(self) -> List[Supply]:
        return self.__supplies

    @property
    def demands(self) -> List[Supply]:
        return self.__demands

    def DistanceStr(self, otherCity: City, player: Player) -> str:
        distance: int = DistanceBetween(self, otherCity)
        return f"""
NAME    : {self.name.upper()}
DISTANCE: {distance}KM
COST    : {player.CalculateDistanceCost(distance)}G
SUPPLY  : {"".join([i.__repr__() for i in self.supplies])}
DEMAND  : {"".join([i.__repr__() for i in self.demands])}
KEY     : {self.sName.upper()}
"""

    @staticmethod
    def GetStartCities() -> List[City]:
        return START_CITIES

    @staticmethod
    def GenerateCityList() -> List[City]:
        global START_CITIES
        mCities: List[City] = []
        city: Dict[str, Union[int, float, str, List[str]]]
        for city in CITIES:
            mSupplies: List[Supply] = [
                Supply(
                    SUPPLIES[i]["name"],
                    SUPPLIES[i]["value"],
                    SUPPLIES[i]["weight"],
                    SUPPLY
                ) for i in range(len(SUPPLIES)) if SUPPLIES[i]["name"] in city["supply"]
            ]
            mDemands: List[Supply] = [
                Supply(
                    SUPPLIES[i]["name"],
                    SUPPLIES[i]["value"],
                    SUPPLIES[i]["weight"],
                    DEMAND
                ) for i in range(len(SUPPLIES)) if SUPPLIES[i]["name"] in city["demand"]
            ]
            mCity = City(city["name"], city["phi"], city["gamma"], city["size"], mSupplies, mDemands)
            if int(city["size"]) == 1:
                START_CITIES.append(mCity)
            mCities.append(mCity)
        return mCities

    def __eq__(self, otherCity: City) -> bool:
        return self.name == otherCity.name

    def __repr__(self) -> str:
        return f"""
NAME  : {self.name.upper()}
SUPPLY: {"".join([i.__repr__() for i in self.supplies])}
DEMAND: {"".join([i.__repr__() for i in self.demands])}
KEY   : {self.sName.upper()}
"""
