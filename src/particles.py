"""Bounded, time-based particle effects; no external assets."""
import random
import math
import pygame
from .physics import Vec

class Particles:
    def __init__(self): self.items = []

    def emit(self, pos, color, count=1, explosion=False, direction=None):
        for _ in range(count):
            angle = random.uniform(0, math.tau)
            speed = random.uniform(120, 650) if explosion else random.uniform(25, 100)
            vel = Vec(math.cos(angle), math.sin(angle)) * speed
            if direction is not None: vel = vel + direction * -160
            life = random.uniform(.5, 1.3) if explosion else random.uniform(.15, .4)
            self.items.append([Vec(pos.x, pos.y), vel, life, life, color, random.uniform(2, 6)])
        self.items = self.items[-900:]

    def update(self, dt):
        for p in self.items:
            p[0] = p[0] + p[1] * dt
            p[1].y += 110 * dt
            p[2] -= dt
        self.items = [p for p in self.items if p[2] > 0]

    def draw(self, screen):
        for pos, vel, life, total, color, radius in self.items:
            fade = life / total
            pygame.draw.circle(screen, tuple(int(c * fade) for c in color),
                               (round(pos.x), round(pos.y)), max(1, int(radius * fade)))
