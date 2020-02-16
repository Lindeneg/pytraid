"""
Author : Christian Lindeneg
         https://github.com/Lindeneg
Contact: christian@lindeneg.org
Licence: Public Domain
"""

from __future__ import annotations
from typing import Dict

from util.constants import TRAINS, Cargo


class Train:
    def __init__(
            self,
            name: str,
            price: int,
            maintenance: int,
            speed: int,
            cargoSpace: int
    ) -> None:
        self.__name: str = name
        self.__price: int = price
        self.__maintenance: int = maintenance
        self.__speed: int = speed
        self.__cargoSpace: int = cargoSpace
        self.__cargo: Cargo = {"departure": [], "arrival": []}
        self.IsRoute: bool = False

    @property
    def name(self) -> str:
        return self.__name

    @property
    def sName(self) -> str:
        return self.__name[:3].upper()

    @property
    def price(self) -> int:
        return self.__price

    @property
    def speed(self) -> int:
        return self.__speed

    @property
    def maintenance(self) -> int:
        return self.__maintenance

    @property
    def cargoSpace(self) -> int:
        return self.__cargoSpace

    @property
    def cargo(self) -> Cargo:
        return self.__cargo

    @cargo.setter
    def cargo(self, other: Cargo) -> None:
        self.__cargo = other

    @staticmethod
    def GenerateTrainsDict() -> Dict[str, Train]:
        mTrains: Dict[str, Train] = {}
        for train in TRAINS:
            mTrains[train["name"][:3].upper()] = Train(
                train["name"],
                train["price"],
                train["maintenance"],
                train["speed"],
                train["cargoSpace"]
            )
        return mTrains

    @staticmethod
    def GetTrain(train: Train) -> Train:
        return Train(train.name, train.price, train.maintenance, train.speed, train.cargoSpace)

    def __eq__(self, other: Train) -> bool:
        return self.name == other.name

    def __repr__(self) -> str:
        return f"""
NAME  : {self.name.upper()}
COST  : {self.price}G
UPKEEP: {self.__maintenance}G
SPEED : {self.speed}KM/TURN
CARGO : {self.cargoSpace}
KEY   : {self.sName.upper()}
"""
