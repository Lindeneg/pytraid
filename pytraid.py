from math import sin, cos, sqrt, atan2, radians
from random import randint
from time import sleep
from pickle import dump as pdump
from pickle import load as pload
from os import system, getcwd
from os import name as osname
from data import *


if osname.lower() == 'nt':
    clear = 'cls'
    viewDir = 'dir /b'
    slash = '\\'
else:
    clear = 'clear'
    viewDir = 'ls'
    slash = '/'


class Player(object):
    def __init__(self, name, color='std'):
        self.name = name
        self.color = color
        self.gold = SV['gold']
        self.multiplier = SV['multiplier']

        self.trains = [] 
        # {"from": str, "to": str, "name": str, "distance": int, "cargoOut": list, "cargoIn": list, "currentCity": str}

        self.buildQueue = []
        # {"from": str, "to": str, "turnCost": int, "isTrain": [bool, trainDict]}

        self.cityConnections = []
        # {"from": str, "to": str, "amount": int}

        self.turnFinance = []
        # [str(name), int(value), str(typeof)]

        self.totalTurns = 1
        self.maxDistance = None
        self.maxConnections = None
        self.startCity = self.playerStartCity()

    def playerStartCity(self):
        n = randint(0, len(START_CITIES)-1)
        return START_CITIES.pop(n)


def mainGameHandler(player):
    checkPlayerBuildQueue(player)
    handlePlayerTrainRoutes(player)
    handlePlayerFinances(player)
    setMaxConnections(player, getMaxConnections(player))
    setMaxDistance(player, getMaxDistance(player))
    handleTurn(player)


def handleTurn(player):
    nextPlayerIndex = findNextPlayer(player)
    if hasPlayerWon(player):
        print(f'\n{player.name.upper()} HAS WON AFTER {player.totalTurns} TURNS\n')
        input("PRESS ENTER TO CONTINUE GAME")
    if player.name.upper() == 'AI':
        handleAITurn(player)
    else:
        turn = True 
        while turn:
            choice = presentMainMenu(player)
            if choice.upper() == 'N':
                newRouteMain(player)
            elif choice.upper() == 'E':
                editTrainCargoMain(player)
            elif choice.upper() == 'F': 
                presentTurnFinance(player)
            elif choice.upper() == 'P':
                presentProductValues()
            elif choice.upper() == 'I':
                presentCompetitor(PLAYER_LIST[nextPlayerIndex])
            elif choice.upper() == 'T':
                turn = False
            elif choice.upper() == 'Q':
                saveGame()
                exitGame()
    checkPlayerBuildQueue(player)
    player.totalTurns += 1
    player.turnFinance.clear()
    mainGameHandler(PLAYER_LIST[nextPlayerIndex])


def checkPlayerBuildQueue(player):
    if len(player.buildQueue) < 1:
        return
    for i in range(len(player.buildQueue)):
        currentObject = player.buildQueue[i]
        if -1 < int(currentObject["turnCost"]) < 1:
            if currentObject["isTrain"][0]:
                player.trains.append({
                    'from': currentObject["from"],
                    'to': currentObject["to"],
                    'name': TABB[currentObject["isTrain"][1]['train']],
                    'distance': currentObject["isTrain"][1]['distance'],
                    'cargoOut': currentObject["isTrain"][1]['cargoOut'],
                    'cargoIn': currentObject["isTrain"][1]['cargoIn'],
                    'currentCity': currentObject["isTrain"][1]['currentCity'],
                    'currentDistance': currentObject["isTrain"][1]['distance']
                    }
                )
            else:
                if len(player.cityConnections) < 1:
                    player.cityConnections.append(
                        {"from": currentObject["from"], 
                        "to": currentObject["to"], 
                        "amount": 1})
                else:
                    for connections in player.cityConnections:
                        if connections["to"] == currentObject["to"] \
                        and connections["from"] == currentObject["from"]:
                            connections["amount"] += 1
                    player.cityConnections.append(
                        {"from": currentObject["from"], 
                        "to": currentObject["to"], 
                        "amount": 1})
        currentObject["turnCost"] -= 1
    cleanPlayerBuildQueue(player)


def cleanPlayerBuildQueue(player):
    cleanQueue = []
    for i in range(len(player.buildQueue)):
        currentObject = player.buildQueue[i]
        if currentObject['turnCost'] >= 0:
            cleanQueue.append(currentObject)
    player.buildQueue.clear()
    player.buildQueue = cleanQueue


