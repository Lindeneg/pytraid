from __future__ import annotations
from typing import List, Union

from util.constants import City, Cargo
from train.train import Train


class Route:
    def __init__(
            self,
            mID: int,
            departCity: City,
            arriveCity: City,
            train: Train,
            distance: int,
            cost: int
    ) -> None:
        self.__mID: int = mID
        self.__departCity: City = departCity
        self.__arriveCity: City = arriveCity
        self.__train: Train = train
        self.__distance: int = distance
        self.__cost: int = cost
        self.__currentCity: List[Union[bool, City]] = [False, self.departCity]
        self.__currentDistance: int = distance

    @property
    def currentCity(self) -> List[Union[bool, City]]:
        return self.__currentCity

    @currentCity.setter
    def currentCity(self, other: List[Union[bool, City]]) -> None:
        self.__currentCity = other

    @property
    def currentDistance(self) -> int:
        return self.__currentDistance

    @currentDistance.setter
    def currentDistance(self, other: int) -> None:
        self.__currentDistance = other

    @property
    def mID(self) -> int:
        return self.__mID

    @property
    def departCity(self) -> City:
        return self.__departCity

    @property
    def arriveCity(self) -> City:
        return self.__arriveCity

    @property
    def train(self) -> Train:
        return self.__train

    @property
    def distance(self) -> int:
        return self.__distance

    @property
    def cost(self) -> int:
        return self.__cost

    @property
    def name(self) -> str:
        return f"{self.departCity.sName} | {self.arriveCity.sName}"

    def HandleMovement(self) -> None:
        if self.currentCity[0] is False:
            if self.currentDistance <= 0:
                if self.currentCity[1] == self.departCity:
                    self.currentCity[1] = self.arriveCity
                else:
                    self.currentCity[1] = self.departCity
                self.currentCity[0] = True
            else:
                self.currentDistance = self.currentDistance - self.train.speed
        else:
            self.currentDistance = self.distance
            self.currentCity[0] = False

    def ChangeCargo(self, newCargo: Cargo) -> None:
        self.train.cargo = newCargo

    def KeyString(self) -> str:
        return f"""
DEPART  : {self.departCity.name.upper()}
ARRIVE  : {self.arriveCity.name.upper()}
DISTANCE: {self.distance}
COST    : {self.cost}
TRAIN   : {self.train.name.upper()}
KEY     : {self.mID}
"""

    def __eq__(self, other: Route) -> bool:
        return (self.departCity == other.departCity and self.arriveCity == other.arriveCity) \
               or (self.departCity == other.arriveCity and self.arriveCity == other.departCity)

    def __repr__(self) -> str:
        return f"""
DEPART  : {self.departCity.name.upper()}
ARRIVE  : {self.arriveCity.name.upper()}
DISTANCE: {self.distance}
COST    : {self.cost}
TRAIN   : {self.train.name.upper()}
"""