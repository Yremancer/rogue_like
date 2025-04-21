import curses


class Interface:
    def __init__(self, stdscr, game = None):
        self.stdscr = stdscr
        self.game = game
        self.stdscr.timeout(100)
        curses.curs_set(0)


    def draw_menu(self):

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


    def draw_settings(self):
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

        # self.stdscr.clear()
        # self.stdscr.addstr(0, 0, "Настройки")
        # self.stdscr.addstr(1, 0, f"1. Ширина карты: {first_settings['map_width']} Высота карты: {first_settings['map_height']}, Количество комнат: {first_settings['room_count']} Ширина комнаты: {first_settings['room_width']} Высота комнаты: {first_settings['room_height']}")
        # self.stdscr.addstr(2, 0, f"2. Ширина карты: {second_settings['map_width']} Высота карты: {second_settings['map_height']}, Количество комнат: {second_settings['room_count']} Ширина комнаты: {second_settings['room_width']} Высота комнаты: {second_settings['room_height']}")
        # self.stdscr.refresh()

        # while True:
        #     key = self.__get_input()

        #     if key == ord('1'):
        #         return first_settings
            
        #     elif key == ord('2'):
        #         return second_settings
            
        #     elif key == ord('q'):
        #         return None
            

        choices = [f"Ширина карты: {settings[0]['map_width']} Высота карты: {settings[0]['map_height']}, Количество комнат: {settings[0]['room_count']}, Ширина комнаты: {settings[0]['room_width']}, Высота комнаты: {settings[0]['room_height']}",
                   f"Ширина карты: {settings[1]['map_width']} Высота карты: {settings[1]['map_height']}, Количество комнат: {settings[1]['room_count']}, Ширина комнаты: {settings[1]['room_width']}, Высота комнаты: {settings[1]['room_height']}"]
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
                return settings[choice]

    def draw_map(self):
        
        if self.game is None:
            raise ValueError("Игра не установлена")

        while True:
            for point in self.game.map.map:
                if point.shaded:
                    self.stdscr.addstr(point.y, point.x, self.game.hero.view)
                else:
                    self.stdscr.addstr(point.y, point.x, point.symbol)
            self.stdscr.refresh()

            key = self.__get_input()

            if key == ord('d'):
                self.game.hero.move(1, 0)
            elif key == ord('a'):
                self.game.hero.move(-1, 0)
            elif key == ord('w'):
                self.game.hero.move(0, -1)
            elif key == ord('s'):
                self.game.hero.move(0, 1)
            elif key == ord('q'):
                break

    def __get_input(self):
        return self.stdscr.getch()