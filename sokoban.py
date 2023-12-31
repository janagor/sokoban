import curses
from src.graphical_interface import GraphicalInterface
import argparse
import sys


def main(stdscr, arguments):
    colors = {
        'blue': curses.COLOR_BLUE,
        'cyan': curses.COLOR_CYAN,
        'green': curses.COLOR_GREEN,
        'magenta': curses.COLOR_MAGENTA,
        'red': curses.COLOR_RED,
        'white': curses.COLOR_WHITE,
        'yellow': curses.COLOR_YELLOW
        }
    try:
        parser = argparse.ArgumentParser()

        parser.add_argument('--objects_color')
        parser.add_argument('--players_color')
        args = parser.parse_args(arguments[1:])
        obj_col = 'white'
        if args.objects_color:
            if args.objects_color in colors:
                obj_col = args.objects_color
        pl_col = 'white'
        if args.players_color:
            if args.players_color in colors:
                pl_col = args.players_color

        session = GraphicalInterface(stdscr, colors[obj_col], colors[pl_col])
        session.run()
    except curses.error:
        pass


if __name__ == "__main__":
    curses.wrapper(main, sys.argv)
