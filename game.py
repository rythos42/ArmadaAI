class Game:
    # incremented each time a player takes a move
    # 0, 2, 4, 6, 8, 10 are first_player_ship turns and 1, 3, 5, 7, 9, 11 are second_player_ship turns
    player_turn = 0
    ai_log_file = None
    tabs = 0
    is_writing_ai_log_file = False

    def __init__(self, first_player_ship, second_player_ship):
        self.first_player_ship = first_player_ship
        self.second_player_ship = second_player_ship

    def is_finished(self):
        return (self.first_player_ship.is_overlapping(self.second_player_ship)
                or self.first_player_ship.is_within_black_range(self.second_player_ship)
                or self.first_player_ship.is_off_table() or self.second_player_ship.is_off_table()
                or self.player_turn == 12)

    def get_player_turn_id(self):
        return 0 if self.player_turn % 2 == 0 else 1

    def get_current_player_ship(self):
        player_turn_id = self.get_player_turn_id()
        return next((ship for ship in [self.first_player_ship, self.second_player_ship] if ship.player_id == player_turn_id), None)

    def is_player_turn(self, ship):
        return self.get_player_turn_id() == ship.player_id

    def get_winner_ship(self, final=False):
        if(final):
            self.write_ai_log_file("Final")

        if(self.first_player_ship.is_overlapping(self.second_player_ship)):
            self.write_ai_log_file(f"Tie by overlap.")
            return None

        if(self.first_player_ship.is_off_table()):
            self.write_ai_log_file(f"Second player wins by opponent off table.")
            return self.second_player_ship

        if(self.second_player_ship.is_off_table()):
            self.write_ai_log_file(f"First player wins by opponent off table.")
            return self.first_player_ship

        if(self.first_player_ship.is_within_black_range(self.second_player_ship)):
            if(self.is_player_turn(self.first_player_ship)):
                self.write_ai_log_file(f"First player wins by black range.")
                return self.first_player_ship
            else:
                self.write_ai_log_file(f"Second player wins by black range.")
                return self.second_player_ship

        self.write_ai_log_file(f"No winner yet.")
        return None

    def do_move(self, ship, move):
        for move_item in move:
            ship.move(1)
            ship.yaw(move_item[1])
        self.player_turn = self.player_turn + 1

    def clone(self):
        clone_game = Game(self.first_player_ship.clone(),
                          self.second_player_ship.clone())
        clone_game.player_turn = self.player_turn
        clone_game.tabs = self.tabs
        clone_game.ai_log_file = self.ai_log_file
        clone_game.is_writing_ai_log_file = self.is_writing_ai_log_file
        return clone_game

    def evaluate(self):
        winner_ship = self.get_winner_ship()
        if(winner_ship == None):
            self.write_ai_log_file(f"Returning (0, 0).")
            return (0, 0)
        if(winner_ship.player_id == self.first_player_ship.player_id):
            self.write_ai_log_file(f"Returning (1, 0).")
            return (1, 0)
        else:
            self.write_ai_log_file(f"Returning (-1, 0).")
            return (-1, 0)

    def set_using_ai_log_file(self, using_ai_log_file):
        self.is_writing_ai_log_file = using_ai_log_file

    def write_ai_log_file(self, message):
        if(not self.is_writing_ai_log_file):
            return

        if(self.ai_log_file == None):
            self.ai_log_file = open("ai.log", "w")

        current_tabs = self.get_tabs()
        self.ai_log_file.write(f"{current_tabs}{message}\n")

    def get_tabs(self):
        return "".rjust(self.tabs, "\t")

    def get_best_move_for_first_player(self):
        return self.__get_best_move_for_first_player(-2, 2)

    def __get_best_move_for_first_player(self, alpha, beta):
        max_game_value = -2
        move = None

        if(self.is_finished()):
            self.write_ai_log_file("Finished")
            return self.evaluate()

        for trying_move in self.first_player_ship.get_available_moves():
            imaginary_game = self.clone()
            imaginary_game.do_move(imaginary_game.first_player_ship, trying_move)

            self.write_ai_log_file(f"Trying {trying_move} for {self.first_player_ship.name}.")

            self.tabs = self.tabs + 1
            (game_value, unused_move) = imaginary_game.__get_best_move_for_second_player(alpha, beta)
            self.tabs = self.tabs - 1

            self.write_ai_log_file(f"Move {trying_move} for {self.first_player_ship.name} got value {game_value}.")

            if (game_value > max_game_value):
                max_game_value = game_value
                move = trying_move

            if (max_game_value >= beta):
                return (max_game_value, move)

            if(max_game_value > alpha):
                alpha = max_game_value

        return (max_game_value, move)

    def __get_best_move_for_second_player(self, alpha, beta):
        min_game_value = 2
        move = None

        if(self.is_finished()):
            self.write_ai_log_file("Finished")
            return self.evaluate()

        for trying_move in self.second_player_ship.get_available_moves():
            self.write_ai_log_file(f"Trying {trying_move} for {self.second_player_ship.name}.")
            self.tabs = self.tabs + 1

            imaginary_game = self.clone()
            imaginary_game.do_move(imaginary_game.second_player_ship, trying_move)

            (game_value, unused_moved) = imaginary_game.get_best_move_for_first_player()

            self.tabs = self.tabs - 1
            self.write_ai_log_file(f"Move {trying_move} for {self.second_player_ship.name} got value {game_value}.")

            if(game_value < min_game_value):
                min_game_value = game_value
                move = trying_move

            if(min_game_value <= alpha):
                return (min_game_value, move)

            if(min_game_value < beta):
                beta = min_game_value

        return (min_game_value, move)
