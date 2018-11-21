############################################################
# Imports
############################################################
from random import randrange, choice, Random
from ship import Ship, Direction
import re

############################################################
# Constants
############################################################
BOARD_HIT = '*'
BOARD_SHIP_BODY_INTACT = 'X'
BOARD_SHIP_BODY_HIT = 'O'
BOARD_EMPTY = '_'

LINE_BREAK = '\n'
ROW_DELIMITER = '|'
COLUMN_DELIMITER = '-'

LINE_SEPARATOR = '*'*30 + '\n'
BOARD_LEGEND = LINE_SEPARATOR + 'LEGEND :\n' + \
    LINE_SEPARATOR + \
    BOARD_SHIP_BODY_INTACT + ' : Ship body (not hit)\n' +\
    BOARD_SHIP_BODY_HIT + ' : Ship body (hit)\n' +\
    BOARD_HIT + ' : Hit in last turn\n' +\
    '3\\2\\1 : Life span of bomb\n' +\
    LINE_SEPARATOR

MESSAGE_GET_USER_INPUT = 'Insert x, y coordinate for bomb drop: '
MESSAGE_WRONG_INPUT_FORMAT = 'Wrong input format - input should be two numbers ' \
    'separated by comma, e.g. "1, 4"'
MESSAGE_COORDINATE_OUT_OF_BOUND = 'Coordinate out of bound - min ' \
    'value is: 0, max value is: '
MESSAGE_GAME_OVER = 'All ships were terminated - Well done!'

_rand = Random()


def seed(a=None):
    _rand.seed(a)
############################################################
# Helper functions
############################################################


def report(s):
    """
    Report a message to the user.
    :param s: A string that should be reported to the user.
    :return: None
    """
    print(s)


def board_to_string(board_length, hits, bombs, hit_ships, ships, debug=True):
    """
    Return  a string representation of the boards.
    :param board_length: Length of the board size.
    :param hits: A list of tuples representing the (x, y) coordinates
    that were hit in current turn.
    :param bombs: A dictionary with tuples representing the (x, y) coordinates
    that contain active bombs as keys and an int representing the numbers of
    turns remaining for the current bomb (1-3) as values.
    :param hit_ships: A list of tuples representing the (x, y) coordinates
    in which there are hit ships' body.
    :param ships: A list of tuples representing the (x, y) coordinates
    of ships (that are *not* hit).
    :param debug: If true - print all ships and their body (even those that are
    not hit). If False - print only hit coordinates.
    :return: None
    """
    def make_line(line_number, line):
        """
        Create a regular (not header) line in the board.
        A line consists of a line number, line content and break line.
        For example : '1|__OXX\n'
        :param line_number: The index of the line.
        :param line: A sequence representing the line content.
        :return: A stylized line with prefix of line number and row delimiter.
        """
        return \
            str(line_number) + \
            ROW_DELIMITER + \
            ''.join(line) + \
            LINE_BREAK

    def make_columns_header(line):
        """
        Create a decorated header for the columns. The header includes a
        prefix of 2 spaces ('  ') to be aligned with the rows prefix.
        A sample header is : '  01234' or '  -----'
        :param line : a sequence (or simple string) that should manifest a
         header for columns.
        :return A string representation of the given sequence adjusted
          to be used as columns header.
        """
        return \
            '  ' + \
            ''.join(line) + \
            LINE_BREAK

    if debug:
        inner_board = [[BOARD_EMPTY for i in range(board_length)]
                       for i in range(board_length)]
        for (x, y) in ships:
            inner_board[x][y] = BOARD_SHIP_BODY_INTACT
        for (x, y) in hit_ships:
            inner_board[x][y] = BOARD_SHIP_BODY_HIT
        for x, y in bombs.keys():
            inner_board[x][y] = str(bombs[(x, y)])
        for (x, y) in hits:
            inner_board[x][y] = BOARD_HIT

        def transpose(l):
            """
            Transpose the given 2D list.
            :param l: 2-D square list (list of n lists each with n elements).
            :return: A 2-D list where the (i, j) element in the original list is
                now the (j, i) element.
            """
            return list(map(list, zip(*l)))

        boards_rows = list()
        # Note - the lists contained in inner_board are the boards *columns* (and
        # not as you might intuitively think of them, as the rows). As the board
        # is printed from top left to bottom right, we now transpose the inner
        # board such that its lists will represent the rows.
        for row, line_index in zip(transpose(inner_board), range(board_length)):
            boards_rows.append(make_line(line_index, row))

        boards_rows.insert(0, make_columns_header(COLUMN_DELIMITER*board_length))
        boards_rows.insert(0, make_columns_header(
            ''.join([str(i) for i in range(board_length)])))

        return ''.join(boards_rows)
    else:
        return str((board_length, hits, bombs, hit_ships, ships))

