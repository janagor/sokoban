import curses
from src.gui import Gui
import argparse
import sys
from src.helpers import colors


def game_session(stdscr, arguments):
    try:
        parser = argparse.ArgumentParser()

        parser.add_argument('--game_color', '-g')
        parser.add_argument('--player_color', '-p')
        args = parser.parse_args(arguments[1:])
        default_color = 'white'
        game_col = default_color
        if args.game_color:
            if args.game_color in colors:
                game_col = args.game_color
        pl_col = default_color
        if args.player_color:
            if args.player_color in colors:
                pl_col = args.player_color

        game = Gui(stdscr, colors[game_col], colors[pl_col])
        game.run()
    except curses.error:
        pass


if __name__ == "__main__":
    curses.wrapper(game_session, sys.argv)
