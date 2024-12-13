import pygame
from player.states.state_machine import StateMachine
from particle.particle import Particle
from group_picker.group_picker import group_picker
from group_picker.settings import GroupType
from random import uniform, random
from entity.entity import Entity


class Player(Entity):
    def __init__(self, groups, assets, **pos: tuple[int]) -> None:
        super().__init__(groups, 'player', assets, StateMachine, **pos)

        self.jumps = 1

        self._charge = 0
        self._delta_charge = 100
        self._max_charge = 50

    @property
    def charge_fraction(self):
        return self._charge / self._max_charge

    @property
    def charge(self):
        return self._charge

    def self_charge(self, dt, direction: int):
        self._charge = sorted([0, self._charge + direction * dt * self._delta_charge, self._max_charge])[1]

    def generate_particles(self, dt, particles):
        if random() * 8 > self.charge * dt:
            return
        groups = group_picker.get_groups(GroupType.Visible, GroupType.Particles)
        animation = particles['spark']
        velocity = pygame.Vector2(uniform(-50, 50), -30)
        acceleration = pygame.Vector2(0, 0.5)
        pos = self.hitbox.left + random() * self.hitbox.width, self.hitbox.top + random() * self.hitbox.height
        Particle(groups, 'spark', animation, velocity, acceleration, offgrid_tile=True, z=7, center=pos)

    def update(self, dt, events):
        super().update(dt, events)
        self.self_charge(dt, 2 * events['shift'] - 1)
        self.slide_hitbox.center = self.hitbox.center
