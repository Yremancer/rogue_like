from map import *
from characters import *
from interface import *
import json


class Game:

    interface: Interface
    map: Map
    hero: Hero
    enemy: Enemy

    def __init__(self, stdscr):
        self.interface = Interface(stdscr)
        self.__launch_game()


    def __launch_game(self):

        while True:
            user_choice = self.interface.display_menu()
            
            if user_choice == 2:
                break
                
            if user_choice == 0:
                
                with open('settings.json', 'r') as f:
                    settings = json.load(f)
                
                self.map = Map(settings['room_count'], settings['map_width'], settings['map_height'], settings['room_width'], settings['room_height'])
                self.hero = Hero("hero", self.map)
                self.enemy = Enemy("enemy", self.map)
                self.interface.display_game(self.map, self.hero, self.enemy)

            elif user_choice == 1:
                settings = self.interface.display_settings()

                if settings is not None:
                    with open('settings.json', 'w') as f:
                        json.dump(settings, f)

                self.interface.display_menu()

        

        
    
