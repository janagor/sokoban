import curses
from src.graphical_interface import GraphicalInterface


def main(stdscr):
    game_session = GraphicalInterface(stdscr)
    game_session.run()


if __name__ == "__main__":
    curses.wrapper(main)