def handlePlayerTrainRoutes(player):
    if len(player.trains) < 1:
        return
    for i in range(len(player.trains)):
        currentTrain = player.trains[i]
        if currentTrain['currentDistance'] <= 0:
            if currentTrain['currentCity'] == currentTrain['from']:
                currentTrain['currentCity'] = currentTrain['to']
            else:
                currentTrain['currentCity'] = currentTrain['from']
            currentTrain['currentDistance'] = currentTrain['distance']
        else:
            currentTrain['currentDistance'] -= TRAINS[currentTrain['name']]['speed']


def handlePlayerFinances(player):
    financeInfo = []
    if len(player.trains) < 1:
        return
    income, expenses = 0, 0
    findCargo = lambda c, t, o, i: i if c == t else o # c: currentCity, t: toCity, o: cargoOut, i: cargoIn
    for train in player.trains:
        if train['currentDistance'] == train['distance']:
            potentialCargo = findCargo(train['currentCity'], train['from'], train['cargoOut'], train['cargoIn'])
            for currentCargo in potentialCargo:
                if currentCargo in [i[0] for i in CITIES[train['currentCity']]['demand'] if i[1] > 0]:
                    if player.name.upper() == 'AI':
                        income += PRODUCTS[currentCargo]['worth'] / SV['AIHandicap']
                    else:
                        income += PRODUCTS[currentCargo]['worth']
                    financeInfo.append([currentCargo, PRODUCTS[currentCargo]['worth'], 'income'])
                    # CITIES[train['currentCity']]['demand'][currentCargo][1] -= 1
        expenses += TRAINS[train['name']]['maintenance']
        financeInfo.append([train['name'], TRAINS[train['name']]['maintenance'], 'expense'])
    player.gold += income - expenses
    player.turnFinance.append(financeInfo)
    return


def calculateDistance(cityOne, cityTwo):
    R = 6371 
    p1, p2 = CITIES[cityOne]["phi"], CITIES[cityTwo]["phi"]
    g1, g2 = CITIES[cityOne]["gamma"], CITIES[cityTwo]["gamma"]
    
    deltaPhi = abs(radians(p2) - radians(p1))
    deltaGamma = abs(radians(g2) - radians(g1))

    a = sin(deltaPhi / 2) ** 2 + cos(radians(p1)) * cos(radians(p2)) * sin(deltaGamma / 2) ** 2
    c = 2 * atan2(sqrt(abs((a))), sqrt(abs(1-a)))
    
    return int(R * c)

def generateCityStartSupplies():
    for i in CITIES:
        for j in CITIES[i]["supply"]:
            CITIES[i]["supply"][CITIES[i]["supply"].index(j)] = [j, int((CITIES[i]["size"]*SV['minSupplyAmount']))]
    for i in CITIES:
        for j in CITIES[i]["demand"]:
            CITIES[i]["demand"][CITIES[i]["demand"].index(j)] = [j, int((CITIES[i]["size"]*SV['minSupplyAmount']))]
    return

def createPlayer():
    i = 0
    while not i == 1:
        system(clear)
        print("\nPLAY PLAYER VS PLAYER (P)\nPLAY PLAYER VS AI     (A)")
        choice = input("\nENTER HERE: ")
        if choice.upper() == 'A':
            system(clear)
            print("\nYOU WILL BE PLAYING AGAINST SINGLE AI")
            playerName = input("\nENTER YOUR NAME: ")
            newPlayer(playerName.capitalize())
            newPlayer('AI')
            i = 1
        if choice.upper() == 'P':
            system(clear)
            playerOne = input("\nENTER PLAYER ONE NAME: ")
            playerTwo = input("\nENTER PLAYER TWO NAME: ")
            newPlayer(playerOne.capitalize())
            newPlayer(playerTwo.capitalize())
            i = 1
    return

def newPlayer(name, color='std'):
    player = Player(name, color)
    PLAYER_LIST.append(player)
    return

def findNextPlayer(player):
    currentIndex = PLAYER_LIST.index(player)
    if int(currentIndex) == int(len(PLAYER_LIST)-1):
        return 0
    else:
        return (currentIndex+1)

def calculateTurnCost(player, distance=None, train=None):
    # right now, building/editing anything, costs 1 turn
    return 1

def hasPlayerWon(player):
    if player.gold >= SV['maxGold']:
        return True
    return

def saveGame():
    system(clear)
    name = input("PLEASE ENTER NAME OF YOUR SAVE GAME\n\nENTER HERE: ")
    playerDict = {}
    for player in PLAYER_LIST:
        playerDict[player.name.lower()] = player
    playerDict['cities'] = CITIES
    saveGamePath = f'{SAVE_GAME_DIR}/{name.lower()}'
    saveThisGame = open(saveGamePath, 'ab')
    pdump(playerDict, saveThisGame)
    saveThisGame.close()
    return

