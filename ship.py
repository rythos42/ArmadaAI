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
        self.mask = pygame.mask.from_surface(self.ship)
        self.ship_mask = self.mask

        if(not clone):
            self.ship = pygame.transform.rotate(self.ship, facing)
            self.arcs = pygame.transform.rotate(self.arcs, facing)
            self.__generate_masks()

        self.rect = self.ship.get_rect()
        self.arcs_rect = self.arcs.get_rect()

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
        screen_distance = distance * screen_board.STRAIGHT_LINE_MOVE_DISTANCE

        if(self.facing == 0):   # straight up
            x_move = 0
            y_move = screen_distance * -1
        elif(self.facing == 90):  # straight right
            x_move = screen_distance
            y_move = 0
        elif(self.facing == 180):  # straight down
            x_move = 0
            y_move = screen_distance
        elif(self.facing == 270):  # straight left
            x_move = screen_distance * -1
            y_move = 0
        else:
            # rotation is counter-clockwise
            angle = self.facing % 90    # angle is always comparing against the closest 90deg angle to 0
            amount = self.facing / 90
            adjacent = math.fabs(screen_distance * math.cos(math.radians(angle)))
            opposite = math.fabs(screen_distance * math.sin(math.radians(angle)))

            if(amount < 1):  # upper left
                x_move = opposite * -1
                y_move = adjacent * -1
            elif(amount < 2):  # lower left
                x_move = adjacent * -1
                y_move = opposite
            elif(amount < 3):  # lower right
                x_move = opposite
                y_move = adjacent
            elif(amount < 4):  # upper right
                x_move = adjacent
                y_move = opposite * -1

        self.rect.move_ip(x_move, y_move)
        self.arcs_rect.move_ip(x_move, y_move)

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

        # update the facing, keep the number below 360deg
        self.facing = (self.facing + degrees) % 360
        upsidedown = self.facing > 90 and self.facing < 270

        # rotate image
        rotated_image = pygame.transform.rotate(self.ship, degrees)
        new_rect = rotated_image.get_rect()

        # place the y of the image at a point on the triangle created by the rotation of the sin(degrees) * hypotenus_length
        new_rect.y = self.rect.bottom - new_rect.height if upsidedown else self.rect.y
        opposite = math.fabs(math.sin(math.radians(degrees)) * self.rect.width)
        opposite = opposite * -1 if upsidedown else opposite
        new_rect.y = new_rect.y - opposite

        # place the edge we rotated around at the edge of the original rect
        if(direction == "right"):
            new_rect.x = self.rect.x if upsidedown else self.rect.right - new_rect.width
        else:
            new_rect.x = self.rect.x if not upsidedown else self.rect.right - new_rect.width

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
