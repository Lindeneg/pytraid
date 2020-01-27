SV = {
    'gold': 1000,
    'distance': 100,
    'multiplier': 1.5,
    'maxGold': 15000,
    'AIHandicap': 1.75,
    'minSupplyAmount': 3
}
PLAYER_LIST = []

SAVE_GAME_DIR = './saves'

CM= {
    0: '\x1b[1;31;40m',
    1: '\x1b[1;32;40m',
    2: '\x1b[1;33;40m',
    3: '\x1b[1;38;44m',
    4: '\x1b[1;29;41m',
    5: '\x1b[1;30;40m',
    'E': '\x1b[0m'
}

MAIN_MENU = [
    CM[0] + 'NEW ROUTE                (N)' + CM["E"], 
    CM[0] + 'VIEW/EDIT ROUTES         (E)' + CM["E"],  
    CM[1] + 'VIEW FINANCES            (F)' + CM["E"],
    CM[1] + 'VIEW SUPPLY VALUES       (P)' + CM["E"],
    CM[2] + 'VIEW COMPETITOR INFO     (I)' + CM["E"],
    CM[5] + 'END TURN                 (T)' + CM["E"],
    CM[5] + 'SAVE AND QUIT            (Q)' + CM["E"]
]

PRODUCTS = {
    'passengers': {
        'worth': 10.0, 
        'weight': 1,
        'cap': 10.0
    },
    'grain': {
        'worth': 24,
        'weight': 2,
        'cap': 19
    },
    'corn': {
        'worth': 26,
        'weight': 2,
        'cap': 18
    },
    'textiles': {
        'worth': 20,
        'weight': 2,
        'cap': 25
    },
    'fish': {
        'worth': 18,
        'weight': 2,
        'cap': 30
    },
    'beer': {
        'worth': 20,
        'weight': 2,
        'cap': 30
    },
    'paper': {
        'worth': 18,
        'weight': 2,
        'cap': 34
    },
    'ore': {
        'worth': 45,
        'weight': 4,
        'cap': 68
    },
    'coal': {
        'worth': 50,
        'weight': 4,
        'cap': 72
    },
    'steel': {
        'worth': 95,
        'weight': 8,
        'cap': 150
    },
    'cars': {
        'worth': 110,
        'weight': 8,
        'cap': 150
    },
    'arms': {
        'worth': 65,
        'weight': 4,
        'cap': 80
    },
    'medicine': {
        'worth': 65,
        'weight': 4,
        'cap': 85
    },
    'technology': {
        'worth': 75,
        'weight': 4,
        'cap': 105
    },
    'luxury_goods': {
        'worth': 40,
        'weight': 2,
        'cap': 55
    },
    'government': {
        'worth': 50,
        'weight': 2,
        'cap': 65
    }
}
# Product Abbreviations (first three letters)
PABB = {}
for i in [[i[0:3].lower(), i.lower()] for i in PRODUCTS.keys()]:
    PABB[i[0]] = i[1]

UPGRADES = {
    # lower cost of tracks (decrement player multiplier) 
    # or upgrade trains (better speed/lower maintaince/more cargo)
}

