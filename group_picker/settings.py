from enum import Enum


class GroupType(Enum):
    Visible = 0
    Collidable = 1
    Magnets = 2
    Background = 3


class InvalidGroupTypeError(Exception):
    pass
