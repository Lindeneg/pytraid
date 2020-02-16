from typing import Optional, List, Dict, Union
from time import sleep

from util.constants import Route, Cargo, Supply, DEPART, ARRIVE
from game.menu import Menu
from player.player import Player
from city.city import City
from train.train import Train


class Game:
    def __init__(
            self,
            players: List[Player],
            cities: List[City],
            trains: Dict[str, Train]
    ) -> None:
        self.__players: List[Player] = players
        self.__cities: List[City] = cities
        self.__trains: Dict[str, Train] = trains

    @property
    def players(self) -> List[Player]:
        return self.__players

    @property
    def cities(self) -> List[City]:
        return self.__cities

    @property
    def trains(self) -> Dict[str, Train]:
        return self.__trains

    def StartGame(self) -> None:
        mPlayer: Optional[Player] = None
        menu: Menu = Menu(self)
        while True:
            mPlayer = self.__GetNextPlayer(mPlayer)
            if HasPlayerWon(mPlayer):
                print("WON")
                sleep(10)
            HandlePlayerQueue(mPlayer)
            HandlePlayerRoutes(mPlayer)
            menu.Main(mPlayer)
            HandlePlayerIncome(mPlayer)
            HandlePlayerAttributes(mPlayer)
            mPlayer.ClearTurnFinance()
            mPlayer.IncrementTurns()

    def __GetNextPlayer(self, mPlayer: Optional[Player]) -> Player:
        if not mPlayer or self.players.index(mPlayer) == len(self.players) - 1:
            return self.players[0]
        return self.players[self.players.index(mPlayer) + 1]


def HasPlayerWon(mPlayer: Player) -> bool:
    return False


def HandlePlayerQueue(mPlayer: Player) -> None:
    if len(mPlayer.queue) < 1:
        return
    i: int
    turnCost: int
    route: Route
    for i in range(len(mPlayer.queue)):
        try:
            turnCost, route = mPlayer.queue[i]
        except IndexError:
            i = len(mPlayer.queue) - 1
            turnCost, route = mPlayer.queue[i]
        if turnCost <= 0:
            mPlayer.connections.append(route)
            mPlayer.queue.pop(i)
        else:
            mPlayer.queue[i][0] -= 1


def HandlePlayerRoutes(mPlayer: Player) -> None:
    if len(mPlayer.connections) < 1:
        return
    route: Route
    for route in mPlayer.connections:
        mPlayer.gold = mPlayer.gold - route.train.maintenance
        mPlayer.AddExpense(route.train)
        if route.currentCity[0] is False:
            if route.currentDistance <= 0:
                cargo: Cargo
                city: City
                if route.currentCity[1] == route.departCity:
                    cargo = route.train.cargo[DEPART]
                    city = route.arriveCity
                    route.currentCity[1] = route.arriveCity
                else:
                    cargo = route.train.cargo[ARRIVE]
                    city = route.departCity
                    route.currentCity[1] = route.departCity
                [mPlayer.AddIncome(i) for i in cargo if i in city.demands]
                route.currentCity[0] = True
            else:
                route.currentDistance = route.currentDistance - route.train.speed
        else:
            route.currentDistance = route.distance
            route.currentCity[0] = False


def HandlePlayerIncome(mPlayer: Player) -> None:
    if len(mPlayer.turnFinance["income"]) < 1:
        return
    income: int = 0
    i: List[Union[int, Supply]]
    for i in mPlayer.turnFinance["income"]:
        income += i[0] * i[1].value
    mPlayer.gold = mPlayer.gold + income


def HandlePlayerAttributes(mPlayer: Player) -> None:
    pass
