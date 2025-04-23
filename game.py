from map import *
from characters import *


class Game:

    map_width: int
    map_height: int
    room_count: int
    map: Map
    hero: Hero

    def __init__(self, map_width, map_height, room_count, room_width, room_height):

        self.map = Map(room_count, map_width, map_height, room_width, room_height)
        self.hero = Hero(self.map)

    

        
    
