import pygame
import screen_board


class Ship(pygame.sprite.Sprite):
    def __init__(self, name, player_id, facing, ship, arcs, clone=False):
        self.name = name
        self.player_id = player_id
        self.facing = facing
        self.ship = ship
        self.arcs = arcs
        self.rect = ship.get_rect()
        self.mask = pygame.mask.from_surface(self.ship)
        self.ship_mask = self.mask
        self.arcs_rect = self.arcs.get_rect()

        if(not clone):
            if(facing > 0):
                self.ship = pygame.transform.rotate(self.ship, 180)
                self.arcs = pygame.transform.rotate(self.arcs, 180)

            self.generate_masks()

    def is_overlapping(self, other_ship):
        return pygame.sprite.collide_mask(self, other_ship) != None

    def is_within_black_range(self, other_ship):
        ship_rect = self.rect
        self.rect = self.arcs_rect
        self.mask = self.black_mask

        in_black_range = pygame.sprite.collide_mask(self, other_ship)

        self.mask = self.ship_mask
        self.rect = ship_rect

        return in_black_range != None

    def move(self, distance):
        # facing is -1 or 1, which defines which direction the ship is moving
        screen_move_distance = distance * screen_board.STRAIGHT_LINE_MOVE_DISTANCE * self.facing
        self.rect.move_ip(0, screen_move_distance)
        self.arcs_rect.move_ip(0, screen_move_distance)

    def direct_move(self, screen_x, screen_y):
        self.rect.move_ip(screen_x, screen_y)

        width_diff_one_side = (self.arcs_rect.width - self.rect.width) / 2
        height_diff_one_side = (self.arcs_rect.height - self.rect.height) / 2
        self.arcs_rect.move_ip(screen_x - width_diff_one_side, screen_y - height_diff_one_side)

    def clone(self):
        clone_ship = Ship(self.name, self.player_id, self.facing, self.ship, self.arcs, True)
        clone_ship.black_mask = self.black_mask
        clone_ship.rect = self.rect.copy()
        clone_ship.arcs_rect = self.arcs_rect.copy()
        return clone_ship

    def generate_masks(self):
        black = (0, 0, 0)
        no_alpha_arcs = self.arcs.convert()
        no_alpha_arcs.set_colorkey(black)

        # mask set of all non-black pixels (including "transparent", convert() doesn't keep transparency)
        non_black_mask = pygame.mask.from_surface(no_alpha_arcs)

        # mask set of all black pixels (including "transparent")
        non_black_mask.invert()

        # mask set of only pixels with any colour
        transparent_mask = pygame.mask.from_surface(self.arcs, 0)

        # mask set of the AND of all of the "black" pixels (black+transparent) and the mask of just the transparent pixels
        self.black_mask = non_black_mask.overlap_mask(transparent_mask, (0, 0))