def loadGame():
    i = 0
    while not i == 1:
        system(clear)
        print('CURRENT SAVED GAMES:\n')
        path = f'{getcwd()}{slash}saves'
        system(f'{viewDir} {path}')
        loadGameName = input('\nWHICH SAVE WOULD YOU LIKE TO LOAD?\n\nENTER HERE (0 TO GO BACK): ')
        if str(loadGameName) == '0':
            return False
        try:
            loadThisGame = open(f'{path}{slash}{loadGameName.lower()}', 'rb')
            i = 1
        except FileNotFoundError:
            system(clear)
            print('NAME OF SAVE GAME NOT FOUND\nTRY AGAIN')
            sleep(1)
    playerDict = pload(loadThisGame)
    PLAYER_LIST.clear()
    for player in playerDict:
        PLAYER_LIST.append(playerDict[player])
    generateCityStartSupplies() # todo:  save city information instead and then load that dict
    return


def exitGame():
    system(clear)
    print("\n\n\n" + trainDepot + "\n\n\n")
    print(CM[4] + "\nSAVING GAME, THEN EXITING\n\nTHANKS FOR PLAYING!\n" + CM['E'])
    sleep(1)
    system(clear)
    exit()


def presentMainMenu(player):
    system(clear)
    print("\n\n\n" + trainDepot + "\n\n\n")
    print(CM[3] + f"{player.name.upper()}'S TURN" + CM["E"])
    print(CM[3] + f"TARGET: {SV['maxGold']} GOLD" + CM["E"])
    print(CM[3] + f"TURN #{player.totalTurns}" + CM["E"])
    drawGold(player)
    print('\n')
    [print(option) for option in MAIN_MENU]
    choice = input("\n\nENTER HERE: ")
    return choice

def presentStartMenu():
    i = 0
    while not i == 1:
        system(clear)
        print(logo)
        print("\n\n")
        print('WELCOME TO PYTRAID')
        print("\nSTART   A NEW GAME (N)\nLOAD EXISTING GAME (L)\nQUIT               (Q)")
        choice = input("\nENTER HERE: ")
        if choice.upper() == 'N':
            i = 1
        if choice.upper() == 'L':
            i = 1
        if choice.upper() == 'Q':
            system(clear)
            exit()
    return choice


def StartMenu():
    choice = presentStartMenu()
    print(choice)
    if choice.upper() == 'N':
        createPlayer()
        generateCityStartSupplies()
    if choice.upper() == 'L':
        load = loadGame()
        if load is False:
            StartMenu()
    mainGameHandler(PLAYER_LIST[0])


def drawGold(player):
    if player.gold > 0:
        print(CM[3] + f"\n{player.gold} GOLD" + CM["E"])
    else:
        print(CM[4] + f"\n{player.gold} GOLD" + CM["E"])



def presentTurnFinance(player):
    if len(player.turnFinance) < 1:
        system(clear)
        print(CM[3] + "NO FINANCE DATA TO SHOW THIS TURN\n" + CM["E"])
        input("\n\nPRESS ENTER TO CONTINUE ")
        return
    income, expense = {}, {}
    profit = 0
    for i in range(len(player.turnFinance)):
        for j in range(len(player.turnFinance[i])):
            finance = player.turnFinance[i][j]
            name, value, typeof = finance[0], finance[1], finance[2]
            if typeof == 'income':
                try:
                    income[name][0] += 1
                except KeyError:
                    income[name] = [1, value]
            if typeof == 'expense':
                try:
                    expense[name][0] += 1
                except KeyError:
                    expense[name] = [1, value]
    incomeString = "INCOME:"
    if len(income) >= 1:
        for inc in income:
            item = income[inc]
            total = item[0] * item[1]
            profit += total
            incomeString += f"\n\nNAME: {inc.upper()}\nAMOUNT: {item[0]}\nVALUE: {item[1]}\nTOTAL: {total}\n"
    else:
        incomeString += "\n\nNO INCOME THIS TURN:\n"
    expenseString = "EXPENSE:"
    if len(expense) >= 1:
        for exp in expense:
            item = expense[exp]
            total = item[0] * item[1]
            profit -= total
            expenseString += f"\n\nNAME: {exp.upper()}\nAMOUNT: {item[0]}\nVALUE: {item[1]}\nTOTAL: {total}\n"
    else:
        expenseString += "\n\nNO EXPENSE THIS TURN\n"
    system(clear)
    print(CM[3] + f"{incomeString}" + CM["E"])
    print(CM[4] + f"{expenseString}" + CM["E"])
    print(CM[1] + f"\n\nPROFIT: {profit} GOLD" + CM["E"])
    input("\n\nPRESS ENTER TO CONTINUE ")


