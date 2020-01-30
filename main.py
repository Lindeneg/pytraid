#from game.game import Game

from menu.menu import Menu
from game.player import Player
from game.city import City

cities = City.GenerateCityList()
player = Player("Christian", cities[0])


def main():
    menu = Menu()
    menu.Main(player)


if __name__ == "__main__":
    main()
