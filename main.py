import curses
from interface import *
from game import *
import json


def main(stdscr):

    Game(stdscr)
    
curses.wrapper(main)


        
