import random

class Character:
    def init(self, name, max_health=100, x=0, y=0):
        self.name = name
        self.x = x
        self.y = y
        self.max_health = max_health
        self.current_health = max_health
        

    def attack(self, enemy):
        pass

    def take_damage(self, damage):
        self.current_health -= damage
        if self.current_health <= 0:
            print(f"{self.name} погиб!")
        else:
            print(f"{self.name} получил {damage} урона. Осталось здоровья: {self.current_health}/{self.max_health}")

class Hero(Character):
    def init(self, name, max_health=100, x=0, y=0):
        super().init(name, max_health, x, y)
        self.inventory = Inventory()
        self.weapon = None

    def move(self, direction):
        if direction == 'w':
            self.y -= 1
        elif direction == 's':
            self.y += 1
        elif direction == 'a':
            self.x -= 1
        elif direction == 'd':
            self.x += 1

    def pick_up_item(self, item):
        print(f"{self.name} подобрал {item}")
        self.inventory.add_item(item)

    def check_for_weapon_spawn(self, required_items):
        if self.inventory.has_all_items(required_items):
            self.weapon = "Меч"
            print(f"Вы собрали все необходимые предметы! Теперь у вас есть {self.weapon}.")

    def attack(self, enemy):
        if self.weapon:
            print(f"{self.name} атакует {enemy.name} с {self.weapon}!")
            enemy.take_damage(50)
        else:
            print(f"{self.name} пытается атаковать, но у него нет оружия!")

    def str(self):
        return f"{self.name} (Здоровье: {self.current_health}, Инвентарь: {self.inventory})"

class Enemy(Character):
    def init(self, name, max_health=100, x=0, y=0):
        super().init(name, max_health, x, y)

    def move_randomly(self, max_x, max_y):
        direction = random.choice(['w', 's', 'a', 'd'])
        if direction == 'w' and self.y > 0:
            self.y -= 1
        elif direction == 's' and self.y < max_y - 1:  
            self.y += 1
        elif direction == 'a' and self.x > 0:
            self.x -= 1
        elif direction == 'd' and self.x < max_x - 1:  
            self.x += 1

    def attack(self, hero):
        print(f"{self.name} атакует {hero.name}!")
        hero.take_damage(30)