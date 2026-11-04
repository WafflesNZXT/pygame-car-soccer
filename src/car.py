"""Car movement is independent of rendering, so it can be tested headlessly."""
import math
from dataclasses import dataclass
from .physics import Vec, axes, clamp
from .settings import GRAVITY, FLOOR, CEILING, LEFT, RIGHT

@dataclass
class Controls:
    move: float = 0
    rotate: float = 0
    jump: bool = False
    boost: bool = False

class Car:
    half = Vec(38, 17)
    mass = 4

    def __init__(self, player):
        self.player = player
        self.reset()

    def reset(self):
        self.pos = Vec(350 if self.player == 0 else 930, FLOOR - 17)
        self.vel = Vec()
        self.angle = 0 if self.player == 0 else math.pi
        self.facing = 1 if self.player == 0 else -1
        self.boost = 100
        self.grounded = True
        self.boosting = False
        self.wheel = 0

    def update(self, dt, control):
        if control.move: self.facing = 1 if control.move > 0 else -1
        if self.grounded:
            # Ground travel remains readable even when the sprite faces left.
            self.angle = 0 if self.facing == 1 else math.pi
            self.vel.x += control.move * 1450 * dt
            self.vel.x *= math.exp(-(1.1 if control.move else 5.5) * dt)
            self.vel.x = clamp(self.vel.x, -560, 560)
        else:
            self.angle = (self.angle + control.rotate * 3.9 * dt) % math.tau
            self.vel.x += control.move * 180 * dt
        if control.jump and self.grounded:
            self.vel.y = -580
            self.grounded = False
        self.boosting = control.boost and self.boost > 0
        if self.boosting:
            direction, _ = axes(self.angle)
            self.vel = self.vel + direction * (1450 * dt)
            self.boost = max(0, self.boost - 29 * dt)
        else:
            self.boost = min(100, self.boost + (24 if self.grounded else 7) * dt)
        self.vel.y += GRAVITY * dt
        speed = self.vel.length()
        if speed > 1050: self.vel = self.vel * (1050 / speed)
        self.pos = self.pos + self.vel * dt
        self.wheel += self.vel.x * dt / 12
        self.constrain()

    def constrain(self):
        u, v = axes(self.angle)
        ex = abs(u.x) * self.half.x + abs(v.x) * self.half.y
        ey = abs(u.y) * self.half.x + abs(v.y) * self.half.y
        self.grounded = False
        if self.pos.y + ey >= FLOOR:
            self.pos.y = FLOOR - ey
            self.vel.y = min(0, self.vel.y)
            self.grounded = True
        if self.pos.y - ey < CEILING:
            self.pos.y = CEILING + ey
            self.vel.y = max(0, self.vel.y) * .5
        if self.pos.x - ex < LEFT:
            self.pos.x = LEFT + ex
            self.vel.x = max(0, self.vel.x) * .4
        if self.pos.x + ex > RIGHT:
            self.pos.x = RIGHT - ex
            self.vel.x = min(0, self.vel.x) * .4
