from map import *
from points import *
from abc import ABC, abstractmethod
from items import *
import time

class Character(ABC):

    name: str
    view: str
    position: ShadedPoint
    game_map: Map
    max_health: int     
    current_health: int   
    is_dead: bool = False

    
    def __init__(self, name, game_map, max_health, view = None):
        self.name = name
        self.view = view
        self.game_map = game_map
        self.max_health = max_health
        self.current_health = max_health

        available_points = [point for room in self.game_map.rooms for point in room.coordinates]
        position = random.choice(available_points)

        index = game_map.map.index(position)
        game_map.map[index] = ShadedPoint(position.x, position.y, position.symbol, self.view)
        self.position = game_map.map[index]
    
    @abstractmethod
    def attack(self, enemy):
        pass
    
    
    def __dead(self):
        self.position.shaded = None
        self.is_dead = True

    def take_damage(self, damage):
        self.current_health -= damage
        if self.current_health <= 0:
            self.current_health = 0
            self.__dead()

    def is_adjacent(self, other):
        return (abs(self.position.x - other.position.x) <= 1 and 
                abs(self.position.y - other.position.y) <= 1 and
                not (self.position.x == other.position.x and 
                     self.position.y == other.position.y))


class Hero(Character):

    inventory: Inventory
    weapon: Weapon

    def __init__(self, name, map, max_health = 100):
        super().__init__(name, map,  max_health, "☻")
        self.inventory = Inventory()
        self.weapon = None

    def move(self, x,y):

        index = next((i for i, p in enumerate(self.game_map.map) if p == Point(self.position.x+x, self.position.y+y)), None)

        if index == None:
            return

        position = self.game_map.map[index]

        if position.symbol != Map.view and position.shaded == None:

            self.position.shaded = None
            position.shaded = self.view
            self.position = position

    
    def pick_up_item(self):
        direction = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for x, y  in direction:
            index = next((i for i, it in enumerate(self.game_map.items) if it.position == Point(self.position.x+x, self.position.y+y)), None)
            if index == None:
                continue
            item = self.game_map.items[index]

            self.inventory.add_item(item)
            item.position.shaded = None
            item.position = None
            self.game_map.items.remove(item)
            self.__check_for_weapon_spawn()

        
    def __check_for_weapon_spawn(self):
        part_count = 0
        for item in self.inventory.items:
            if isinstance(item, Part_Weapon):
                part_count += 1

        if part_count == 3:
            self.weapon = Weapon("Меч", "⚔️", 50)
            self.inventory.items = []

    def attack(self, enemy):
        if enemy is not None:
            if self.weapon and self.is_adjacent(enemy):
                enemy.take_damage(self.weapon.damage)
    
    def on_exit(self):
        if any(isinstance(x, Key) for x in self.inventory.items):
            if self.position.symbol == self.game_map.exit_view:
                return True
            else:
                return False
        return False

        

class Enemy(Character):

    damage: int
    attack_duration: int = 0
    
    def __init__(self, name, map, max_health=100, damage=30):
        self.damage = damage
        super().__init__(name, map , max_health, "E")

    def move_randomly(self):
        direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        index = next((i for i, p in enumerate(self.game_map.map) if p == Point(self.position.x+direction[0], self.position.y+direction[1])), None)

        if index == None:
            return

        position = self.game_map.map[index]

        if position.symbol != Map.view and position.shaded == None:

            self.position.shaded = None
            position.shaded = self.view
            self.position = position

    def attack(self, hero):
        if self.is_adjacent(hero):
            if self.attack_duration % 5 == 0:
                hero.take_damage(self.damage)
            self.attack_duration += 1




