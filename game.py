import math


class Game:
    def __init__(self, first_player_ship, second_player_ship, player_turn, logger):
        self.first_player_ship = first_player_ship
        self.second_player_ship = second_player_ship
        self.logger = logger
        self.player_turn = player_turn

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
            ship.move_yaw(move_item[1])
        self.player_turn = self.player_turn + 1

    def clone(self):
        return Game(self.first_player_ship.clone(), self.second_player_ship.clone(), self.player_turn, self.logger)

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

    def write_ai_log_file(self, message):
        self.logger.write(message)

    def get_best_move_for_first_player(self):
        return self.__get_best_move_for_first_player(-2, 2)

    def __get_best_move_for_first_player(self, alpha, beta):
        max_game_value = -2
        move = None

        if(self.is_finished()):
            self.write_ai_log_file("Finished")
            return self.evaluate()

        for trying_move in self.first_player_ship.get_available_moves():
            self.write_ai_log_file(
                f"Trying {trying_move} for {self.first_player_ship.name} at turn {self.player_turn}.")

            imaginary_game = self.clone()
            imaginary_game.do_move(imaginary_game.first_player_ship, trying_move)

            if(self.__does_move_turn_away(self.first_player_ship, imaginary_game.first_player_ship, self.second_player_ship)):
                self.write_ai_log_file("Move turned away, discounting.")
                continue

            self.logger.increment_tabs()
            (game_value, unused_move) = imaginary_game.__get_best_move_for_second_player(alpha, beta)
            self.logger.decrement_tabs()

            self.write_ai_log_file(
                f"Move {trying_move} at turn {self.player_turn} for {self.first_player_ship.name} got value {game_value}.")

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
            self.write_ai_log_file(
                f"Trying {trying_move} for {self.second_player_ship.name} at turn {self.player_turn}.")

            imaginary_game = self.clone()
            imaginary_game.do_move(imaginary_game.second_player_ship, trying_move)

            if(self.__does_move_turn_away(self.second_player_ship, imaginary_game.second_player_ship, self.first_player_ship)):
                self.write_ai_log_file("Move turned away, discounting.")
                continue

            self.logger.increment_tabs()
            (game_value, unused_moved) = imaginary_game.__get_best_move_for_first_player(alpha, beta)
            self.logger.decrement_tabs()

            self.write_ai_log_file(
                f"Move {trying_move} at turn {self.player_turn} for {self.second_player_ship.name} got value {game_value}.")

            if(game_value < min_game_value):
                min_game_value = game_value
                move = trying_move

            if(min_game_value <= alpha):
                return (min_game_value, move)

            if(min_game_value < beta):
                beta = min_game_value

        return (min_game_value, move)

    def does_move_turn_away(self, player_ship_original, player_ship_final, opponent_ship):
        return self.__does_move_turn_away(player_ship_original, player_ship_final, opponent_ship)

    def __does_move_turn_away(self, player_ship_original, player_ship_final, opponent_ship):
        # This is a really naive plan that only checks if the distance of the shorter of the nearest and furthest corners of the ships has increased
        original_corner_distance_1 = math.hypot(
            player_ship_original.rect.right - opponent_ship.rect.left, player_ship_original.rect.y - opponent_ship.rect.y)
        original_corner_distance_2 = math.hypot(
            player_ship_original.rect.left - opponent_ship.rect.right, player_ship_original.rect.y - opponent_ship.rect.y)
        shortest_original_distance = min(original_corner_distance_1, original_corner_distance_2)

        final_corner_distance_1 = math.hypot(
            player_ship_final.rect.right - opponent_ship.rect.left, player_ship_final.rect.y - opponent_ship.rect.y)
        final_corner_distance_2 = math.hypot(
            player_ship_final.rect.left - opponent_ship.rect.right, player_ship_final.rect.y - opponent_ship.rect.y)
        shortest_final_distance = min(final_corner_distance_1, final_corner_distance_2)

        return shortest_final_distance > shortest_original_distance
