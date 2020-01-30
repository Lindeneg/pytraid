from __future__ import annotations
from typing import Tuple, List, Dict, Union

from game.supply import Supply
from util.constants import SUPPLY, DEMAND, CITIES, SUPPLIES


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
        return self.__name[:3]

    @property
    def coordinates(self) -> Tuple[float, float]:
        return self.__phi, self.__gamma

    @property
    def supplies(self) -> List[Supply]:
        return self.__supplies

    @property
    def demands(self) -> List[Supply]:
        return self.__demands

    def IsStartCity(self) -> bool:
        return self.__size <= 1

    @staticmethod
    def GenerateCityList() -> List[City]:
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
            mCities.append(
                City(
                    city["name"],
                    city["phi"],
                    city["gamma"],
                    city["size"],
                    mSupplies,
                    mDemands
                )
            )
        return mCities
