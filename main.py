import curses
from interface import *
from game import *
import json


def main(stdscr):
    
    interface = Interface(stdscr)

    while True:
        user_choice = interface.draw_menu()
        
        if user_choice == 2:
            break
            
        if user_choice == 0:
            
            with open('settings.json', 'r') as f:
                settings = json.load(f)
            
            game = Game(settings['map_width'], settings['map_height'], 
                    settings['room_count'], settings["room_width"], 
                    settings["room_height"])

            interface = Interface(stdscr, game)
            interface.draw_map()

        elif user_choice == 1:
            settings = interface.draw_settings()

            if settings is not None:
                with open('settings.json', 'w') as f:
                    json.dump(settings, f)

            interface.draw_menu()

    stdscr.clear()
    stdscr.refresh()

curses.wrapper(main)


        
