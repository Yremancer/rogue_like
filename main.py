import curses
from game import *


def main(stdscr):

    Game(stdscr)
    
curses.wrapper(main)


        
