import os
import pygame
import screen_board
from ship import Ship
from game import Game
from logger import Logger


pygame.init()


os.environ['SDL_VIDEO_WINDOW_POS'] = "75, 27"
screen = pygame.display.set_mode([screen_board.SCREEN_WIDTH, screen_board.SCREEN_HEIGHT],
                                 pygame.HWSURFACE | pygame.DOUBLEBUF)
map = pygame.transform.scale(pygame.image.load("img/map_scarif_shieldgate_v3.jpg"),
                             (screen_board.SCREEN_WIDTH, screen_board.SCREEN_HEIGHT))
ship = pygame.image.load("img/ship_munificent noFade.png").convert_alpha()
arcs = pygame.image.load("img/arcs_v5_munificent.png").convert_alpha()
clock = pygame.time.Clock()

original_ship_rect = ship.get_rect()
original_arcs_rect = arcs.get_rect()
ship = pygame.transform.scale(ship, (int(original_ship_rect.width / screen_board.SCALING),
                                     int(original_ship_rect.height / screen_board.SCALING)))
arcs = pygame.transform.scale(arcs, (int(original_arcs_rect.width / screen_board.SCALING),
                                     int(original_arcs_rect.height / screen_board.SCALING)))


first_player_ship = Ship("First", 0, 180, ship, arcs)
second_player_ship = Ship("Second", 1, 0, ship, arcs)

top_yaw_1_left_ship = Ship("Top yaw left 1", 2, 180, ship, arcs)
top_yaw_1_right_ship = Ship("Top yaw right 1", 3, 180, ship, arcs)
bottom_yaw_1_left_ship = Ship("Bottom yaw left 1", 4, 0, ship, arcs)
bottom_yaw_1_right_ship = Ship("Bottom yaw right 1", 5, 0, ship, arcs)

# ships = [first_player_ship, second_player_ship, top_yaw_1_left_ship,
#         top_yaw_1_right_ship, bottom_yaw_1_left_ship, bottom_yaw_1_right_ship]
ships = [first_player_ship, second_player_ship]

first_player_ship.place(screen_board.SCREEN_MIDDLE, screen_board.SCREEN_DISTANCE_3_TOP - first_player_ship.rect.height)
top_yaw_1_left_ship.place(screen_board.SCREEN_MIDDLE, screen_board.SCREEN_DISTANCE_3_TOP -
                          top_yaw_1_left_ship.rect.height)
top_yaw_1_left_ship.move_yaw(-1)
top_yaw_1_right_ship.place(screen_board.SCREEN_MIDDLE, screen_board.SCREEN_DISTANCE_3_TOP -
                           top_yaw_1_right_ship.rect.height)
top_yaw_1_right_ship.move_yaw(1)

second_player_ship.place(screen_board.SCREEN_MIDDLE - 300, screen_board.SCREEN_DISTANCE_3_BOTTOM)
bottom_yaw_1_left_ship.place(screen_board.SCREEN_MIDDLE - 300, screen_board.SCREEN_DISTANCE_3_BOTTOM)
bottom_yaw_1_left_ship.move_yaw(-1)
bottom_yaw_1_right_ship.place(screen_board.SCREEN_MIDDLE - 300, screen_board.SCREEN_DISTANCE_3_BOTTOM)
bottom_yaw_1_right_ship.move_yaw(1)

logger = Logger()
logger.set_writing_log(True)
the_game = Game(first_player_ship, second_player_ship, 0, logger)

clone_ship = second_player_ship.clone()
second_player_ship.move(0)
second_player_ship.move(0)

#print(the_game.does_move_turn_away(clone_ship, second_player_ship, first_player_ship))


def draw_screen():
    screen.blit(map, (0, 0))
    for ship in ships:
        ship.draw(screen)
    pygame.draw.line(screen, screen_board.COLOUR_WHITE, (0, screen_board.SCREEN_DISTANCE_3_TOP),
                     (screen_board.SCREEN_WIDTH, screen_board.SCREEN_DISTANCE_3_TOP))
    pygame.draw.line(screen, screen_board.COLOUR_WHITE, (0, screen_board.SCREEN_DISTANCE_3_BOTTOM),
                     (screen_board.SCREEN_WIDTH, screen_board.SCREEN_DISTANCE_3_BOTTOM))
    pygame.display.flip()


draw_screen()

running = True
end_of_game_waiting = True
while not the_game.is_finished() and running:
    player_turn_id = the_game.get_player_turn_id()
    pressed_key = None
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False
            end_of_game_waiting = False
        if(event.type == pygame.KEYUP):
            pressed_key = event.key

    if player_turn_id == 0:
        (unused_value, move) = the_game.get_best_move_for_first_player()
        the_game.do_move(first_player_ship, move)
        print(f"Turn {the_game.player_turn}: {first_player_ship.name} moved {move} to {first_player_ship.rect.y}. {second_player_ship.name} is at {second_player_ship.rect.y}. ")
    else:
        player_distance = 0

        if(pressed_key == pygame.K_1 or pressed_key == pygame.K_KP1):
            player_distance = 1
        elif(pressed_key == pygame.K_2 or pressed_key == pygame.K_KP2):
            player_distance = 2
        elif(pressed_key == pygame.K_3 or pressed_key == pygame.K_KP3):
            player_distance = 3

        if(player_distance != 0):
            the_game.do_move(second_player_ship, player_distance)
            print(f"Turn {the_game.player_turn}: {second_player_ship.name} moved {player_distance} to {second_player_ship.rect.y}. {first_player_ship.name} is at {first_player_ship.rect.y}.")

    draw_screen()
    clock.tick(100)

winner = the_game.get_winner_ship(True)
if winner == None:
    print("Tie")
else:
    print(f"Winner: {the_game.get_winner_ship().name}.")
    print(f"{the_game.get_current_player_ship().name} starts it's turn and shoots.")
print(f"{first_player_ship.name} Ship at: {first_player_ship.rect.y}.")
print(f"{second_player_ship.name} Ship at: {second_player_ship.rect.y}.")

while end_of_game_waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end_of_game_waiting = False

pygame.quit()
