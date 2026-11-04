"""Fixed-step match state machine, without Pygame dependencies."""
from .car import Car, Controls
from .ball import Ball
from .arena import Arena
from .physics import box_contact
from .settings import MATCH_SECONDS

class Match:
    def __init__(self):
        self.cars = [Car(0), Car(1)]
        self.ball, self.arena = Ball(), Arena()
        self.scores = [0, 0]
        self.remaining = MATCH_SECONDS
        self.phase, self.delay = 'kickoff', 2.5
        self.scorer = None

    def reset_positions(self):
        for car in self.cars: car.reset()
        self.ball.reset()

    def step(self, dt, controls):
        """Return a goal event exactly once; celebration and kickoff freeze the clock."""
        if self.phase == 'over': return None
        if self.phase in ('kickoff', 'goal'):
            self.delay = max(0, self.delay - dt)
            if self.delay <= 0:
                if self.phase == 'goal':
                    if self.remaining <= 0: self.phase = 'over'
                    else:
                        self.reset_positions()
                        self.phase, self.delay = 'kickoff', 2.5
                else: self.phase = 'play'
            return None
        for car, control in zip(self.cars, controls): car.update(dt, control)
        contact = box_contact(*self.cars)
        if contact:
            n, depth = contact
            a, b = self.cars
            a.pos, b.pos = a.pos - n * (depth / 2), b.pos + n * (depth / 2)
            approach = (b.vel - a.vel).dot(n)
            if approach < 0:
                impulse = -.65 * approach
                a.vel, b.vel = a.vel - n * impulse, b.vel + n * impulse
            a.constrain()
            b.constrain()
        self.ball.update(dt)
        for car in self.cars: self.ball.hit_car(car)
        scorer = self.arena.collide(self.ball)
        self.remaining = max(0, self.remaining - dt)
        if scorer is not None:
            self.scores[scorer] += 1
            self.scorer = scorer
            self.phase, self.delay = 'goal', 2.4
            return scorer
        if self.remaining <= 0: self.phase = 'over'
        return None
