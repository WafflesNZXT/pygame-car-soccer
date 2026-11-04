import math
import random
import unittest
from src.physics import Vec, circle_box, box_contact
from src.car import Car, Controls
from src.ball import Ball
from src.arena import Arena
from src.match import Match
from src.settings import STEP, LEFT, RIGHT, FLOOR, GOAL_TOP

class PhysicsTests(unittest.TestCase):
    def test_inside_contact_has_normal(self):
        normal, depth = circle_box(Vec(), 23, Vec(), .7, Vec(38, 17))
        self.assertAlmostEqual(normal.length(), 1)
        self.assertGreater(depth, 23)

    def test_rotated_box_and_miss(self):
        self.assertIsNotNone(circle_box(Vec(0, 40), 23, Vec(), math.pi/2, Vec(38, 17)))
        self.assertIsNone(circle_box(Vec(100, 100), 23, Vec(), 0, Vec(38, 17)))

    def test_jump_requires_ground(self):
        car = Car(0)
        car.update(STEP, Controls(jump=True))
        self.assertLess(car.vel.y, -500)
        old = car.vel.y
        car.update(STEP, Controls(jump=True))
        self.assertGreater(car.vel.y, old)

    def test_boost_depletes_and_refills(self):
        car = Car(0)
        car.update(.1, Controls(boost=True))
        self.assertLess(car.boost, 100)
        before = car.boost
        car.update(.1, Controls())
        self.assertGreater(car.boost, before)

    def test_floor_bounce(self):
        ball = Ball()
        ball.pos, ball.vel = Vec(640, FLOOR-10), Vec(20, 300)
        Arena().collide(ball)
        self.assertEqual(ball.pos.y, FLOOR-ball.radius)
        self.assertLess(ball.vel.y, 0)

    def test_wall_and_goal_opening(self):
        ball = Ball()
        ball.pos, ball.vel = Vec(LEFT, 250), Vec(-200, 0)
        self.assertIsNone(Arena().collide(ball))
        self.assertGreater(ball.vel.x, 0)
        ball.pos = Vec(LEFT-24, 510)
        self.assertEqual(Arena().collide(ball), 1)
        ball.pos = Vec(RIGHT+24, 510)
        self.assertEqual(Arena().collide(ball), 0)

    def test_whole_ball_crosses_line(self):
        ball = Ball()
        ball.pos = Vec(LEFT-10, 510)
        self.assertIsNone(Arena().collide(ball))

    def test_post_deflects_ball(self):
        ball = Ball()
        ball.pos, ball.vel = Vec(LEFT+15, GOAL_TOP+10), Vec(-200, -100)
        self.assertIsNone(Arena().collide(ball))
        self.assertGreater(ball.vel.x, 0)

    def test_car_impulse(self):
        ball, car = Ball(), Car(0)
        ball.pos, ball.vel = Vec(400, 610), Vec()
        car.pos, car.vel = Vec(350, 610), Vec(500, 0)
        self.assertTrue(ball.hit_car(car))
        self.assertGreater(ball.vel.x, 0)
        self.assertLess(car.vel.x, 500)

    def test_car_car_contact(self):
        a, b = Car(0), Car(1)
        b.pos = a.pos + Vec(50, 0)
        self.assertIsNotNone(box_contact(a, b))
        b.pos.x += 150
        self.assertIsNone(box_contact(a, b))

class MatchTests(unittest.TestCase):
    def test_kickoff_freezes_timer(self):
        match = Match()
        for _ in range(301): match.step(STEP, [Controls(), Controls()])
        self.assertEqual(match.phase, 'play')
        self.assertEqual(match.remaining, 90)

    def test_goal_scores_once_and_resets(self):
        match = Match()
        match.phase = 'play'
        match.ball.pos = Vec(RIGHT+30, 510)
        self.assertEqual(match.step(STEP, [Controls(), Controls()]), 0)
        self.assertEqual(match.scores, [1, 0])
        time = match.remaining
        for _ in range(290): match.step(STEP, [Controls(), Controls()])
        self.assertEqual(match.scores, [1, 0])
        self.assertEqual(match.phase, 'kickoff')
        self.assertEqual(match.ball.pos.x, 640)
        self.assertEqual(match.remaining, time)

    def test_timer_ends_match(self):
        match = Match()
        match.phase, match.remaining = 'play', STEP/2
        match.step(STEP, [Controls(), Controls()])
        self.assertEqual(match.phase, 'over')
        self.assertEqual(match.remaining, 0)

    def test_final_tick_goal_celebrates_then_ends(self):
        match = Match()
        match.phase, match.remaining = 'play', STEP/2
        match.ball.pos = Vec(RIGHT+30, 510)
        match.step(STEP, [Controls(), Controls()])
        self.assertEqual(match.phase, 'goal')
        for _ in range(290): match.step(STEP, [Controls(), Controls()])
        self.assertEqual(match.phase, 'over')

    def test_seeded_full_match_stays_finite(self):
        rng = random.Random(42)
        match = Match()
        for i in range(60000):
            controls = [Controls(rng.choice([-1, 0, 1]), rng.choice([-1, 0, 1]), rng.random()<.03, rng.random()<.6) for _ in range(2)]
            match.step(STEP, controls)
            for body in [*match.cars, match.ball]:
                self.assertTrue(all(math.isfinite(v) for v in (body.pos.x, body.pos.y, body.vel.x, body.vel.y)))
            if match.phase == 'over': break
        self.assertEqual(match.phase, 'over')

if __name__ == '__main__': unittest.main()
