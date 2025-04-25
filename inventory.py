class Item:
    def __init__(self, name):
        self.name = name

class Gun_part(Item):
    view: str = "*"
    def __init__(self, max_parts):
        self.max_parts = max_parts
        gun_parts_count =+ 1
        if gun_parts_count == max_parts:
            Inventory.items.append("gun")

class Inventory:
    def __init__(self, items=[]):
        self.items = items

    
    def add_item(self, item):
            self.items.append(item)

gun_part1 = Gun_part(3)
inventory = Inventory()
inventory.add_item (gun_part1)
print(inventory.items)