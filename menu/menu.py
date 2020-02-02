from os import system
from time import sleep
from typing import Optional, List

from util.constants import CLEAR
from util.functions import DistanceBetween
from game.player import Player
from game.city import City


class Menu:
    @staticmethod
    def Main(player: Player, cities: List[City]) -> Player:
        while True:
            system(CLEAR)
            print(f"""
{depotTrain}


{player.name.upper()}'S TURN

CURRENT GOLD     : {player.gold}G
# OF CONNECTIONS : {len(player.connections)}
# OF TURNS       : {player.totalTurns}

NEW  ROUTE                (N)
EDIT ROUTE                (E)
VIEW FINANCES             (F)
VIEW ALL SUPPLIES         (V)
VIEW OPPONENT INFO        (I)
END TURN                  (Q)
SAVE AND QUIT             (S)

""")
            choice: str = input("ENTER HERE: ")
            if choice.upper() == "N":
                NewRoute(player, cities)      # TODO NewRoute
            elif choice.upper() == "E":
                EditRoute(player)     # TODO EditRoute
            elif choice.upper() == "F":
                ViewFinances(player)  # TODO PresentFinance
            elif choice.upper() == "V":
                ViewSupplies(player)  # TODO PresentSupplies
            elif choice.upper() == "I":
                ViewOpponent(player)  # TODO PresentCompetitor
            elif choice.upper() == "Q":
                break
            elif choice.upper() == "S":
                pass                         # TODO SAVE AND QUIT
        return player


def NewRoute(player: Player, cities: List[City], fCity: Optional[City] = None) -> None:
    mHasConnections: str = ""
    if not fCity:
        fCity = player.startCity
    if len(player.connections) >= 1:
        mHasConnections = " | ENTER 'C' TO CHANGE CITY"
    while True:
        system(CLEAR)
        print(f"""
CURRENT CITY{mHasConnections}
{fCity}

AVAILABLE CONNECTIONS
{"".join([city.DistanceStr(fCity, player) for city in cities 
          if DistanceBetween(city, fCity) <= player.maxDistance and city != fCity])}
""")
        choice: str = input("ENTER KEY HERE (0 MAIN MENU): ")
        choice = choice.upper()
        ValidateCityKey(choice, player, fCity, cities)
        if choice == "0":
            break
        if choice == "C" and len(mHasConnections) > 0:
            ChangeNewRouteOverview()


def NewRouteAddTrain():
    pass


def NewRouteAddCargo():
    pass


def ValidateCityKey(key: str, player: Player, fCity: City, cities: List[City]) -> None:
    # TODO Temp store 'available connections' and use that to check against
    if len(key) < 3 or len(key) > 3 or key == fCity.sName:
        KeyErrorMessage(key)
        return
    city: City
    for city in cities:
        if key == city.sName:
            distance: int = DistanceBetween(city, fCity)
            cost: int = player.CalculateDistanceCost(distance)
            if distance > player.maxDistance or cost > player.gold:
                KeyErrorMessage(key)


def KeyErrorMessage(key: str) -> None:
    system(CLEAR)
    print(f"\n\n\nKEY ERROR '{key}'\nTRY AGAIN")
    sleep(2)


def ChangeNewRouteOverview():
    pass


def EditRoute(player) -> None:
    pass


def ViewFinances(player) -> None:
    pass


def ViewSupplies(player) -> None:
    pass


def ViewOpponent(player) -> None:
    pass


def GetNextPlayer(player: Player) -> Player:
    return player


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