def presentProductValues():
    productString = ""
    for name in PRODUCTS:
        value = PRODUCTS[name]['worth']
        weight = PRODUCTS[name]['weight']
        productString += f"NAME: {name.upper()}\nWEIGHT: {weight}\nVALUE: {value}\n\n"
    system(clear)
    print(CM[1] + f"{productString}" + CM["E"])
    input("PRESS ENTER TO CONTINUE ")


def presentCompetitor(player):
    system(clear)
    print(CM[2] + f"NAME                   : {player.name}" + CM["E"])
    print(CM[2] + f"CURRENT GOLD           : {player.gold}" + CM["E"])
    print(CM[2] + f"TOTAL CITY CONNECTIONS : {len(player.cityConnections)}" + CM["E"])
    print(CM[2] + f"BUILD QUEUE LENGTH     : {len(player.buildQueue)}" + CM["E"])
    input("\n\nPRESS ENTER TO CONTINUE ")


def getSupplyIndex(city, supply):
    for i in CITIES[city]['supply']:
        if str(i[0]).lower() == str(supply).lower():
            return CITIES[city]['supply'].index(i)

def getMaxConnections(player):
    # as of now, only one connection per city
    # one connection counts as FROM->TO and TO->FROM
    # so there and back again
    if player.multiplier <= SV['multiplier']:
        return 1

def setMaxConnections(player, value):
    player.maxConnections = value


def getMaxDistance(player):
    return SV["distance"] * player.multiplier

def setMaxDistance(player, value):
    player.maxDistance = value


def newRouteMain(player, fromCity=None):
    if not fromCity: 
        fromCity = player.startCity
    system(clear)
    drawGold(player)
    if len(player.cityConnections) >= 1:
        print(CM[0] + f"\nCURRENT CITY {fromCity.upper()}\nENTER C TO CHANGE CITY\n" + CM["E"])
    else:
        print(CM[0] + f"\nCURRENT CITY: {fromCity.upper()}\n" + CM["E"])
    print(CM[0] + f"\n{fromCity.upper()} SUPPLY: {[i[0].title() for i in CITIES[fromCity.lower()]['supply']]}" + CM["E"])
    print(CM[0] + f"{fromCity.upper()} DEMAND: {[i[0].title() for i in CITIES[fromCity.lower()]['demand']]}\n" + CM["E"])
    print(CM[0] + f"\nAVAILABLE CONNECTIONS FROM {fromCity.upper()}\n" + CM["E"])
    cityList = newRouteOverview(player, fromCity)
    toCity = input("\nENTER KEY HERE (0 MAIN MENU): ")

    if str(toCity) == "0":
        return
    if toCity.upper() == 'C':
        return changeNewRouteOverview(player, fromCity)
    if toCity.lower() not in ABB:
        print(CM[0] + "\nWRONG KEY USED. TRY AGAIN\n" + CM["E"])
        sleep(1)
        return
    
    for city in cityList:
        if city["keyWord"].upper() == toCity.upper() \
        or city["city"].upper() == ABB[toCity.lower()].upper():
            cost, distance = city["cost"], city["distance"]
            if cost > player.gold:
                print(CM[0] + f"CANNOT AFFORD CONNECTION\nCOST {cost}g\nGOLD {player.gold}g\n" + CM["E"])
                sleep(1)
            else:
                turnCost = calculateTurnCost(player, distance)
                train = specifyNewRoute(player, fromCity, ABB[toCity.lower()], cost, turnCost, distance)
                if not train:
                    return
                trainCost = TRAINS[TABB[train.lower()]]['cost']
                system(clear)
                print(CM[0] + f"\nCONNECTION IN PROGRESS\nETA {turnCost} TURN(S)\n\nOVERVIEW OF COST:\n" + CM["E"])
                print(CM[0] + f"COST OF TRACKS: {cost} GOLD" + CM["E"])
                print(CM[0] + f"COST OF TRAIN : {trainCost} GOLD" + CM["E"])
                print(CM[0] + f"\nTOTAL         : {float(cost)+float(trainCost)} GOLD\n" + CM["E"])
                input("\nPRESS ENTER TO CONTINUE ")


