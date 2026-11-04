"""Small dependency-free vector and contact helpers, shared by the simulation."""
from dataclasses import dataclass
import math

@dataclass
class Vec:
    x: float = 0
    y: float = 0

    def __add__(self, other): return Vec(self.x + other.x, self.y + other.y)
    def __sub__(self, other): return Vec(self.x - other.x, self.y - other.y)
    def __mul__(self, scalar): return Vec(self.x * scalar, self.y * scalar)
    def dot(self, other): return self.x * other.x + self.y * other.y
    def length(self): return math.hypot(self.x, self.y)
    def normalized(self): return self * (1 / self.length()) if self.length() else Vec(1, 0)


def clamp(value, low, high): return max(low, min(high, value))


def axes(angle):
    return Vec(math.cos(angle), math.sin(angle)), Vec(-math.sin(angle), math.cos(angle))


def circle_box(center, radius, box, angle, half):
    """Return outward normal and penetration of a circle against a rotated box."""
    u, v = axes(angle)
    delta = center - box
    x, y = delta.dot(u), delta.dot(v)
    nearest = Vec(clamp(x, -half.x, half.x), clamp(y, -half.y, half.y))
    offset = Vec(x - nearest.x, y - nearest.y)
    distance = offset.length()
    if distance >= radius: return None
    if distance > 1e-8:
        local = offset * (1 / distance)
        return u * local.x + v * local.y, radius - distance
    # Center inside the body: choose the nearest face rather than a zero normal.
    if half.x - abs(x) < half.y - abs(y):
        return u * (1 if x >= 0 else -1), radius + half.x - abs(x)
    return v * (1 if y >= 0 else -1), radius + half.y - abs(y)


def box_contact(a, b):
    """Separating axis test for two oriented cars; normal points from a to b."""
    au, av = axes(a.angle)
    bu, bv = axes(b.angle)
    best, normal = float('inf'), None
    delta = b.pos - a.pos
    for axis in (au, av, bu, bv):
        ra = abs(axis.dot(au)) * a.half.x + abs(axis.dot(av)) * a.half.y
        rb = abs(axis.dot(bu)) * b.half.x + abs(axis.dot(bv)) * b.half.y
        overlap = ra + rb - abs(delta.dot(axis))
        if overlap <= 0: return None
        if overlap < best:
            best = overlap
            normal = axis * (1 if delta.dot(axis) >= 0 else -1)
    return normal, best
