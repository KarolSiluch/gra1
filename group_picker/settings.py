from enum import Enum


class GroupType(Enum):
    Visible = 0
    Collidable = 1
    Magnets = 2


class InvalidGroupTypeError(Exception):
    pass
