from os import system
from time import sleep
from typing import Optional, List, Dict, Union, Callable

from supply.supply import Supply
from util.constants import CLEAR, ConnectionInfo, DEPART, ARRIVE
from player.player import Player
from city.city import City
from train.train import Train
from route.route import Route


class Menu:
    @staticmethod
    def Main(player: Player, cities: List[City], trains: Dict[str, Train]) -> None:
        while True:
            system(CLEAR)
            print(f"""
{depotTrain}


{player.name.upper()}'S TURN

CURRENT GOLD     : {player.gold}G
CURRENT QUEUE    : {len(player.queue)}
# OF ROUTES      : {len(player.connections)}
# OF TURNS       : {player.totalTurns}

NEW  ROUTE                (N)
EDIT ROUTE                (E)
VIEW BUILD QUEUE          (B)
VIEW FINANCES             (F)
VIEW OPPONENT INFO        (I)
END TURN                  (Q)
SAVE AND QUIT             (S)

""")
            choice: str = GetUserChoice(inMainMenu=True)
            if choice == "N":
                NewRoute(player, cities, trains)
            elif choice == "E":
                EditRoute(player)  # TODO EditRoute
            elif choice == "B":
                ViewQueue(player)
            elif choice == "F":
                ViewFinances(player)
            elif choice == "I":
                ViewOpponent(player)  # TODO PresentCompetitor
            elif choice == "Q":
                break
            elif choice == "S":
                pass  # TODO SAVE AND QUIT


def NewRoute(player: Player, cities: List[City], trains: Dict[str, Train], fCity: Optional[City] = None) -> None:
    mHasConnections: str = ""
    mFinished: bool = False
    if not fCity:
        fCity = player.startCity
    if len(player.connections) >= 1:
        mHasConnections = " | ENTER 'C' TO CHANGE CITY"
    mConnections: ConnectionInfo = GetConnectionInfo(player, cities, fCity)
    while True:
        system(CLEAR)
        print(f"""
CURRENT CITY{mHasConnections}
{fCity}

AVAILABLE CONNECTIONS
{"".join([mConnections[i][0].DistanceStr(mConnections[i][1], mConnections[i][2]) for i in range(len(mConnections))])}
""")
        choice: str = GetUserChoice()
        if choice == "0":
            break
        elif choice == "C" and len(mHasConnections) > 0:
            ChangeNewRouteOverview(player, cities, trains, fCity)
        elif choice == "C" and len(mHasConnections) < 1:
            KeyErrorMessage("YOU HAVE NO OTHER CONNECTIONS")
        elif choice == fCity.sName:
            KeyErrorMessage("CANNOT CREATE ROUTE FROM AND TO THE SAME CITY")
        elif choice != fCity.sName and len(choice) == 3:
            for city, distance, cost in mConnections:
                if choice == city.sName:
                    if player.gold < cost:
                        KeyErrorMessage(f"CANNOT CHOOSE DESTINATION {choice}\nINSUFFICIENT FUNDS")
                    else:
                        train: Optional[Train] = GetTrain(trains)
                        if not train:
                            break
                        else:
                            totalCost: int = cost + train.price
                            if player.gold < totalCost:
                                KeyErrorMessage("CANNOT AFFORD ROUTE AND TRAIN.")
                                break
                            AddCargoToTrain(train, fCity, city, DEPART)
                            AddCargoToTrain(train, city, fCity, ARRIVE)
                            route: Route = Route(len(player.connections)+1, fCity, city, train, distance, totalCost)
                            if HasCappedRoutes(player, route):
                                KeyErrorMessage(f"YOU ALREADY HAVE THE MAXIMUM AMOUNT OF THIS ROUTE: {route.name}")
                            else:
                                if PurchaseRoute(player, route):
                                    player.gold = player.gold - totalCost
                                    player.AddToBuildQueue(route)
                                    player.AddExpense(route)
                                    mFinished = True
                            break
            if mFinished:
                break
        else:
            KeyErrorMessage(f"'{choice}' NOT A VALID KEY")


def PurchaseRoute(player: Player, route: Route) -> bool:
    while True:
        system(CLEAR)
        print(f"""
PURCHASE THIS ROUTE?

{route}

TURNS TO CREATE: {player.CalculateTurnCost(route)} TURN(S)

Y FOR YES
N FOR NO
""")
        choice: str = GetUserChoice()
        if choice == "Y":
            return True
        if choice == "N" or choice == "0":
            return False


def HasCappedRoutes(player: Player, route: Route) -> bool:
    return len([mRoute for mRoute in player.connections if mRoute == route]) >= player.maxOfSameRoutes


