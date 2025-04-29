class Item:
    def __init__(self, name):
        self.name = name


class Gun_parts(Item):
    view: str = "*"
    def __init__(self, max_parts):
        self.max_parts = max_parts
    

class Key(Item):
    pass


class Inventory:
    def __init__(self, items=[]):
        self.items = items

    def add_item(self, item):
            self.items.append(item)
            if isinstance(item, Gun_parts):
                gun_parts_count =+ 1
                if gun_parts_count == self.max_parts:
                    Inventory.items.append("gun")