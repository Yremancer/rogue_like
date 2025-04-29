from abc import ABC, abstractmethod


class Item(ABC):
    def __str__(self):
        return "8"

class Weapon(Item):

    def __str__(self):
        return "Оружие"

class Inventory:

    def __init__(self):
        self.items = [Item()]
        self.size = 5