def GetTrain(trains: Dict[str, Train]) -> Optional[Train]:
    routeTrain: Optional[Train] = None
    while True:
        system(CLEAR)
        print("PURCHASABLE TRAINS: ")
        train: Train
        for train in trains.values():
            print(train)
        choice: str = GetUserChoice()
        if choice == "0":
            break
        try:
            routeTrain = trains[choice]
            break
        except KeyError:
            KeyErrorMessage(f"'{choice}' NOT A VALID KEY")
    return routeTrain


def AddCargoToTrain(train: Train, fCity: City, tCity: City, typeof: str) -> None:
    CargoWeight: Callable = lambda cargo: sum([i.weight for i in cargo])
    IsFull: Callable = lambda cargo, limit: False if len(cargo) < 1 else (True if CargoWeight(cargo) >= limit else False)
    while not IsFull(train.cargo[typeof], train.cargoSpace):
        system(CLEAR)
        print(f"""
FROM {fCity.name.upper()} TO {tCity.name.upper()}

CURRENT CARGO : {[i.name.upper() for i in train.cargo[typeof]]}
CURRENT SPACE : {train.cargoSpace - CargoWeight(train.cargo[typeof])}

{fCity.name.upper()}'S SUPPLIES:
{"".join([i.KeyString() for i in fCity.supplies])}

{tCity.name.upper()}'S DEMANDS:
{"".join([i.NonKeyString() for i in tCity.demands])}
""")
        choice: str = GetUserChoice()
        if choice == "0":
            break
        supply: Supply
        for supply in fCity.supplies:
            if choice == supply.sName:
                if supply.weight + CargoWeight(train.cargo[typeof]) <= train.cargoSpace:
                    train.cargo[typeof].append(supply)
                else:
                    KeyErrorMessage(f"{supply.name.upper()} TAKES MORE SPACE THAN AVAILABLE")


def GetConnectionInfo(player: Player, cities: List[City], fCity: City) -> ConnectionInfo:
    cityList: ConnectionInfo = []
    city: City
    for city in cities:
        if not city == fCity:
            distance = City.DistanceBetween(fCity, city)
            cost = player.CalculateDistanceCost(distance)
            if not distance > player.maxDistance:
                cityList.append((city, distance, cost))
    return cityList


def GetUserChoice(inMainMenu: bool = False, inFinanceMenu: bool = False) -> str:
    choice: str
    if inMainMenu:
        choice = input("ENTER KEY HERE: ")
    elif inFinanceMenu:
        choice = input("ENTER 0 TO GO BACK: ")
    else:
        choice = input("ENTER KEY HERE (0 TO CANCEL): ")
    return choice.upper()


def ChangeNewRouteOverview(player: Player, cities: List[City], trains: Dict[str, Train], fCity: City) -> None:
    alreadyPresented: List[City] = []
    while True:
        system(CLEAR)
        print("CONNECTED CITIES:")
        for route in player.connections:
            if not route.departCity in alreadyPresented and not route.departCity == fCity:
                alreadyPresented.append(route.departCity)
                print(route.departCity)
            if not route.arriveCity in alreadyPresented and not route.arriveCity == fCity:
                alreadyPresented.append(route.arriveCity)
                print(route.arriveCity)
        choice: str = GetUserChoice()
        if choice == "0":
            break
        for city in alreadyPresented:
            if choice == city.sName:
                NewRoute(player, cities, trains, city)


def EditRoute(player: Player) -> None:
    if len(player.connections) < 1:
        KeyErrorMessage("YOU HAVE NO CONNECTIONS TO EDIT")
        return
    while True:
        system(CLEAR)
        print("EDITABLE ROUTES:")
        [print(i.KeyString()) for i in player.connections]
        choice: str = GetUserChoice()
        if choice == "0":
            break


def ViewQueue(player: Player) -> None:
    if len(player.queue) < 1:
        KeyErrorMessage("YOUR BUILD QUEUE IS EMPTY")
        return
    while True:
        system(CLEAR)
        print("CURRENT QUEUE")
        i: List[Union[int, Route]]
        for i in player.queue:
            print(f"{i[1]}TURN COST: {i[0]}")
        choice: str = input("\n\nENTER 0 TO GO BACK: ")
        if choice == "0":
            break


