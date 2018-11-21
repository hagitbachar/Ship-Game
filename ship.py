############################################################
# Helper class
############################################################


class Direction:
    """
    Class representing a direction in 2D world.
    You may not change the name of any of the constants (UP, DOWN, LEFT, RIGHT,
     NOT_MOVING, VERTICAL, HORIZONTAL, ALL_DIRECTIONS), but all other
     implementations are for you to carry out.
    """
    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'

    NOT_MOVING = 'NOT_MOVING'

    VERTICAL = (UP, DOWN)
    HORIZONTAL = (LEFT, RIGHT)

    ALL_DIRECTIONS = (UP, DOWN, LEFT, RIGHT)


############################################################
# Class definition
############################################################

import ship_helper as sh


class Ship:
    """
    A class representing a ship in Battleship game.
    A ship is 1-dimensional object that could be laid in either horizontal or
    vertical alignment. A ship sails on its vertical\horizontal axis back and
    forth until reaching the board's boarders and then changes its direction to
    the opposite (left <--> right, up <--> down).
    If a ship is hit in one of its coordinates, it ceases its movement in all
    future turns.
    A ship that had all her coordinates hit is considered terminated.
    """

    def __init__(self, pos, length, direction, board_size):
        """
        A constructor for a Ship object
        :param pos: A tuple representing The ship's head's (x, y) position
        :param length: Ship's length
        :param direction: Initial direction in which the ship is sailing
        :param board_size: Board size in which the ship is sailing
        """
        self.__pos = list(pos)
        self.__length = length
        self.__direction = direction
        self.__board_size = board_size
        self.__first_direction = direction
        self.__ship_cells = self.__length * [False]


    def __repr__(self):
        """
        Return a string representation of the ship.
        :return: A tuple converted to string (that is, for a tuple x return
            str(x)).
        The tuple's content should be (in the exact following order):
            1. A list of all the ship's coordinates.
            2. A list of all the ship's hit coordinates.
            3. Last sailing direction.
            4. The size of the board in which the ship is located.
        """
        damaged_coordinates = (self.damaged_cells())
        ship_direction = sh.direction_repr_str(Direction, self.__direction)
        board_size = self.__board_size

        return str((self.coordinates(), damaged_coordinates,
                    ship_direction, board_size))


    def move(self):
        """
        Make the ship move one board unit.
        Movement is in the current sailing direction, unless such movement
        would take the ship outside of the board, in which case the ship
        switches direction and sails one board unit in the new direction.
        :return: A direction object representing the current movement
        direction.
        """
        if self.__direction in Direction.VERTICAL:
            if self.__direction == Direction.UP:
                if self.__pos[1] == 0:
                    self.__pos[1] += 1
                    self.__direction = Direction.DOWN

                else:
                    self.__pos[1] -= 1

            elif self.__direction == Direction.DOWN:
                if self.__pos[1] + self.__length >= self.__board_size:
                    self.__pos[1] -= 1
                    self.__direction = Direction.UP

                else:
                    self.__pos[1] += 1

        elif self.__direction in Direction.HORIZONTAL:
            if self.__direction == Direction.LEFT:
                if self.__pos[0] == 0:
                    self.__pos[0] += 1
                    self.__direction = Direction.RIGHT

                else:
                    self.__pos[0] -= 1

            elif self.__direction == Direction.RIGHT:
                if self.__pos[0] + self.__length >= self.__board_size:
                    self.__pos[0] -= 1
                    self.__direction = Direction.LEFT

                else:
                    self.__pos[0] += 1

        return self.__direction


    def hit(self, pos):
        """
        Inform the ship that a bomb hit a specific coordinate. The ship updates
         its state accordingly.
        If one of the ship's body's coordinate is hit, the ship does not move
         in future turns. If all ship's body's coordinate are hit, the ship is
         terminated and removed from the board.
        :param pos: A tuple representing the (x, y) position of the hit.
        :return: True if the bomb generated a new hit in the ship, False
         otherwise.
        """
        ship_coordinates = self.coordinates()
        for i in range(self.__length):
            if pos == ship_coordinates[i]:
                self.__direction = Direction.NOT_MOVING

                if self.__ship_cells[i]:
                    return False

                else:
                    self.__ship_cells[i] = True
                    return True
        return False


    def terminated(self):
        """
        :return: True if all ship's coordinates were hit in previous turns,
        False otherwise.
        """
        damaged_list = self.damaged_cells()
        if len(damaged_list) == self.__length:
            return True

        else:
            return False


    def __contains__(self, pos):
        """
        Check whether the ship is found in a specific coordinate.
        :param pos: A tuple representing the coordinate for check.
        :return: True if one of the ship's coordinates is found in the
        give (x, y) coordinate, False otherwise.
        """
        if pos in self.coordinates():
            return True

        else:
            return False


    def coordinates(self):
        """
        Return ship's current coordinates on board.
        :return: A list of (x, y) tuples representing the ship's current
        occupying coordinates.
        """
        list_coordinates = []
        if self.__first_direction in Direction.VERTICAL:

            for i in range(self.__length):
                one_coordinates = (self.__pos[0], self.__pos[1] + i)
                list_coordinates.append(one_coordinates)

        if self.__first_direction in Direction.HORIZONTAL:

            for i in range(self.__length):
                one_coordinates = (self.__pos[0] + i, self.__pos[1])
                list_coordinates.append(one_coordinates)

        return list_coordinates


    def damaged_cells(self):
        """
        Return the ship's hit positions.
        :return: A list of tuples representing the (x, y) coordinates of the
         ship which were hit in past turns (If there are no hit coordinates,
         return an empty list). There is no importance to the order of the
         values in the returned list.
        """
        damaged = []
        ship_coordinates = self.coordinates()

        for i in range(self.__length):
            if self.__ship_cells[i]:
                damaged.append(ship_coordinates[i])

        return damaged


    def direction(self):
        """
        Return the ship's current sailing direction.
        :return: One of the constants of Direction class :
         [UP, DOWN, LEFT, RIGHT] according to current sailing direction or
         NOT_MOVING if the ship is hit and not moving.
        """

        return self.__direction


    def cell_status(self, pos):
        """
        Return the status of the given coordinate (hit\not hit) in current ship.
        :param pos: A tuple representing the coordinate to query.
        :return:
            if the given coordinate is not hit : False
            if the given coordinate is hit : True
            if the coordinate is not part of the ship's body : None
        """
        ship_coordinates = self.coordinates()
        for i in range(self.__length):
            if pos == ship_coordinates[i]:
                return self.__ship_cells[i]

        return None
