import curses

class Interface:

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.stdscr.timeout(100)
        curses.curs_set(0)


    def display_menu(self):

        choices = ["Начать игру", "Настройки", "Выход"]
        choice = 0

        self.stdscr.clear()


        while True:

            for i in range(len(choices)):
                self.stdscr.addstr(i, 0, f"{i + 1}. {choices[i]}{' <-' if i == choice else ''}")

            self.stdscr.refresh()

            key = self.__get_input()

            if key == ord('w'):
                self.stdscr.clear()
                if choice > 0:
                    choice -= 1

            elif key == ord('s'):
                self.stdscr.clear()
                if choice < len(choices) - 1:
                    choice += 1
                
            elif key == 10:
                self.stdscr.clear()
                return choice


    def display_settings(self):
        settings = [
            {
                "map_width": 70,
                "map_height": 30,
                "room_count": 10,
                "room_width": 4,
                "room_height": 6
            },
            {
                "map_width": 70,
                "map_height": 30,
                "room_count": 5,
                "room_width": 7,
                "room_height": 11
            },
            {
                "map_width": 45,
                "map_height": 20,
                "room_count": 5,
                "room_width": 3,
                "room_height": 6
            }
        
        ]
            

        choices = [f"Ширина карты: {settings[0]['map_width']} Высота карты: {settings[0]['map_height']}, Количество комнат: {settings[0]['room_count']}, Ширина комнаты: {settings[0]['room_width']}, Высота комнаты: {settings[0]['room_height']}",
                   f"Ширина карты: {settings[1]['map_width']} Высота карты: {settings[1]['map_height']}, Количество комнат: {settings[1]['room_count']}, Ширина комнаты: {settings[1]['room_width']}, Высота комнаты: {settings[1]['room_height']}",
                   f"Ширина карты: {settings[2]['map_width']} Высота карты: {settings[2]['map_height']}, Количество комнат: {settings[2]['room_count']}, Ширина комнаты: {settings[2]['room_width']}, Высота комнаты: {settings[2]['room_height']}",
                   f"Выход",
                   ]
        choice = 0

        self.stdscr.clear()

        while True:

            for i in range(len(choices)):
                self.stdscr.addstr(i, 0, f"{i + 1}. {choices[i]}{' <-' if i == choice else ''}")

            self.stdscr.refresh()

            key = self.__get_input()

            if key == ord('w'):
                self.stdscr.clear()
                if choice > 0:
                    choice -= 1

            elif key == ord('s'):
                self.stdscr.clear()
                if choice < len(choices) - 1:
                    choice += 1
                
            elif key == 10:
                self.stdscr.clear()
                if choice == len(choices) - 1:
                    return None
                return settings[choice]



    def display_game(self, map, hero, enemy):
        self.stdscr.clear()

        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)


        while True:
            self.__update_visibility(map, hero)

            last_point_y = 0
            last_point_y = self.__draw_map(map, last_point_y)
            last_point_y = self.__draw_statistic(map, hero, last_point_y)
            last_point_y = self.__draw_guide(last_point_y)

            key = self.__get_input()

            if key == ord('d'):
                hero.move(1, 0)
                # hero.take_damage(50)
            elif key == ord('a'):
                hero.move(-1, 0)
            elif key == ord('w'):
                hero.move(0, -1)
            elif key == ord('s'):
                hero.move(0, 1)
            elif key == ord('e'):
                self.display_inventory(hero)
            elif key == ord('q'):
                break
            
            enemy.move_randomly()


    def display_inventory(self, hero):
        while True:
            self.stdscr.clear()
            self.stdscr.addstr(0, 0, "Инвентарь:")

            for i in range(hero.inventory.size):
                x = i * 5 + 1
                y = 1
                item = hero.inventory.items[i] if i < len(hero.inventory.items) else None
                self.__draw_inventory_slot(x, y, item)

            self.stdscr.addstr(4, 0, "Нажмите 'q' для выхода из инвентаря")
            self.stdscr.refresh()

            if self.__get_input() == ord('q'):
                self.stdscr.clear()
                break


    def __draw_inventory_slot(self, x, y, item=None):

        self.stdscr.addstr(y, x, "╔═══╗")
        if item is not None:
            self.stdscr.addstr(y + 1, x, f"║ {str(item)} ║")
        else:
            self.stdscr.addstr(y + 1, x, "║   ║")
        self.stdscr.addstr(y + 2, x, "╚═══╝")


    def __get_input(self):
        return self.stdscr.getch()
    

    def __update_visibility(self, map, hero):
        cords = []

        for x in range(-3, 4):
            for y in range(-3, 4):
                    cords.append((x, y))
        
        for point in map.map:
            for dx, dy in cords:
                if (point.x == hero.position.x + dx and 
                    point.y == hero.position.y + dy):
                    point.is_visible = True
                    break


    def __draw_map(self, map, last_point_y):
        for point in map.map:
            if last_point_y <= point.y:
                last_point_y = point.y
            if point.is_visible:
                if point.shaded is not None:
                    self.stdscr.addstr(point.y, point.x, point.shaded)
                else:
                    self.stdscr.addstr(point.y, point.x, point.symbol)                    
            self.stdscr.refresh()
        return last_point_y


    def __draw_statistic(self, map, hero, last_point_y):
        statistics = [
                f"╔" + "═" * (map.width+2) + "╗",
                f"║ {'Статистика'.center(map.width)} ║",
                f"║ {('Здоровье:' + str(hero.current_health) + '/' + str(hero.max_health)).ljust(map.width)} ║",
                f"║ {('█' * int((hero.current_health / hero.max_health) * map.width) + '░' * (map.width - int((hero.current_health / hero.max_health) * map.width))).ljust(map.width)} ║",
                f"║ {('Оружие:' + str(hero.weapon)).ljust(map.width)} ║",
                f"╚" + "═" * (map.width+2) + "╝",
                ]

        for y, string in enumerate(statistics):
                last_point_y += 1
                if y == 3:
                    for x, char in enumerate(string):
                        if char == '█':
                            self.stdscr.addstr(last_point_y + 1, x, char, curses.color_pair(2))
                        elif char == '░':
                            self.stdscr.addstr(last_point_y + 1, x, char, curses.color_pair(1))
                        else:
                            self.stdscr.addstr(last_point_y + 1, x, char)
                else:
                        self.stdscr.addstr(last_point_y + 1, 0, string)
        return last_point_y
    

    def __draw_guide(self, last_point_y):

        guide = [
                "Управление:",
                "w - вверх, s - вниз, a - влево, d - вправо",
                "e - инвентарь",
                "q - выход"
            ]

        for y, string in enumerate(guide):
                last_point_y += 1
                self.stdscr.addstr(last_point_y + 1, 0, string)
        self.stdscr.refresh()