def ViewFinances(player: Player) -> None:
    total: int = 0
    while True:
        system(CLEAR)
        print(f"FINANCE FOR TURN #{player.totalTurns}\n")
        print("INCOME\n")
        if len(player.turnFinance["income"]) < 1:
            print("NO INCOME THIS TURN\n")
        else:
            income: List[Union[int, Supply]]
            for income in player.turnFinance["income"]:
                total += (income[0] * income[1].value)
                print(f"{income[0] * income[1].value}G FOR {income[1].name.upper()}")
        print("EXPENSE\n")
        if len(player.turnFinance["expense"]) < 1:
            print("NO EXPENSES THIS TURN\n")
        else:
            expense: List[Union[int, Train, Route]]
            for expense in player.turnFinance["expense"]:
                if not expense[1].IsRoute:
                    total -= (expense[0] * expense[1].maintenance)
                    print(f"{expense[0] * expense[1].maintenance}G FOR {expense[1].name.upper()} UPKEEP")
                else:
                    total -= (expense[0] * expense[1].cost)
                    print(f"{expense[0] * expense[1].cost}G FOR {expense[1].name.upper()} ROUTE")
        print("TOTAL\n")
        print(f"{total}G\n")
        choice: str = GetUserChoice(inFinanceMenu=True)
        if choice == "0":
            break


def ViewOpponent(player: Player) -> None:
    pass


def KeyErrorMessage(msg: str) -> None:
    system(CLEAR)
    print(f"{msg}")
    sleep(2)


noCargoTrain = '''
      ___ _________
 _][__|o| |O O O O|
<_______|-|_______|
 /O-O-O     o   o
*********************
'''

SingleCargoTrain = '''

        ____          
 ][_n_i_| (   ooo___  
(__________|_[______]
  0--0--0      0  0 
*********************
'''

DoubleCargoTrain = '''
                      ___________________________________
        ____          |                 | |             |
 ][_n_i_| (   ooo___  |                 | |             |
(__________|_[______]_|_________________|_|_____________|
  0--0--0      0  0    0               0   0            0
**********************************************************
'''

underwayTrain = '''
                                              ooooo
                                            oooo
                                          oooo
                                        oooo
                                       oo
                                      o  _____ 
                                     II__|[] |
                                    |        |_|_
                                   < OO----OOO  
**************************************************
'''

depotTrain = '''
                                                     ___
                                             ___..--'  .`.
                                    ___...--'     -  .` `.`.
                           ___...--' _      -  _   .` -   `.`.
                  ___...--'  -       _   -       .`  `. - _ `.`.
           __..--'_______________ -         _  .`  _   `.   - `.`.
        .`    _ /\    -        .`      _     .`__________`. _  -`.`.
      .` -   _ /  \_     -   .`  _         .` |Train Depot|`.   - `.`.
    .`-    _  /   /\   -   .`        _   .`   |___________|  `. _   `.`.
  .`________ /__ /_ \____.`____________.`     ___       ___  - `._____`|
    |   -  __  -|    | - |  ____  |   | | _  |   |  _  |   |  _ |
    | _   |  |  | -  |   | |.--.| |___| |    |___|     |___|    |
    |     |--|  |    | _ | |'--'| |---| |   _|---|     |---|_   |
    |   - |__| _|  - |   | |.--.| |   | |    |   |_  _ |   |    |
 ---``--._      |    |   |=|'--'|=|___|=|====|___|=====|___|====|
 -- . ''  ``--._| _  |  -|_|.--.|_______|_______________________|
`--._           '--- |_  |:|'--'|:::::::|:::::::::::::::::::::::|
_____`--._ ''      . '---'``--._|:::::::|:::::::::::::::::::::::|
----------`--._          ''      ``--.._|:::::::::::::::::::::::|
`--._ _________`--._'        --     .   ''-----.................|
     `--._----------`--._.  _           -- . :''           -    ''
          `--._ _________`--._ :'              -- . :''      -- . ''
 -- . ''       `--._ ---------`--._   -- . :''
          :'        `--._ _________`--._:'  -- . ''      -- . ''
  -- . ''     -- . ''    `--._----------`--._      -- . ''     -- . ''
                              `--._ _________`--._
 -- . ''           :'              `--._ ---------`--._-- . ''    -- . ''
          -- . ''       -- . ''         `--._ _________`--._   -- . ''
:'                 -- . ''          -- . ''  `--._----------`--._
'''

logoTrain = '''
########################## WELCOME TO ##########################
##########################   PYTRAID  ##########################


                            P  Y  T  R A
                       ,_____  ____    I
                       |     \_|[]|_'__D
                       |_______|__|_|__|}
=======================oo--oo==oo--OOO\\========================

################################################################
################# https://github.com/lindeneg ##################
################################################################
'''