def specifyNewRoute(player, fromCity, toCity, cost, turnCost, distance, train=None):
    if train is None:
        system(clear)
        drawGold(player)
        print(CM[0] + f"\nCOST OF TRACKS: {cost} GOLD\n" + CM["E"])
        print(CM[0] + f"ROUTE DISTANCE: {distance}\n" + CM["E"])
        print(CM[0] + f"TURN COST     : {int(turnCost)} TURN(S)\n" + CM["E"])
        print(CM[2] + "\nBUY A TRAIN BY ENTERING KEY:\n" + CM["E"])
        print(CM[2] + f"\n{stringifyBuyableTrains(player)}\n" + CM["E"])
        train = input("\nENTER KEY HERE (0 MAIN MENU): ")
        if str(train) == '0':
            return
        if str(train).lower() not in TABB:
            system(clear)
            print(CM[0] + "\nWRONG KEY USED. TRY AGAIN\n" + CM["E"])
            sleep(1)
            return
        costSum = float(cost)+float(TRAINS[TABB[train.lower()]]['cost'])
        if costSum > player.gold:
            system(clear)
            print(CM[0] + f"CANNOT AFFORD CONNECTION\nCOST {costSum}g\nGOLD {player.gold}g\n" + CM["E"])
            sleep(2)
            return
    else:
        train = train[0:3]

    try:
        cargoOut, cargoIn = loadTrainCargo(player, TABB[train.lower()], fromCity, toCity)
    except TypeError:
        return
    addToQueue = [True, {'train': train, 'distance': distance,'cargoOut': cargoOut,'cargoIn': cargoIn}]
    addNewRoute(player, fromCity, toCity, cost, turnCost, [False])
    player.turnFinance.append([[f'TRAIN TRACKS, DISTANCE: {distance}', cost, 'expense']])
    addNewRoute(player, fromCity, toCity, cost, turnCost, addToQueue)
    player.turnFinance.append([[TABB[train.lower()], TRAINS[TABB[train.lower()]]['cost'], 'expense']])
    return train

def loadTrainCargo(player, train, fromCity, toCity):
    cargoOut, cargoIn = [], []
    cargo = int(TRAINS[train.lower()]["cargo"])
    cargoOutN, cargoInN = cargo, cargo
    cargoOutW, cargoInW = 0, 0
    while cargoOutW < cargo:
        system(clear)
        print(CM[2] + f"\nTRAIN CARGO SPACE: {cargoOutN}\n" + CM["E"])
        print(CM[2] + f"\nTRAIN CARGO-OUT  : {cargoOut}\n" + CM["E"])
        print(CM[2] + f"\nFROM {fromCity.upper()} TO {toCity.upper()}\n" + CM["E"])
        presentSupplyDemand(fromCity, toCity)
        print(CM[2] + "\nADD CARGO BY ENTERING KEY\n" + CM["E"])
        chosenOutCargo = input("\nENTER KEY HERE (0 MAIN MENU): ")
        if chosenOutCargo == "0":
            return
        if chosenOutCargo.lower() in [i[0][0:3].lower() for i in CITIES[fromCity]['supply']]:
            fullName = PABB[chosenOutCargo.lower()]
            index = int(getSupplyIndex(fromCity, fullName))
            cargoOut.append(fullName)
            cargoOutN -= PRODUCTS[fullName]["weight"]
            cargoOutW += PRODUCTS[fullName]["weight"]
            CITIES[fromCity]['supply'][index][1] -= 1
    while cargoInW < cargo:
        system(clear)
        print(CM[2] + f"\nTRAIN CARGO SPACE: {cargoInN}\n" + CM["E"])
        print(CM[2] + f"\nTRAIN CARGO-OUT  : {cargoIn}\n" + CM["E"])
        print(CM[2] + f"\nFROM {toCity.upper()} TO {fromCity.upper()}\n" + CM["E"])
        presentSupplyDemand(toCity, fromCity)
        print(CM[2] + "\nADD CARGO BY ENTERING KEY\n" + CM["E"])
        chosenInCargo = input("\nENTER KEY HERE (0 MAIN MENU): ")
        if chosenInCargo == "0":
            return
        if chosenInCargo.lower() in [i[0][0:3].lower() for i in CITIES[toCity]['supply']]:
            fullName = PABB[chosenInCargo.lower()]
            index = int(getSupplyIndex(toCity, fullName))
            cargoIn.append(fullName)
            cargoInN -= PRODUCTS[fullName]["weight"]
            cargoInW += PRODUCTS[fullName]["weight"]
            CITIES[toCity]['supply'][index][1] -= 1
    return cargoOut, cargoIn

def addNewRoute(player, fromCity, toCity, cost, turnCost, isTrain):
    if isTrain[0]:
        if cost == 0:
            trainCost = 0
        else:
            trainCost = int(TRAINS[TABB[isTrain[1]['train'].lower()]]['cost'])
        newRoute = {
            "from": fromCity, 
            "to": toCity, 
            "turnCost": turnCost,
            "isTrain": [True, {
                'train': isTrain[1]['train'],
                'distance': isTrain[1]['distance'],
                'cargoOut': isTrain[1]['cargoOut'],
                'cargoIn': isTrain[1]['cargoIn'],
                'currentCity': fromCity,
                'currentDistance': isTrain[1]['distance']
                }
            ]
        }
        player.gold -= trainCost
    else:
        newRoute = {
            "from": fromCity,
            "to": toCity,
            "cost": cost,
            "turnCost": turnCost,
            "isTrain": [False] 
        }
        player.gold -= cost
    player.buildQueue.append(newRoute)
    return


