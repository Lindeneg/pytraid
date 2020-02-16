"""
Author : Christian Lindeneg
         https://github.com/Lindeneg
Contact: christian@lindeneg.org
Licence: Public Domain
"""

from game.game import Game


def main():
    game: Game = Game.Setup()
    game.StartGame()


if __name__ == "__main__":
    main()
