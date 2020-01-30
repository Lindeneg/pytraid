#from game.game import Game

from menu.menu import Menu
from game.player import Player

player = Player("Christian", "Test")


def main():
    Menu.Main(player)


if __name__ == "__main__":
    main()
