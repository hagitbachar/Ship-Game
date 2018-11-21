def direction_repr_str(direction_class, direction):
    """
    Converts a direction to string.
    :param direction: The direction to convert to string. Should be one of the
     constants of the Direction class ([UP, DOWN, LEFT, RIGHT, NOT_MOVING)
    :return: A string representation for a valid direction input or the string
    'UNKNOWN' if the input direction is not valid.
    """
    if direction == direction_class.NOT_MOVING:
        return 'NOT MOVING'
    elif direction == direction_class.UP:
        return 'UP'
    elif direction == direction_class.DOWN:
        return 'DOWN'
    elif direction == direction_class.LEFT:
        return 'LEFT'
    elif direction == direction_class.RIGHT:
        return 'RIGHT'
    else:
        return 'UNKNOWN'
