import curses
from points import Point 

class Interface:

    def __statistics(self, map, hero):
        return [
                f"╔" + "═" * (map.width+2) + "╗",
                f"║ {'Статистика'.center(map.width)} ║",
                f"║ {('Здоровье:' + str(hero.current_health) + '/' + str(hero.max_health)).ljust(map.width)} ║",
                f"║ {('█' * int((hero.current_health / hero.max_health) * map.width) + '░' * (map.width - int((hero.current_health / hero.max_health) * map.width))).ljust(map.width)} ║",
                f"║ {('Оружие:' + str(hero.weapon)).ljust(map.width)} ║",
                f"╚" + "═" * (map.width+2) + "╝",
                ]
    def __guide(self):
        return [
                "Управление:",
                "w - вверх, s - вниз, a - влево, d - вправо",
                "e - инвентарь",
                "q - выход"
            ]

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
            cords = [
                # Центр и радиус 1
                (0, 0), (0, 1), (1, 0), (-1, 0), (0, -1),
                (1, 1), (-1, -1), (-1, 1), (1, -1),
                # Радиус 2
                (0, 2), (2, 0), (0, -2), (-2, 0),
                (1, 2), (2, 1), (2, -1), (1, -2),
                (-1, -2), (-2, -1), (-2, 1), (-1, 2),
                (2, 2), (-2, -2), (-2, 2), (2, -2)
            ]
            for cord in cords:
                pos = Point(hero.position.x + cord[0], hero.position.y + cord[1])
                if pos in map.map:
                    index = map.map.index(pos)
                    map.map[index].is_visible = True


            last_point_y = 0
            for point in map.map:
                if last_point_y <= point.y:
                    last_point_y = point.y
                if point.is_visible:
                    if point.shaded is not None:
                        self.stdscr.addstr(point.y, point.x, point.shaded)
                    else:
                        self.stdscr.addstr(point.y, point.x, point.symbol)                    
            self.stdscr.refresh()

            for y, string in enumerate(self.__statistics(map, hero)):
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

            for y, string in enumerate(self.__guide()):
                last_point_y += 1
                self.stdscr.addstr(last_point_y + 1, 0, string)
            self.stdscr.refresh()


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
            self.stdscr.refresh()

            key = self.__get_input()

            if key == ord('q'):
                self.stdscr.clear()
                break

    def __get_input(self):
        return self.stdscr.getch()