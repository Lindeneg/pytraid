from typing import List, Dict, Union

from util.constants import mLEVELS
from game.city import City
from game.supply import Supply
from game.train import Train


ConnectionType = List[Dict[str, Union[City, Train, str, int]]]
QueueType = List[List[Union[int, ConnectionType]]]
FinanceType = List[Union[str, int]]


class Player:
    def __init__(
            self,
            name: str,
            startCity: City,
            startGold: int = 1000,
            startDistance: int = 100
    ) -> None:
        self.__name: str = name
        self.__gold: int = startGold
        self.__maxDist: int = startDistance
        self.__level: int = 1
        self.__buildQueue: QueueType = []
        self.__connections: ConnectionType = []
        self.__finance: FinanceType = []
        self.__totalTurns: int = 1
        self.__startCity: City = startCity

    @property
    def name(self) -> str:
        return self.__name

    @property
    def gold(self) -> int:
        return self.__gold

    @property
    def maxDistance(self) -> int:
        return self.__maxDist

    @property
    def connections(self) -> ConnectionType:
        return self.__connections

    @property
    def totalTurns(self) -> int:
        return self.__totalTurns

    @property
    def startCity(self) -> City:
        return self.__startCity

    def CalculateDistanceCost(self, distance) -> int:
        return int(distance * mLEVELS[self.__level])


    # Todo Implement Player methods
    # GetGold
    # GetConnections
    # GetQueue
    # GetFinances


