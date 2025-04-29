from abc import ABC, abstractmethod


class Item(ABC):
    pass

class Weapon(Item):
    pass

    def __str__(self):
        return "Оружие"

class Inventory:
    pass