from os import system


from util.constants import CLEAR, viewDir
from game.player import Player


class Menu:
    def Main(self, player: Player) -> Player:
        nextPlayer: Player = self.__GetNextPlayer(player)
        while True:
            system(CLEAR)
            print("\n\n\n" + depotTrain + "\n\n\n")
            print(f"{player.name.upper()}'S TURN\n")
            print(f"CURRENT GOLD: {player.gold}G")
            print(f"CURRENT TURN: #{player.totalTurns}\n")
            print("NEW  ROUTE                (N)")
            print("EDIT ROUTE                (E)")
            print("VIEW FINANCES             (F)")
            print("VIEW ALL SUPPLIES         (V)")
            print("VIEW OPPONENT INFO        (I)")
            print("END TURN                  (Q)")
            print("SAVE AND QUIT             (S)\n")
            choice: str = input("ENTER HERE: ")
            if choice.upper() == "N":
                self.__NewRoute(player)      # TODO NewRoute
            elif choice.upper() == "E":
                self.__EditRoute(player)     # TODO EditRoute
            elif choice.upper() == "F":
                self.__ViewFinances(player)  # TODO PresentFinance
            elif choice.upper() == "V":
                self.__ViewSupplies(player)  # TODO PresentSupplies
            elif choice.upper() == "I":
                self.__ViewOpponent(nextPlayer)  # TODO PresentCompetitor
            elif choice.upper() == "Q":
                break
            elif choice.upper() == "S":
                pass                         # TODO SAVE AND QUIT
        return nextPlayer

    def __NewRoute(self, player) -> None:
        pass

    def __EditRoute(self, player) -> None:
        pass

    def __ViewFinances(self, player) -> None:
        pass

    def __ViewSupplies(self, player) -> None:
        pass

    def __ViewOpponent(self, player) -> None:
        pass

    def __GetNextPlayer(self, player: Player) -> Player:
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
