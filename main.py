from game.game import Game
from player.player import Player
from city.city import City
from train.train import Train

cities = City.GenerateCityList()
trains = Train.GenerateTrainsDict()
startCities = City.GetStartCities()


player = Player("Christian", startCities[1])
player2 = Player("Far", startCities[0])
players = [player, player2]


def main():
    game = Game(players, cities, trains)
    game.StartGame()


if __name__ == "__main__":
    main()
