import curses
from src.game import Game


class GraphicalInterface:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        curses.curs_set(0)
        self.running = True
        self.init_game()

    def init_game(self):
        self.print_start_of_the_game()
        self.game = Game()
        self.print_screen()
        self.stdscr.refresh()

    def print_start_of_the_game(self):
        self.welcome_msg1 = "Welcome in Sokoban game!"
        self.welcome_msg2 = "Press any key to start."
        self.stdscr.addstr(0, 0, self.welcome_msg1)
        self.stdscr.addstr(1, 0, self.welcome_msg2)
        self.stdscr.getch()
        self.stdscr.clear()
        self.stdscr.refresh()

    def print_level_number(self):
        level_statement = f"LEVEL {self.game.cur_state_num}"
        self.stdscr.addstr(0, 1, level_statement)

    def print_map(self, level):
        offset = 2
        for row_index, row in enumerate(level):
            for col_index, cell in enumerate(row):
                self.stdscr.addch(row_index + offset, col_index * 2 + 1, cell)

    def print_help_msg(self, offset):
        offset += 2
        help_msg1 = "PRESS ARROW KEYS OR [hjkl] TO MOVE"
        help_msg2 = "PRESS q TO EXIT"
        help_msg3 = "PRESS r TO RESTART LEVEL"
        help_msg4 = "PRESS w TO GO TO PREVIOUS LEVEL"
        help_msg5 = "PRESS w TO GO TO PREVIOUS LEVEL (IF UNLOCKED)"

        self.stdscr.addstr(offset, 1, help_msg1)
        self.stdscr.addstr(offset + 1, 1, help_msg2)
        self.stdscr.addstr(offset + 2, 1, help_msg3)
        self.stdscr.addstr(offset + 3, 1, help_msg4)
        self.stdscr.addstr(offset + 4, 1, help_msg5)

    def print_num_of_moves_done(self, offset):
        num_of_moves = self.game.cur_state.num_of_done_moves
        msg = f"MOVE COUNT: {num_of_moves}"
        self.stdscr.addstr(offset + 1, 1, msg)

    def print_end_of_the_game(self):
        self.stdscr.clear()
        end_msg1 = "Congratulation! You won the game!"
        end_msg2 = "Press any key to exit the game."
        self.stdscr.addstr(0, 0, end_msg1)
        self.stdscr.addstr(1, 0, end_msg2)
        self.stdscr.getch()
        self.running = False

    def print_screen(self):
        self.stdscr.clear()
        level = self.game.cur_state.map
        self.print_level_number()
        self.print_map(level)
        offset = len(level) + 1
        self.print_num_of_moves_done(offset)
        self.print_help_msg(offset + 1)
        self.stdscr.refresh()

    def handle_input(self, key):
        if key in [
            curses.KEY_UP,
            curses.KEY_DOWN,
            curses.KEY_LEFT,
            curses.KEY_RIGHT,
            ord('h'),
            ord('j'),
            ord('k'),
            ord('l')
        ]:
            self.handle_movement(key)
        elif key == ord('q'):
            self.running = False
        elif key == ord('r'):
            self.game.player.reset_level()
        elif key == ord('w'):
            self.game.player.prev_level()
        elif key == ord('e'):
            self.game.player.next_level()
        self.print_screen()


    def handle_movement(self, key):
        if key in [curses.KEY_UP, ord('k')]:
            self.game.player.move('up')
        elif key in [curses.KEY_DOWN, ord('j')]:
            self.game.player.move('down')
        elif key in [curses.KEY_LEFT, ord('h')]:
            self.game.player.move('left')
        elif key in [curses.KEY_RIGHT, ord('l')]:
            self.game.player.move('right')

    def run(self):
        while self.running:
            key = self.stdscr.getch()
            self.handle_input(key)
            if self.game.is_game_finished:
                self.print_end_of_the_game()
            self.print_screen()
            self.stdscr.refresh()
