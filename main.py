"""
Author : Christian Lindeneg
         https://github.com/Lindeneg
Contact: christian@lindeneg.org
Licence: Public Domain
"""

from game.game import Game # type: ignore[import]

# TODO Write stubfile
# https://mypy.readthedocs.io/en/latest/stubs.html#stub-files

def main():
    game: Game = Game.Setup()
    game.StartGame()


if __name__ == "__main__":
    main()
