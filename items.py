from abc import ABC, abstractmethod
from points import *

class Item(ABC):
    view: str
    position: ShadedPoint
    def __init__(self, view = None):
        self.view = view


class Key(Item):
    def __init__(self):
        super().__init__("K")

class Part_Weapon(Item):
    def __init__(self):
        super().__init__("1")

class Weapon(Item):
    name: str
    damage: int

    def __init__(self, name, view, damage = 10):
        self.name = name
        self.damage = damage
        super().__init__(view)

class Inventory:

    items: list[Item]
    size: int

    def __init__(self, size = 5):
        self.items = []
        self.size = size

    def add_item(self, item: Item):
        if len(self.items) < self.size:
            self.items.append(item)