def newRouteOverview(player, fromCity):
    cityList = []
    for city in CITIES.keys():
        if not city == fromCity and checkMaxConnections(player, city):
            distance = calculateDistance(fromCity, city)
            keyWord = str(city[0:3]).upper()
            cost = int(distance) * player.multiplier
            if distance <= player.maxDistance:
                cityList.append({
                    "city": city,
                    "distance": distance,
                    "cost": cost,
                    "keyWord": keyWord
                })
    return presentOverview(player, cityList, fromCity)

def presentOverview(player, cityList, fromCity):
    for city in cityList:
        print(CM[0] + f"""
CITY       : {city["city"].title()}
DISTANCE   : {city["distance"]}km
CONNECTIONS: {getCityConnections(player, city["city"], fromCity)} 
COST       : {city["cost"]}g
SUPPLY     : {[i[0].title() for i in CITIES[city['city'].lower()]['supply']]}
DEMAND     : {[i[0].title() for i in CITIES[city['city'].lower()]['demand']]}
KEY        : {city["keyWord"]}
""" + CM["E"])
    return cityList


def changeNewRouteOverview(player, currentCity):
    alreadyShowed = []
    toShow = []
    if len(player.cityConnections) < 1:
        print(CM[0] + "\nYOU HAVE NO OTHER CITY CONNECTIONS\n" + CM["E"])
        sleep(1)
        return
    for cities in player.cityConnections:
        if cities['from'] not in alreadyShowed and cities['from'].upper() != currentCity.upper():
            alreadyShowed.append(cities['from'])
            toShow.append(cities['from'])
        if cities['to'] not in alreadyShowed and cities['to'].upper() != currentCity.upper():
            alreadyShowed.append(cities['to'])
            toShow.append(cities['to'])
    return changeNewRouteOverviewPresenter(player, currentCity, toShow)


def changeNewRouteOverviewPresenter(player, currentCity, cityList):
    system(clear)
    print(CM[0] + f"\nCURRENT CITY: {currentCity.upper()}\n" + CM["E"])
    print(CM[0] + "\nAVAILABLE CITIES:\n" + CM["E"])
    for city in cityList:
        print(CM[0] + f"""
CITY        : {city.upper()}
SUPPLY      : {CITIES[city.lower()]['supply'][0]}
DEMAND      : {CITIES[city.lower()]['demand'][0]}
KEY         : {city.upper()[0:3]}
""" + CM["E"])
    newCity = input("\nENTER KEY HERE (0 MAIN MENU): ")
    if str(newCity) == "0":
        return

    if str(newCity.lower()) not in ABB:
        print(CM[0] + "\nWRONG KEY USED. TRY AGAIN\n" + CM["E"])
        sleep(1)
        return
    return newRouteMain(player, ABB[newCity.lower()])


def editTrainCargoMain(player):
    system(clear)
    if len(player.trains) <= 0:
        print(CM[0] + "\nYOU HAVE NO TRAIN ROUTES\n" + CM["E"])
        sleep(1)
        return

    presentCurrentTrains(player)
    trainIndex = len(player.trains)+1
    while not str(trainIndex) in [str(i) for i in range(len(player.trains))]:
        trainIndex = input("\nENTER KEY HERE (B MAIN MENU): ")
        if trainIndex.upper() == 'B':
            return
    editTrainCargoHandler(player, int(trainIndex))
    return


def editTrainCargoHandler(player, trainIndex):
    train = player.trains[trainIndex]
    fromCity, toCity, cost = train['from'], train['to'], 0
    distance, name = train['distance'], train['name']
    turnCost = calculateTurnCost(player, distance)
    editRoute = specifyNewRoute(player, fromCity, toCity, cost, turnCost, distance, name)
    if not editRoute:
        return
    player.trains.pop(trainIndex)
    system(clear)
    print(CM[0] + f"\nEDITING IN PROGRESS\nETA {turnCost} TURN(S)\n" + CM["E"])
    input("\nPRESS ENTER TO CONTINUE ")
    return