CITIES = {
    'dover': {
        'phi': 51.1337, 
        'gamma': 1.3,
        'size': 2, # should be 1
        'supply': ['passengers', 'fish', 'paper'],
        'demand': ['passengers', 'corn', 'beer']
    },
    'carlisle': {
        'phi': 54.88, 
        'gamma': -2.93,
        'size': 1,
        'supply': ['passengers', 'corn', 'textiles'],
        'demand': ['passengers', 'fish', 'paper']
    },
    'whitby': {
        'phi': 54.4863, 
        'gamma': 0.6133,
        'size': 1,
        'supply': ['passengers', 'fish', 'beer'],
        'demand': ['passengers', 'grain', 'coal']
    },
    'exeter': {
        'phi': 50.7004, 
        'gamma': -3.53,
        'size': 2,
        'supply': ['passengers', 'fish', 'corn'],
        'demand': ['passengers', 'grain', 'textiles']
    },
    'derby': {
        'phi': 52.9333, 
        'gamma': -1.5,
        'size': 2,
        'supply': ['passengers', 'textiles', 'ore'],
        'demand': ['passengers', 'fish', 'beer']
    },
    'norwich': {
        'phi': 52.6304, 
        'gamma': 1.3,
        'size': 2,
        'supply': ['passengers', 'beer', 'coal'],
        'demand': ['passengers', 'textiles', 'fish']
    },
    'oxford': {
        'phi': 51.7704, 
        'gamma': -1.25,
        'size': 2,
        'supply': ['passengers', 'steel', 'technology'],
        'demand': ['passengers', 'ore', 'coal']
    },
    'cambridge': {
        'phi': 52.2004, 
        'gamma': 0.1166,
        'size': 2,
        'supply': ['passengers', 'technology', 'paper'],
        'demand': ['passengers', 'medicine', 'luxury_goods']
    },
    'newcastle': {
        'phi': 55.0004, 
        'gamma': -1.6,
        'size': 3,
        'supply': ['passengers', 'steel', 'fish'],
        'demand': ['passengers', 'ore', 'technology']
    },
    'york': {
        'phi': 53.9704, 
        'gamma': -1.08,
        'size': 3,
        'supply': ['passengers', 'grain', 'corn'],
        'demand': ['passengers', 'medicine', 'technology']
    },
    'nottingham': {
        'phi': 52.9703, 
        'gamma': -1.17,
        'size': 3,
        'supply': ['passengers', 'cars', 'beer'],
        'demand': ['passengers', 'steel', 'fish']
    },
    'bighton': {
        'phi': 50.8303, 
        'gamma': -0.17,
        'size': 3,
        'supply': ['passengers', 'textiles', 'beer'],
        'demand': ['passengers', 'luxury_goods', 'fish']
    },
    'southampton': {
        'phi': 50.9, 
        'gamma': -1.4,
        'size': 3,
        'supply': ['passengers', 'grain', 'corn', 'textiles'],
        'demand': ['passengers', 'fish', 'medicine', 'government']
    },
    'plymouth': {
        'phi': 50.3854,
        'gamma': -4.16,
        'size': 3,
        'supply': ['passengers', 'coal', 'steel'],
        'demand': ['passengers', 'government', 'beer', 'corn']
    },
    'leicester': {
        'phi': 52.63, 
        'gamma': -1.1332,
        'size': 4,
        'supply': ['passengers', 'coal', 'ore'],
        'demand': ['passengers', 'government', 'medicine']
    },
    'bristol': {
        'phi': 51.45, 
        'gamma': -2.5833,
        'size': 4,
        'supply': ['passengers', 'paper', 'arms'],
        'demand': ['passengers', 'steel', 'ore', 'grain']
    },
    'leeds': {
        'phi': 53.83, 
        'gamma': -1.58,
        'size': 4,
        'supply': ['passengers', 'paper', 'medicine'],
        'demand': ['passengers', 'textiles', 'fish']
    },
    'manchester': {
        'phi': 53.5004, 
        'gamma': -2.248,
        'size': 5,
        'supply': ['passengers', 'technology', 'textiles'],
        'demand': ['passengers', 'luxury_goods', 'paper']
    }, 
    'liverpool': {
        'phi': 53.416, 
        'gamma': -2.918,
        'size': 5,
        'supply': ['passengers', 'fish', 'luxury_goods'],
        'demand': ['passengers', 'medicine', 'technology', 'arms']
    },
    'birmingham': {
        'phi': 52.475, 
        'gamma': -1.92,
        'size': 5,
        'supply': ['passengers', 'government', 'medicine'],
        'demand': ['passengers', 'cars', 'paper', 'technology']
    },
    'london': {
        'phi': 51.5, 
        'gamma': -0.1167,
        'size': 6,
        'supply': ['passengers', 'medicine', 'technology', 'luxury_goods'],
        'demand': ['passengers', 'cars', 'arms', 'grain', 'textiles']
    }
}
# City Abbreviations (first three letters)
ABB = {}
for i in [[i[0:3].lower(), i.lower()] for i in CITIES.keys()]:
    ABB[i[0]] = i[1]
START_CITIES = [i for i in CITIES.keys() if CITIES[i]['size'] == 1]

TRAINS = {
    'languidade': {
        'cost': 150, 
        'maintenance': 15,
        'speed': 100, 
        'cargo': 3,
        'level': 1 
    },
    'mediann': {
        'cost': 250, 
        'maintenance': 20, 
        'speed': 145, 
        'cargo': 4,
        'level': 1
    },
    'boltify': {
        'cost': 350, 
        'maintenance': 20, 
        'speed': 175, 
        'cargo': 6,
        'level': 1
    }
}
# Train Abbreviations (first three letters)
TABB = {}
for i in [[i[0:3].lower(), i.lower()] for i in TRAINS.keys()]:
    TABB[i[0]] = i[1]

################################################################
##### ASCII ART FOR TERMINAL                  ##################
##### BY: Gregg 'L.A.' Anders                 ##################
##### https://www.asciiart.eu/vehicles/trains ##################
################################################################
train1 = '''
      ___ _________
 _][__|o| |O O O O|
<_______|-|_______|
 /O-O-O     o   o
*********************
'''

train2 = '''
       
        ____          
 ][_n_i_| (   ooo___  
(__________|_[______]
  0--0--0      0  0 
*********************
'''

train2 = '''
                      ___________________________________
        ____          |                 | |             |
 ][_n_i_| (   ooo___  |                 | |             |
(__________|_[______]_|_________________|_|_____________|
  0--0--0      0  0    0               0   0            0
**********************************************************
'''

trainUnderway = '''
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

################################################################
##### ASCII ART FOR TERMINAL                                 ###
##### BY: Igbeard                                            ###
##### https://www.asciiart.eu/buildings-and-places/buildings ###
################################################################
trainDepot = '''
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

logo = '''
########################## WELCOME TO ##########################
##########################   PYTRAID  ##########################


                            P  Y  T  R A
                       ,_____  ____    I
                       |     \_|[]|_'__D
                       |_______|__|_|__|}
=======================oo--oo==oo--OOO\\========================

################################################################
################# https://github.com/funkallero ################
################################################################
'''