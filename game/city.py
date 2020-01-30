from __future__ import annotations
from typing import Tuple, List

from game.supply import Supply
from util.constants import SUPPLY, DEMAND


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

    @staticmethod
    def GenerateCityList() -> List[City]:
        pass