def presentCurrentTrains(player):
    print(CM[2] + "\nCURRENT TRAINS: \n" + CM["E"])
    for i in range(len(player.trains)):
        train = player.trains[i]
        if train['currentDistance'] == train['distance']:
            state = train['currentCity']
        else:
            state = 'CURRENTLY ON ROUTE.'
        print(CM[2] + f"FROM      : {train['from'].upper()}" + CM["E"])
        print(CM[2] + f"TO        : {train['to'].upper()}" + CM["E"])
        print(CM[2] + f"CARGO OUT : {[train['cargoOut'][j].title() for j in range(len(train['cargoOut']))]}" + CM["E"])
        print(CM[2] + f"CARGO IN  : {[train['cargoIn'][j].title() for j in range(len(train['cargoIn']))]}" + CM["E"])
        print(CM[2] + f"IN CITY   : {state.upper()}" + CM["E"])
        print(CM[2] + f"KEY       : {i}\n\n" + CM["E"])
    return


def stringifyCitySupplies(city):
    citySize = CITIES[city.lower()]['size']
    r = ""
    for supply in CITIES[city.lower()]['supply']:
        if supply[1] > 0:
            weight = PRODUCTS[supply[0].lower()]['weight']
            amount = supply[1]
            key = supply[0][0:3].upper()
            r += f"({supply[0].upper()}, {amount}, {weight}, {key}) "
    return r


def stringifyCityDemands(city):
    citySize = CITIES[city.lower()]['size']
    r = ""
    for demand in CITIES[city.lower()]['demand']:
        if demand[1] > 0:
            weight = PRODUCTS[demand[0].lower()]['weight']
            amount = demand[1]
            key = demand[0][0:3].upper()
            r += f"({demand[0].upper()}, {amount}, {weight}, {key}) "
    return r


def stringifyBuyableTrains(player):
    r = ""
    for train in TRAINS:
        if TRAINS[train]['level'] <= player.multiplier:
            name, speed, cargo = train, TRAINS[train]['speed'], TRAINS[train]['cargo']
            cost, upkeep = TRAINS[train]['cost'], TRAINS[train]['maintenance']
            key = name[0:3]
            r += f"NAME   : {name.upper()}\nSPEED  : {speed}/turn\nCARGO  : {cargo}\nCOST   : {cost} GOLD\nUPKEEP : {upkeep}/turn\nKEY    : {key.upper()}\n\n"
    return r


def presentSupplyDemand(fromCity, toCity):
    print(CM[0] + "\nFORMAT: (TYPE, AMOUNT, WEIGHT, KEY)\n" + CM["E"])
    print(CM[0] + f"\n{fromCity.upper()}:\nSUPPLY: {stringifyCitySupplies(fromCity)}\n" + CM["E"])
    print(CM[0] + f"DEMAND: {stringifyCityDemands(fromCity)}\n" + CM["E"])
    print(CM[1] + f"\n{toCity.upper()}:\nSUPPLY: {stringifyCitySupplies(toCity)}\n" + CM["E"])
    print(CM[1] + f"DEMAND: {stringifyCityDemands(toCity)}\n" + CM["E"])


def getCityConnections(player, city, fromCity):
    for connections in player.cityConnections:
        if connections["to"].lower() == city.lower() \
        and connections["from"].lower() == fromCity.lower() \
        or connections["from"].lower() == city.lower() \
        and connections["to"].lower() == fromCity.lower():
            return connections["amount"]
    return 0


def checkMaxConnections(player, city):
    if len(player.buildQueue) >= 1:
        for objects in player.buildQueue:
            if objects["to"].lower() == city.lower():
                return False
    if len(player.cityConnections) >= 1:
        for connections in player.cityConnections:
            if connections["to"].lower() == city.lower() \
            or connections["from"].lower() == city.lower():
                if connections["amount"] >= player.maxConnections:
                    return False
    return True


def handleAITurn(ai):
    if ai.totalTurns <= 1:
        cityList = AIFromCityRoutes(ai, ai.startCity.lower())
        bestIndex = findRoute(ai, cityList)
        buildAIRoute(ai, cityList[bestIndex])
        return
    else:
        decideMove(ai)
    return


