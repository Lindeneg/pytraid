from typing import Union

from util.constants import mLEVELS, City, Connection, Supply, Route, Train, Queue, FinanceList
from route.route import Route


class Player:
    def __init__(
            self,
            name: str,
            startCity: City,
            startGold: int = 1000,
            startDistance: int = 200
    ) -> None:
        self.__name: str = name
        self.__gold: int = startGold
        self.__maxDist: int = startDistance
        self.__maxEqRoutes: int = 1
        self.__level: int = 1
        self.__buildQueue: Queue = []
        self.__connections: Connection = []
        self.__turnFinance: FinanceList = {"income": [], "expense": []}
        self.__totalTurns: int = 1
        self.__startCity: City = startCity

    @property
    def name(self) -> str:
        return self.__name

    @property
    def gold(self) -> int:
        return self.__gold

    @gold.setter
    def gold(self, other) -> None:
        self.__gold = other

    @property
    def maxDistance(self) -> int:
        return self.__maxDist

    @property
    def maxOfSameRoutes(self) -> int:
        return self.__maxEqRoutes

    @property
    def connections(self) -> Connection:
        return self.__connections

    @property
    def totalTurns(self) -> int:
        return self.__totalTurns

    @property
    def queue(self) -> Queue:
        return self.__buildQueue

    @property
    def turnFinance(self) -> FinanceList:
        return self.__turnFinance

    @property
    def startCity(self) -> City:
        return self.__startCity

    def IncrementTurns(self) -> None:
        self.__totalTurns += 1

    def AddToBuildQueue(self, route: Route) -> int:
        cost = self.CalculateTurnCost(route)
        self.__buildQueue.append([cost, route])
        return cost

    def AddConnection(self, route: Route) -> None:
        self.__connections.append(route)

    def AddIncome(self, thatFinance: Supply) -> None:
        for thisFinance in self.turnFinance["income"]:
            if thisFinance[1] == thatFinance:
                thisFinance[0] += 1
                return
        self.__turnFinance["income"].append([1, thatFinance])

    def AddExpense(self, thatExpense: Union[Train, Route]) -> None:
        for thisExpense in self.turnFinance["expense"]:
            if thisExpense[1] == thatExpense:
                thisExpense[0] += 1
                return
        self.__turnFinance["expense"].append([1, thatExpense])

    def ClearTurnFinance(self) -> None:
        self.__turnFinance["income"].clear()
        self.__turnFinance["expense"].clear()

    def RemoveConnection(self, route: Route) -> None:
        for i in range(len(self.__connections)):
            mRoute: Route = self.__connections[i]
            if mRoute.mID == route.mID:
                self.__connections.pop(i)

    def CalculateTurnCost(self, route: Route) -> int:
        if route.distance / self.maxDistance > 0.5:
            return 2
        return 1

    def CalculateDistanceCost(self, distance) -> int:
        return int(distance * mLEVELS[self.__level])

    # Todo Implement Player methods
    # GetGold
    # GetConnections
    # GetQueue
    # GetFinances


