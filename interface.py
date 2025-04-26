import curses

class Interface:

    def __statistics(self, map, hero):
        return [
                f"╔" + "═" * (map.width+2) + "╗",
                f"║ {'Статистика'.center(map.width)} ║",
                f"║ {('Здоровье:' + str(hero.current_health) + '/' + str(hero.max_health)).ljust(map.width)} ║",
                f"║ {('█' * int((hero.current_health / hero.max_health) * map.width) + '░' * (map.width - int((hero.current_health / hero.max_health) * map.width))).ljust(map.width)} ║",
                f"╚" + "═" * (map.width+2) + "╝",
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
            }

        ]
            

        choices = [f"Ширина карты: {settings[0]['map_width']} Высота карты: {settings[0]['map_height']}, Количество комнат: {settings[0]['room_count']}, Ширина комнаты: {settings[0]['room_width']}, Высота комнаты: {settings[0]['room_height']}",
                   f"Ширина карты: {settings[1]['map_width']} Высота карты: {settings[1]['map_height']}, Количество комнат: {settings[1]['room_count']}, Ширина комнаты: {settings[1]['room_width']}, Высота комнаты: {settings[1]['room_height']}",
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
        
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)


        while True:
            last_point_y = 0
            for point in map.map:
                if last_point_y <= point.y:
                    last_point_y = point.y

                self.stdscr.addstr(point.y, point.x, point.symbol)
            self.stdscr.refresh()

            for y, string in enumerate(self.__statistics(map, hero)):
                if y == 3:
                    for x, char in enumerate(string):
                        if char == '█':
                            self.stdscr.addstr(last_point_y + y + 1, x, char, curses.color_pair(2))
                        elif char == '░':
                            self.stdscr.addstr(last_point_y + y + 1, x, char, curses.color_pair(1))
                        else:
                            self.stdscr.addstr(last_point_y + y + 1, x, char)
                else:
                    self.stdscr.addstr(last_point_y + y + 1, 0, string)

            key = self.__get_input()

            if key == ord('d'):
                hero.move(1, 0)
                hero.take_damage(50)
            elif key == ord('a'):
                hero.move(-1, 0)
            elif key == ord('w'):
                hero.move(0, -1)
            elif key == ord('s'):
                hero.move(0, 1)
            elif key == ord('q'):
                break
            
            enemy.move_randomly()
            

    def __get_input(self):
        return self.stdscr.getch()