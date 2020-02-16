"""
Author : Christian Lindeneg
         https://github.com/Lindeneg
Contact: christian@lindeneg.org
Licence: Public Domain
"""

from __future__ import annotations
from typing import Tuple, List, Dict, Union
from math import sin, cos, sqrt, atan2, radians

from supply.supply import Supply
from util.constants import SUPPLY, DEMAND, CITIES, SUPPLIES

START_CITIES: List[City] = []


class City:  # TODO 6
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

    def DistanceStr(self, distance: int, cost: int) -> str:
        return f"""
NAME    : {self.name.upper()}
DISTANCE: {distance}KM
COST    : {cost}G
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

    @staticmethod
    def DistanceBetween(c1: City, c2: City) -> int:
        p1: float
        p2: float
        g1: float
        g2: float
        R: int = 6371
        p1, g1 = c1.coordinates
        p2, g2 = c2.coordinates
        deltaPhi: float = abs(radians(p2) - radians(p1))
        deltaGamma: float = abs(radians(g2) - radians(g1))
        a: float = sin(deltaPhi / 2) ** 2 + cos(radians(p1)) * cos(radians(p2)) * sin(deltaGamma / 2) ** 2
        c: float = 2 * atan2(sqrt(abs(a)), sqrt(abs(1 - a)))
        return int(R * c)

    def __eq__(self, otherCity: City) -> bool:
        return self.name == otherCity.name

    def __repr__(self) -> str:
        return f"""
NAME  : {self.name.upper()}
SUPPLY: {"".join([i.__repr__() for i in self.supplies])}
DEMAND: {"".join([i.__repr__() for i in self.demands])}
KEY   : {self.sName.upper()}
"""
