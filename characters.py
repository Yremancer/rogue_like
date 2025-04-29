from map import *
from points import *
from abc import ABC, abstractmethod
from items import *

class Character(ABC):

    name: str
    view: str
    position: ShadedPoint
    game_map: Map
    max_health: int     
    current_health: int   

    
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

    def take_damage(self, damage):
        self.current_health -= damage
        if self.current_health <= 0:
            print(f"{self.name} погиб!")
        else:
            print(f"{self.name} получил {damage} урона. Осталось здоровья: {self.current_health}/{self.max_health}")


class Hero(Character):

    inventory: Inventory
    weapon: Weapon

    def __init__(self, name, map, max_health = 100):
        super().__init__(name, map,  max_health, "☻")
        self.inventory = Inventory()
        self.weapon = Weapon()

    def move(self, x,y):

        index = next((i for i, p in enumerate(self.game_map.map) if p == Point(self.position.x+x, self.position.y+y)), None)

        if index == None:
            return

        position = self.game_map.map[index]

        if (position.symbol == Room.view or position.symbol == Coridor.view) and position.shaded == None:

            self.position.shaded = None
            position.shaded = self.view
            self.position = position

    
    def pick_up_item(self, item):
        print(f"{self.name} подобрал {item}")
        self.inventory.add_item(item)

    def check_for_weapon_spawn(self, required_items):
        if self.inventory.has_all_items(required_items):
            self.weapon = Weapon()
            print(f"Вы собрали все необходимые предметы! Теперь у вас есть {self.weapon}.")

    def attack(self, enemy):
        if self.weapon:
            print(f"{self.name} атакует {enemy.name} с {self.weapon}!")
            enemy.take_damage(self.weapon.damage)
        else:
            print(f"{self.name} пытается атаковать, но у него нет оружия!")
        

class Enemy(Character):

    damage: int
    
    def __init__(self, name, map, max_health=100):
        super().__init__(name, map , max_health, "E")

    def move_randomly(self):
        direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        index = next((i for i, p in enumerate(self.game_map.map) if p == Point(self.position.x+direction[0], self.position.y+direction[1])), None)

        if index == None:
            return

        position = self.game_map.map[index]

        if (position.symbol == Room.view or position.symbol == Coridor.view) and position.shaded == None:

            self.position.shaded = None
            position.shaded = self.view
            self.position = position

    def attack(self, hero):
        print(f"{self.name} атакует {hero.name}!")
        hero.take_damage(self.damage)