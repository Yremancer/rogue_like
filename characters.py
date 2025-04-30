from map import *
from points import *
from abc import ABC, abstractmethod
from items import *
from notifications import *
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
        notifications = []
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
            notifications.append(Notification(f"Вы подобрали {item.name}!", 10))
            if self.__check_for_weapon_spawn():
                notifications.append(Notification(f"Вы собрали оружие!", 10))
            return notifications


        
    def __check_for_weapon_spawn(self):
        part_count = 0
        for item in self.inventory.items:
            if isinstance(item, Part_Weapon):
                part_count += 1

        if part_count == 3:
            self.weapon = Weapon("Меч", "⚔️", 50)
            self.inventory.items = []
            return True

    def attack(self, enemy):
        if enemy is not None:
            if self.weapon and self.is_adjacent(enemy):
                enemy.take_damage(self.weapon.damage)
                return Notification(f"Вы нанесли врагу {self.weapon.damage} урона!", 10)
    
    def on_exit(self):
        if self.position.symbol == self.game_map.exit_view:
            if any(isinstance(x, Key) for x in self.inventory.items):
                return (True, None)
            else:
                return (False, Notification("У вас нет ключа, чтобы выйти!", 15))
        return (False, None)

        

class Enemy(Character):

    damage: int
    __attack_duration: int = 0
    __move_path = []
    
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
            if self.__attack_duration % 5 == 0:
                hero.take_damage(self.damage)
            self.__attack_duration += 1
    
    def move(self, x,y):

        index = next((i for i, p in enumerate(self.game_map.map) if p == Point(self.position.x+x, self.position.y+y)), None)

        if index == None:
            return

        position = self.game_map.map[index]

        if position.symbol != Map.view and position.shaded == None:

            self.position.shaded = None
            position.shaded = self.view
            self.position = position

    def move_random(self):

        if self.__move_path == []:
            valid_points = []
            for room in self.game_map.rooms:
                for point in room.coordinates:
                    if point.shaded is None:
                        valid_points.append(point)
            for coridor in self.game_map.coridors:
                for point in coridor.path:
                    if point.shaded is None:
                        valid_points.append(point)

            finish_point = random.choice(valid_points)
            self.__move_path = self.__find_path(self.position, finish_point)

        else:
            move = self.__move_path[0]
            self.move(move.x - self.position.x, move.y - self.position.y)
            self.__move_path.remove(move)
            


    def __find_path(self, start: Point, end: Point):
        visited = []
        open = [Node(start, h=_h_calculate(start, end))]

        while len(open) != 0:
            current_node = min(open, key=lambda node: node.f)

            if current_node.content == end:
                path = []
                while current_node:
                    path.append(current_node.content)
                    current_node = current_node.previous
                path.reverse()
                return path
            

            open = [node for node in open if node.content != current_node.content]
            visited.append(current_node)
            

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:

                x = current_node.content.x + dx
                y = current_node.content.y + dy
                
                
                if any(node.content.x == x and node.content.y == y for node in visited):
                    continue
                    
                
                if 1 <= x <= self.game_map.width and 1 <= y <= self.game_map.height:
                    
                    point = next((p for p in self.game_map.map if p.x == x and p.y == y), None)
                    
                    if point is None or (point.symbol == Map.view and (point.x, point.y) != (end.x, end.y)):
                        continue
                    

                    new_node = Node(
                        point,
                        current_node,
                        current_node.g + 1,
                        _h_calculate(point, end)
                    )
                    
                    existing_node = next((node for node in open if node.content == point), None)
                    
                    if existing_node is None or existing_node.f > new_node.f:
                        if existing_node:
                            open.remove(existing_node)
                        open.append(new_node)

        print("Путь не найден!")
        return []


class Node:

    def __init__(self, content, previous = None, g = 0, h = 0):
        self.content = content
        self.previous = previous
        self.g = g
        self.h = h
    
    @property
    def f(self):
        return self.g + self.h

def _h_calculate(current: Point, end: Point):
    return abs(current.x-end.x) + abs(current.y - end.y)