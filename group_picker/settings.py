from enum import Enum


class GroupType(Enum):
    Visible = 0
    Collidable = 1
    Magnets = 2
    Background = 3
    Particles = 4
    Enemies = 5
    Attacks = 6


class InvalidGroupTypeError(Exception):
    pass