def decideMove(ai):
    if len(ai.cityConnections) < 1:
        return
    potentialRoutes, visited = {}, []
    for city in ai.cityConnections:
        if not city['to'] in visited:
            visited.append(city['to'])
            try:
                potentialRoutes[city['to']].append(AIFromCityRoutes(ai, city['to']))
            except KeyError:
                potentialRoutes[city['to']] = [AIFromCityRoutes(ai, city['to'])]

    if len(potentialRoutes) == 1:
        city = [i for i in potentialRoutes.keys()][0]
        bestIndex = findRoute(ai, potentialRoutes[city][0])
        buildAIRoute(ai, potentialRoutes[city][0][bestIndex])
        return
    bestPerCity = {}
    if len(potentialRoutes) > 1:
        cityKeys = [i for i in potentialRoutes.keys()]
        for city in cityKeys:
            outerLimit = 0
            currentCity = potentialRoutes[city]
            while outerLimit < len(potentialRoutes):
                innerLimit = 0
                currentRoute = currentCity[innerLimit]
                while innerLimit < len(currentCity):
                    bestIndex = findRoute(ai, currentRoute)
                    if not bestIndex == None:
                        bestPerCity[city] = currentRoute[bestIndex] 
                    innerLimit += 1
                outerLimit += 1
    bestProfit = [0, None]
    for city in bestPerCity:
        if bestPerCity[city]['profit'] > bestProfit[0]:
            bestProfit[0], bestProfit[1] = bestPerCity[city]['profit'], city
    if not bestProfit[1] == None:
        buildAIRoute(ai, bestPerCity[bestProfit[1]])


def AIFromCityRoutes(ai, fromCity):
    cityList = []
    train = getTrain(ai)
    trainCost = TRAINS[train]["cost"]
    for city in CITIES.keys():
        if not city == fromCity and checkMaxConnections(ai, city):
            distance = calculateDistance(fromCity, city)
            if distance <= ai.maxDistance:
                cost = int(distance) * ai.multiplier
                if (cost + trainCost) < ai.gold:
                    supply = CITIES[city]['supply']
                    demand = CITIES[city]['demand']
                    profit = getPotentialProfit(fromCity, [supply, demand], train)
                    cityList.append({
                        "city": city,
                        "fromCity": fromCity,
                        "distance": distance,
                        "cost": cost,
                        "train": train,
                        "turnCost": calculateTurnCost(ai),
                        "trainCost": trainCost,
                        "profit": profit[0],
                        "cargoOut": profit[1],
                        "cargoIn": profit[2]
                    })
    return cityList


def findRoute(ai, cityList):
    bestRoute = [0, float('inf'), None]
    for i in range(len(cityList)):
        city = cityList[i]
        if city['profit'] == bestRoute[0] and city['distance'] < bestRoute[1] \
        or city['profit'] > bestRoute[0] and city['distance'] < ai.maxDistance:
            bestRoute[0], bestRoute[1], bestRoute[2] = city['profit'], city['distance'], i
    return bestRoute[2]


def buildAIRoute(ai, cityDict):
    fromCity, toCity, cost = cityDict['fromCity'], cityDict['city'], cityDict['cost']
    turnCost, train, distance = cityDict['turnCost'], cityDict['train'], cityDict['distance']
    cargoOut, cargoIn = cityDict['cargoOut'], cityDict['cargoIn']
    train, trainCost = cityDict['train'], cityDict['cost']
    
    addToQueue = [True, {'train': train[0:3], 'distance': distance,'cargoOut': cargoOut,'cargoIn': cargoIn}]
    addNewRoute(ai, fromCity, toCity, cost, turnCost, [False])
    addNewRoute(ai, fromCity, toCity, cost, turnCost, addToQueue)
    return

def getPotentialProfit(fromCity, toCity, train):
    # this is really all awful for several reasons, perhaps this whole shebang is actually
    maxCargo = TRAINS[train]["cargo"]
    proOut, proIn, cargoOut, cargoIn = 0, 0, [], []
    fromCitySupply = CITIES[fromCity]['supply']
    fromCityDemand = CITIES[fromCity]['demand']
    toCitySupply, toCityDemand = toCity[0], toCity[1]
    while len(cargoOut) < maxCargo:
        for supply in fromCitySupply:
            if supply[0] in [i[0] for i in toCityDemand if i[1] > 0]:
                if supply[1] >= maxCargo:
                    if len(cargoOut) > 0:
                        cargoOut.clear()
                        proIn = 0
                    proIn += PRODUCTS[supply[0]]['worth'] * maxCargo
                    cargoOut.extend([supply[0] for i in range(maxCargo)])
    while len(cargoIn) < maxCargo:
        for demand in fromCityDemand:
            if demand[0] in [i[0] for i in toCitySupply if i[1] > 0]:
                if demand[1] >= maxCargo:
                    if len(cargoIn) > 0:
                        cargoIn.clear()
                        proOut = 0
                    proOut += PRODUCTS[demand[0]]['worth'] * maxCargo
                    cargoIn.extend([demand[0] for i in range(maxCargo)])
    return (proIn+proOut), cargoOut, cargoIn

def getTrain(ai):
    if ai.multiplier <= SV['multiplier']:
        return [i for i in TRAINS.keys()][0]
    # more trains ..


if __name__ == '__main__':
    StartMenu()