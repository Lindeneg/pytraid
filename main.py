#from game.game import Game

from menu.menu import Menu
from game.player import Player
from game.city import City

cities = City.GenerateCityList()
startCities = City.GetStartCities()


player = Player("Christian", startCities[0])


def main():
    Menu.Main(player, cities)


if __name__ == "__main__":
    main()
