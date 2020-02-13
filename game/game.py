from typing import Optional, List, Union

from util.constants import Route, Cargo, Supply, DEPART, ARRIVE
from game.menu import Menu
from player.player import Player
from city.city import City
from train.train import Train

cities = City.GenerateCityList()
trains = Train.GenerateTrainsDict()
startCities = City.GetStartCities()


player = Player("Christian", startCities[1])
player2 = Player("Far", startCities[0])
players = [player, player2]


def Game() -> None:  # TODO: Make into Game Class: init: players, cities and trains
    mPlayer: Optional[Player] = None
    while True:
        mPlayer = GetNextPlayer(mPlayer)
        HandlePlayerQueue(mPlayer)
        HandlePlayerRoutes(mPlayer)
        Menu.Main(mPlayer, cities, trains)  # TODO: Make Menu.Main() non-static and initiate it with an instance of Game
        mPlayer.ClearTurnFinance()
        mPlayer.IncrementTurns()


def GetNextPlayer(mPlayer: Optional[Player]) -> Player:
    if not mPlayer:
        return players[0]
    if players.index(mPlayer) == len(players) - 1:
        return players[0]
    return players[players.index(mPlayer) + 1]


def HandlePlayerQueue(mPlayer: Player) -> None:
    if len(mPlayer.queue) < 1:
        return
    i: int
    for i in range(len(mPlayer.queue)):
        turnCost: int = mPlayer.queue[i][0]
        route: Route = mPlayer.queue[i][1]
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
