from .physics import Vec, clamp, circle_box
from .settings import BALL_RADIUS, GRAVITY

class Ball:
    radius = BALL_RADIUS

    def __init__(self): self.reset()

    def reset(self):
        self.pos, self.vel = Vec(640, 350), Vec()
        self.angle = 0

    def update(self, dt):
        self.vel.y += GRAVITY * .8 * dt
        self.vel = self.vel * (1 - .045 * dt)
        speed = self.vel.length()
        if speed > 1350: self.vel = self.vel * (1350 / speed)
        self.pos = self.pos + self.vel * dt
        self.angle += self.vel.x * dt / self.radius

    def hit_car(self, car):
        contact = circle_box(self.pos, self.radius, car.pos, car.angle, car.half)
        if not contact: return False
        normal, penetration = contact
        self.pos = self.pos + normal * (penetration + .1)
        relative = (self.vel - car.vel).dot(normal)
        if relative < 0:
            impulse = -(1 + .83) * relative / (1 + 1 / car.mass)
            self.vel = self.vel + normal * impulse
            car.vel = car.vel - normal * (impulse / car.mass)
        return True