'''
# Example of how to call board_to_string() :
print(board_to_string(5,
                      [(0, 0)],
                      {(0, 4): '1'},
                      [(1, 2), (1, 3)],
                      [(1, 3), (1, 4)],
                      debug=False))
# Example till here
'''

def get_random_ship(max_ship_size):
    """
    Return a random ship
    :param max_ship_size: Ship's maximal allowed size
    :return: A ship with Random parameters
    """
    ship_direction = _rand.choice(Direction.ALL_DIRECTIONS)
    ship_length = _rand.randrange(max_ship_size) + 1  # randrange return a number
    # in the range [0, max_ship_size-1]. We want to allow max_ship_size length
    # ships and don't want to allow 0 length ships, hence the '+1'
    free_pos = _rand.randrange(max_ship_size)  # In the axis in which the ship is
    # 1D, (i.e. not in the orientation axis) the ship could get any coordinate
    # between 0 and board-1)
    if max_ship_size - ship_length == 0:
        axis_pos = 0
    else:
        axis_pos = _rand.randrange(max_ship_size - ship_length)  # At the
        # orientation axis, the ship can only be in this range so her nose
        # doesn't stick out of the board.
    if ship_direction in Direction.HORIZONTAL:
        pos_x, pos_y = axis_pos, free_pos
    elif ship_direction in Direction.VERTICAL:
        pos_y, pos_x = axis_pos, free_pos
    return Ship((pos_x, pos_y), ship_length, ship_direction, max_ship_size+1)


def initialize_ship_list(max_ship_size, number_of_ships, rseed=None):
    """
    A function which generates a random list of ships.
    :param max_ship_size: Maximal allowed ship size.
    :param number_of_ships: Number of ships to initialize.
    :return: A list of random ships.
    """
    if rseed is not None:
        seed(rseed)

    ship_list = []
    for i in range(number_of_ships):
        new_ship = get_random_ship(max_ship_size)
        ship_list.append(new_ship)
    return ship_list


def get_target(board_size):
    """
    The function asks the user for input and returns a coordinate
    (a tuple of (x, y)) representing the requested coordinate. If the input
    coordinate is not in a valid form "number comma space number" ( e.g. "1, 4")
    the function automatically asks the user for additional inputs until a valid
    input is entered.
    If the coordinate is out of the board's bound of an error message is printed
    and  another request for input is made.
    :param board_size : The size of the board.
    :return: A tuple of two numbers.
    """
    # The following regex is designed to test the validity of the input.
    # A valid input includes two numbers separated by a comma. To be more
    # permissive, the regex allows any number of preceding, trailing or
    # between numbers inclusion of spaces.
    # for more information on regex see :
    # https://docs.python.org/3.4/library/re.html
    pattern = re.compile('^( )*[0-9]+( )*,( )*[0-9]+( )*$')
    valid_input = False
    while not valid_input:
        user_input = input(MESSAGE_GET_USER_INPUT)
        while not pattern.match(user_input):
            report(MESSAGE_WRONG_INPUT_FORMAT)
            user_input = input(MESSAGE_GET_USER_INPUT)
        coordinate = tuple([int(x.strip()) for x in user_input.split(',')])
        if min(coordinate) >= 0 and max(coordinate) < board_size:
            valid_input = True
        else:
            report(MESSAGE_COORDINATE_OUT_OF_BOUND + str(board_size-1))
    return coordinate

# Example call to get_target - start
''' get_target(5)'''
# Example call to get_target - end


def report_turn(hits, terminations):
    """
    Print to screen the results of current turn - how many ships were destroyed
    and how many were terminated.
    :param hits: Number of hitsin last turn.
    :param terminations: Number of terminated ships in last turn.
    :return: None
    """
    report('In this turn there were ' + str(hits) + ' hits and ' +
          str(terminations) + ' terminations')


def report_gameover():
    """
    Report to user the game has ended successfully.
    :return: None
    """
    report(MESSAGE_GAME_OVER)


def report_legend():
    """
    Print to screen a message containing the symbols of a game board.
    :return: None
    """
    report(BOARD_LEGEND)
