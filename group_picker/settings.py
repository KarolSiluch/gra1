from enum import Enum


class GroupType(Enum):
    Visible = 0
    Collidable = 1


class InvalidGroupTypeError(Exception):
    pass
