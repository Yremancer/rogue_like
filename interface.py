import curses
from notifications import *
import time
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

        notifications = [] 

        while True:

            

            self.__update_visibility(map, hero)

            last_point_y = 0
            last_point_y = self.__draw_map(map, last_point_y)
            last_point_y = self.__draw_statistic(map, hero, last_point_y)
            last_point_y = self.__draw_guide(last_point_y)


            key = self.__get_input()

            if key == ord('d'):
                hero.move(1, 0)
            elif key == ord('a'):
                hero.move(-1, 0)
            elif key == ord('w'):
                hero.move(0, -1)
            elif key == ord('s'):
                hero.move(0, 1)
            elif key == ord('e'):
                self.__display_inventory(hero)
            elif key == ord('f'):

                pick_notifications = hero.pick_up_item()
                if pick_notifications is not None:
                    notifications += pick_notifications

            elif key == ord('r') and enemy is not None:

                notification = hero.attack(enemy)
                if notification is not None:
                    notifications.append(notification)

                if enemy.is_dead:
                    notifications.append(Notification("Вы убили врага!", 10))
                    map.spawn_key(enemy.position)
                    enemy = None

            elif key == ord('q'):
                break
            
            if enemy is not None:
                enemy.move_random()
                enemy.attack(hero)

            if hero.is_dead:
                self.__lose_screen()
                break
            
            hero_exit = hero.on_exit()
            if hero_exit[0]:
                self.__win_screen()
                break
            elif not hero_exit[0] and hero_exit[1] is not None:
                notifications.append(hero_exit[1])
                time.sleep(1)

            self.__display_notification(notifications, last_point_y)

            self.stdscr.refresh()

    def __display_inventory(self, hero):
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

    def __display_notification(self, notifications, last_point_y):
        for i in range(5):
                self.stdscr.addstr(last_point_y + 1 + i, 0, " " * 50)
        for i, notification in enumerate(notifications):
                self.stdscr.addstr(last_point_y + 1 + i, 0, notification.text)
                if notification.lifetime > 0:
                    notification.lifetime -= 1
                else:
                    notifications.remove(notification)


    def __win_screen(self):
        # Инициализация цветовых пар
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)

        # Текст "ПОБЕДА!" большими буквами
        victory_text = [
            "██████╗  ██████╗ ██████╗ ███████╗██████╗  █████╗ ",
            "██╔══██╗██╔═══██╗██╔══██╗██╔════╝██╔══██╗██╔══██╗",
            "██████╔╝██║   ██║██████╔╝█████╗  ██████╔╝███████║",
            "██╔═══╝ ██║   ██║██╔═══╝ ██╔══╝  ██╔═══╝ ██╔══██║",
            "██║     ╚██████╔╝██║     ███████╗██║     ██║  ██║",
            "╚═╝      ╚═════╝ ╚═╝     ╚══════╝╚═╝     ╚═╝  ╚═╝",
        ]

        footer_text = "✧ Нажмите 'пробел' для выхода ✧"

        # Украшения
        decorations = "✨ 🌟 💫 ⭐ ⚝ ✯ ✨ 🌟 💫 ⭐ ⚝ ✯"
        sparkles = "｡･ﾟﾟ･｡･ﾟ✧･ﾟ･｡･ﾟﾟ･｡･ﾟ✧･ﾟ･｡"

        # Центрирование текста
        screen_height, screen_width = self.stdscr.getmaxyx()
        start_y = (screen_height - len(victory_text)) // 2
        start_x = (screen_width - len(victory_text[0])) // 2

        animation_counter = 0
        while True:
            self.stdscr.clear()

            # Отрисовка верхних и нижних украшений
            for i, char in enumerate(decorations):
                color = 3 + ((i + animation_counter) % 4)
                try:
                    # Верхние украшения
                    self.stdscr.addstr(start_y - 2, start_x + i * 4, char, curses.color_pair(color))
                    # Нижние украшения
                    self.stdscr.addstr(start_y + len(victory_text) + 2, start_x + i * 4, char, curses.color_pair(color))
                except curses.error:
                    pass

            # Отрисовка боковых мерцающих искр
            for i, spark in enumerate(sparkles):
                color = 3 + ((i + animation_counter) % 4)
                try:
                    # Левая сторона
                    self.stdscr.addstr(start_y + i % len(victory_text), start_x - 6, spark, curses.color_pair(color))
                    # Правая сторона
                    self.stdscr.addstr(start_y + i % len(victory_text), start_x + len(victory_text[0]) + 4, spark, curses.color_pair(color))
                except curses.error:
                    pass

            # Отрисовка текста "ПОБЕДА!"
            for i, line in enumerate(victory_text):
                try:
                    self.stdscr.addstr(start_y + i, start_x, line, curses.color_pair(5 if i % 2 == 0 else 6))
                except curses.error:
                    pass

            # Отрисовка текста для выхода
            try:
                self.stdscr.addstr(start_y + len(victory_text) + 4, start_x - len(footer_text) // 2 + len(victory_text[0]) // 2, footer_text, curses.color_pair(4))
            except curses.error:
                pass

            self.stdscr.refresh()
            animation_counter += 1

            # Проверка выхода
            key = self.__get_input()
            if key == ord(' '):
                break

        self.stdscr.clear()


    def __lose_screen(self):

        # Инициализация цветовых пар
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)

        # Текст "ПРОИГРЫШЬ!" большими буквами
        lose_text = [
            "██████╗ ██████╗  ██████╗ ██╗ ██████╗ ██████╗ ██╗  ██╗",
            "██╔══██╗██╔══██╗██╔═══██╗██║██╔════╝ ██╔══██╗██║  ██║",
            "██████╔╝██████╔╝██║   ██║██║██║  ███╗██████╔╝███████║",
            "██╔═══╝ ██╔═══╝ ██║   ██║██║██║   ██║██╔═══╝ ╚════██║",
            "██║     ██║     ╚██████╔╝██║╚██████╔╝██║          ██║",
            "╚═╝     ╚═╝      ╚═════╝ ╚═╝ ╚═════╝ ╚═╝          ╚═╝",
        ]

        footer_text = "✧ Нажмите 'пробел' для выхода ✧"

        # Украшения
        decorations = "💧 😢 💔 ⚰️ 🥀 💀 💧 😢 💔 ⚰️ 🥀 💀"
        sparkles = "｡･ﾟﾟ･｡･ﾟ✧･ﾟ･｡･ﾟﾟ･｡･ﾟ✧･ﾟ･｡"

        # Центрирование текста
        screen_height, screen_width = self.stdscr.getmaxyx()
        start_y = (screen_height - len(lose_text)) // 2
        start_x = (screen_width - len(lose_text[0])) // 2

        animation_counter = 0
        while True:
            self.stdscr.clear()

            # Отрисовка верхних и нижних украшений
            for i, char in enumerate(decorations):
                color = 3 + ((i + animation_counter) % 4)
                try:
                    # Верхние украшения
                    self.stdscr.addstr(start_y - 2, start_x + i * 4, char, curses.color_pair(color))
                    # Нижние украшения
                    self.stdscr.addstr(start_y + len(lose_text) + 2, start_x + i * 4, char, curses.color_pair(color))
                except curses.error:
                    pass

            # Отрисовка боковых мерцающих искр
            for i, spark in enumerate(sparkles):
                color = 3 + ((i + animation_counter) % 4)
                try:
                    # Левая сторона
                    self.stdscr.addstr(start_y + i % len(lose_text), start_x - 6, spark, curses.color_pair(color))
                    # Правая сторона
                    self.stdscr.addstr(start_y + i % len(lose_text), start_x + len(lose_text[0]) + 4, spark, curses.color_pair(color))
                except curses.error:
                    pass

            # Отрисовка текста "ПРОИГРЫШЬ!"
            for i, line in enumerate(lose_text):
                try:
                    self.stdscr.addstr(start_y + i, start_x, line, curses.color_pair(5 if i % 2 == 0 else 6))
                except curses.error:
                    pass

            # Отрисовка текста для выхода
            try:
                self.stdscr.addstr(start_y + len(lose_text) + 4, start_x - len(footer_text) // 2 + len(lose_text[0]) // 2, footer_text, curses.color_pair(4))
            except curses.error:
                pass

            self.stdscr.refresh()
            animation_counter += 1

            # Проверка выхода
            key = self.__get_input()
            if key == ord(' '):
                break

        self.stdscr.clear()


    def __draw_inventory_slot(self, x, y, item=None):

        self.stdscr.addstr(y, x, "╔═══╗")
        if item is not None:
            self.stdscr.addstr(y + 1, x, f"║ {item.view} ║")
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
        return last_point_y + 1


    def __draw_statistic(self, map, hero, last_point_y):
        statistics = [
                f"╔" + "═" * (map.width+2) + "╗",
                f"║ {'Статистика'.center(map.width)} ║",
                f"║ {('Здоровье:' + str(hero.current_health) + '/' + str(hero.max_health)).ljust(map.width)} ║",
                f"║ {('█' * int((hero.current_health / hero.max_health) * map.width) + '░' * (map.width - int((hero.current_health / hero.max_health) * map.width))).ljust(map.width)} ║",
                f"║ {('Оружие: ' + str('Нету' if hero.weapon is None else hero.weapon.name)).ljust(map.width)} ║",
                f"╚" + "═" * (map.width+2) + "╝",
                ]

        for y, string in enumerate(statistics):
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
                last_point_y += 1
        return last_point_y
    

    def __draw_guide(self, last_point_y):

        guide = [
                "Управление:",
                "w - вверх, s - вниз, a - влево, d - вправо",
                "e - инвентарь, f - подобрать, r - атаковать",
                "q - выход"
            ]

        for y, string in enumerate(guide):
                self.stdscr.addstr(last_point_y + 1, 0, string)
                last_point_y += 1
        self.stdscr.refresh()
        return last_point_y