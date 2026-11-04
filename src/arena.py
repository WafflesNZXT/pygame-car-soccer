"""Arena contact: the goal opening is a real pocket behind each touchline."""
from .settings import LEFT, RIGHT, FLOOR, CEILING, GOAL_TOP
from .physics import Vec

class Arena:
    def collide(self, ball):
        r, p, v = ball.radius, ball.pos, ball.vel
        if p.y + r > FLOOR:
            p.y = FLOOR - r
            v.y = -abs(v.y) * .77 if v.y > 30 else 0
            v.x *= .995
        if p.y - r < CEILING:
            p.y = CEILING + r
            v.y = abs(v.y) * .8
        # Solid side walls above the goal mouth, rounded posts at each opening.
        if p.y < GOAL_TOP:
            if p.x - r < LEFT: p.x, v.x = LEFT + r, abs(v.x) * .85
            if p.x + r > RIGHT: p.x, v.x = RIGHT - r, -abs(v.x) * .85
        for x in (LEFT, RIGHT):
            delta = p - Vec(x, GOAL_TOP)
            if delta.length() < r + 6:
                normal = delta.normalized()
                ball.pos = p = Vec(x, GOAL_TOP) + normal * (r + 6)
                approach = v.dot(normal)
                if approach < 0: ball.vel = v = v - normal * (1.85 * approach)
        # Whole ball must cross the line. Return the scoring player's index.
        if p.y - r >= GOAL_TOP:
            if p.x + r < LEFT: return 1
            if p.x - r > RIGHT: return 0
        return None
