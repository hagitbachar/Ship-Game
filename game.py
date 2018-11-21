############################################################
# Imports
############################################################
import game_helper as gh
from ship import *

############################################################
# Class definition
############################################################
THREE_REMAINING_LIFE = 3


class Game:
    """
    A class representing a battleship game.
    A game is composed of ships that are moving on a square board and a user
    which tries to guess the locations of the ships by guessing their
    coordinates.
    """

    def __init__(self, board_size, ships):
        """
        Initialize a new Game object.
        :param board_size: Length of the side of the game-board.
        :param ships: A list of ships (of type Ship) that participate in the
            game.
        :return: A new Game object.
        """
        self.__board_size = board_size
        self.ships = ships
        self.dict_bombs = {}
        self.hit_pos = []


    def placing_a_bomb(self):
        """
        This function gets a position of bomb from user, the life of the bomb
        is three
        """
        bomb = gh.get_target(self.__board_size)

        self.dict_bombs[bomb] = THREE_REMAINING_LIFE

        return bomb


    def move_ships(self):
        """
        This function moves all the ships in every round
        """
        for ship in self.ships:
            Ship.move(ship)


    def hit_ships(self, pos):
        """
        This function checks if the ship damaged, if she damaged
        """
        hits = []
        list_bomb_to_del = []
        for ship in self.ships:
            for bomb in self.dict_bombs:
                if Ship.hit(ship, bomb):
                    list_bomb_to_del.append(bomb)
                    hits.append(pos)
                    self.hit_pos.append(pos)

        for bomb in list_bomb_to_del:
            del self.dict_bombs[bomb]

        return hits


    def update_bombs(self):
        """
        This function updates the life of each bomb
        """
        list_bomb_to_del = []

        for bomb in self.dict_bombs:
            if self.dict_bombs[bomb] >= 1:
                self.dict_bombs[bomb] -= 1

            if self.dict_bombs[bomb] < 1:
                list_bomb_to_del.append(bomb)

        for bomb in list_bomb_to_del:
            del self.dict_bombs[bomb]


    def remove_ships_destroyed(self):
        """
        This function removes all the destroyed ship
        """
        counter = 0
        for ship in self.ships:
            if Ship.terminated(ship):
                counter += 1
                self.ships.remove(ship)

        return counter


    def good_ships_coordinate(self):
        """
        This function creates a list of all the coordinates that don't damaged
        """
        good_ships = []
        for ship in self.ships:
            for coordinate in ship.coordinates():
                if coordinate not in self.hit_pos:
                    good_ships.append(coordinate)

        good_ships = set(good_ships)
        good_ships = list(good_ships)

        return good_ships


    def __play_one_round(self):
        """
        Note - this function is here to guide you and it is *not mandatory*
        to implement it. The logic defined by this function must be implemented
        but if you wish to do so in another function (or some other functions)
        it is ok.

        The function runs one round of the game :
            1. Get user coordinate choice for bombing.
            2. Move all game's ships.
            3. Update all ships and bombs.
            4. Report to the user the result of current round (number of hits
             and terminated ships)
        :return:
            (some constant you may want implement which represents) Game status:
            GAME_STATUS_ONGOING if there are still ships on the board or
            GAME_STATUS_ENDED otherwise.
        """

        self.update_bombs()
        pos = self.placing_a_bomb()
        self.move_ships()
        hits = self.hit_ships(pos)
        good_ships = self.good_ships_coordinate()
        print(gh.board_to_string(self.__board_size, hits,
                                 self.dict_bombs, self.hit_pos, good_ships))
        terminations = self.remove_ships_destroyed()
        gh.report_turn(len(hits), terminations)


    def __repr__(self):
        """
        Return a string representation of the board's game.
        :return: A tuple converted to string (that is, for a tuple x return
            str(x)). The tuple should contain (maintain
        the following order):
            1. Board's size.
            2. A dictionary of the bombs found on the board, mapping their
                coordinates to the number of remaining turns:
                 {(pos_x, pos_y) : remaining turns}
                For example :
                 {(0, 1) : 2, (3, 2) : 1}
            3. A list of the ships found on the board (each ship should be
                represented by its __repr__ string).
        """
        board_size = self.__board_size
        dict_bomb = self.dict_bombs

        return str((board_size, dict_bomb, self.ships))


    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        gh.report_legend()
        initial_empty_hits = []
        good_ships = self.good_ships_coordinate()
        print(gh.board_to_string(self.__board_size, initial_empty_hits,
                                 self.dict_bombs, self.hit_pos, good_ships))
        while len(self.ships) != 0:
            self.__play_one_round()

        gh.report_gameover()


############################################################
# An example usage of the game
############################################################
if __name__ == "__main__":
    game = Game(5, gh.initialize_ship_list(4, 2))
    game.play()
