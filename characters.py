from map import *
from points import *


class Character:

    view: str
    position: ShadedPoint
    game_map: Map

    def __init__(self, game_map, view = None):
        self.view = view
        self.game_map = game_map

        available_points = [point for room in self.game_map.rooms for point in room.coordinates]
        self.position = random.choice(available_points)

        index = game_map.map.index(self.position)
        game_map.map[index] = ShadedPoint(self.position.x, self.position.y, self.view)


class Hero(Character):

    def __init__(self, map):
        super().__init__(map, "@")

    def move(self, x,y):

        index = next((i for i, p in enumerate(self.game_map.map) if p == Point(self.position.x+x, self.position.y+y)), None)

        if index == None:
            return

        position = self.game_map.map[index]

        if position.symbol == Room.view or position.symbol == Coridor.view:

            index = self.game_map.map.index(self.position)
            self.game_map.map[index] = self.position

            self.position = position

            index = self.game_map.map.index(self.position)
            self.game_map.map[index] = ShadedPoint(self.position.x, self.position.y, self.view)

        

        