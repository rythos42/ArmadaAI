import pygame
import math
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

            self.__generate_masks()

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

    def place(self, screen_x, screen_y):
        self.rect.move_ip(screen_x, screen_y)

        width_diff_one_side = (self.arcs_rect.width - self.rect.width) / 2
        height_diff_one_side = (self.arcs_rect.height - self.rect.height) / 2
        self.arcs_rect.move_ip(screen_x - width_diff_one_side, screen_y - height_diff_one_side)

    def yaw_left(self, clicks):
        self.__yaw(clicks, "left")

    def yaw_right(self, clicks):
        self.__yaw(clicks, "right")

    def __yaw(self, clicks, direction):
        if(clicks == 1):
            degrees = 20
        elif(clicks == 2):
            degrees = 45
        else:
            raise ValueError("`clicks` can only be 1 or 2.")

        if(direction == "left"):
            pass
        elif(direction == "right"):
            degrees = degrees * -1
        else:
            raise ValueError("`direction` can only be `left` or `right`.")

        old_rect = self.rect.copy()

        # rotate image
        rotated_image = pygame.transform.rotate(self.ship, degrees)
        new_rect = rotated_image.get_rect()

        # if upsidedown, place the front of the ship at the place it was before rotating
        new_rect.y = self.rect.bottom - new_rect.height if self.facing > 0 else self.rect.y

        # place the new center y of the image at a point on the triangle created by the rotation of the sin(degrees) * hypotenus_length
        (new_center_x, new_center_y) = new_rect.center
        opposite = math.fabs(math.sin(math.radians(degrees)) * self.rect.width)
        opposite = opposite if self.facing < 0 else opposite * -1
        new_rect.centerx = new_center_x
        new_rect.centery = new_center_y - opposite

        # place the edge we rotated around at the edge of the original rect, left happens by default
        new_rect.x = self.rect.x if direction == "left" else self.rect.right - new_rect.width

        # set class variables
        self.ship = rotated_image
        self.rect = new_rect

        # rotate arcs
        self.arcs = pygame.transform.rotate(self.arcs, degrees)
        self.arcs_rect = self.arcs.get_rect()
        self.arcs_rect.center = new_rect.center

        # regenerate masks
        self.__generate_masks()

    def clone(self):
        clone_ship = Ship(self.name, self.player_id, self.facing, self.ship, self.arcs, True)
        clone_ship.black_mask = self.black_mask
        clone_ship.rect = self.rect.copy()
        clone_ship.arcs_rect = self.arcs_rect.copy()
        return clone_ship

    def __generate_masks(self):
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
