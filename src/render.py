"""Original procedural stadium, car sprites, ball seams and animation."""
import math
import random
import pygame
from .settings import *
from .physics import axes

class Renderer:
    def __init__(self):
        self.background = self.build_stadium()
        self.trail = []

    def build_stadium(self):
        surface = pygame.Surface((WIDTH, HEIGHT))
        for y in range(HEIGHT):
            t = y / HEIGHT
            pygame.draw.line(surface, (int(7 + 9*t), int(13 + 13*t), int(31 + 14*t)), (0, y), (WIDTH, y))
        rng = random.Random(12)
        for y in range(185, 420, 18):
            for x in range(90, 1200, 18):
                color = rng.choice([(30, 57, 83), (32, 82, 106), (51, 40, 78), (72, 62, 93)])
                pygame.draw.rect(surface, color, (x, y, 4, 3))
        for x in range(100, 1240, 180):
            pygame.draw.polygon(surface, (15, 33, 55), [(x, 125), (x+45, 125), (x+180, 450), (x+130, 450)])
        pygame.draw.rect(surface, (12, 29, 45), (LEFT, 450, RIGHT-LEFT, FLOOR-450))
        for x in range(LEFT, RIGHT, 64): pygame.draw.line(surface, (21, 45, 61), (x, 450), (x, FLOOR))
        for y in range(450, FLOOR, 32): pygame.draw.line(surface, (21, 45, 61), (LEFT, y), (RIGHT, y))
        pygame.draw.line(surface, (46, 76, 91), (640, 450), (640, FLOOR), 2)
        pygame.draw.ellipse(surface, (46, 76, 91), (525, 495, 230, 130), 2)
        pygame.draw.rect(surface, (20, 39, 59), (0, FLOOR, WIDTH, 80))
        pygame.draw.line(surface, (85, 132, 152), (LEFT, FLOOR), (RIGHT, FLOOR), 3)
        for x, color in [(LEFT, CYAN), (RIGHT, ORANGE)]:
            pygame.draw.line(surface, color, (x, CEILING), (x, GOAL_TOP), 4)
            start = 8 if x == LEFT else RIGHT
            pygame.draw.rect(surface, (18, 39, 60), (start, GOAL_TOP, 56, FLOOR-GOAL_TOP))
            for yy in range(GOAL_TOP, FLOOR, 17): pygame.draw.line(surface, (41, 66, 86), (start, yy), (start+56, yy))
            for xx in range(start, start+57, 14): pygame.draw.line(surface, (41, 66, 86), (xx, GOAL_TOP), (xx, FLOOR))
            pygame.draw.line(surface, color, (start, GOAL_TOP), (start+56, GOAL_TOP), 5)
            pygame.draw.circle(surface, WHITE, (x, GOAL_TOP), 6)
        pygame.draw.line(surface, (66, 105, 139), (LEFT, CEILING), (RIGHT, CEILING), 3)
        return surface

    def car(self, screen, car, time):
        sprite = pygame.Surface((136, 80), pygame.SRCALPHA)
        color = CYAN if car.player == 0 else ORANGE
        # Local +x is always the nose. Mirroring vertical art keeps left-facing cars upright.
        if car.boosting:
            flame = 30 + 12 * math.sin(time * 57)
            pygame.draw.polygon(sprite, (255, 100, 47), [(33, 33), (33-flame, 40), (33, 47)])
            pygame.draw.polygon(sprite, (255, 235, 139), [(33, 36), (14-flame*.35, 40), (33, 44)])
        pygame.draw.polygon(sprite, color, [(30, 32), (44, 27), (53, 15), (82, 15), (97, 30), (107, 34), (105, 51), (32, 51)])
        pygame.draw.polygon(sprite, (17, 45, 66), [(52, 27), (58, 19), (79, 19), (89, 28)])
        pygame.draw.line(sprite, (183, 246, 255), (60, 20), (78, 20), 2)
        pygame.draw.rect(sprite, (18, 42, 61), (39, 38, 48, 6), border_radius=3)
        pygame.draw.rect(sprite, (250, 250, 213), (100, 33, 6, 6), border_radius=2)
        pygame.draw.rect(sprite, (239, 80, 104), (30, 33, 4, 7))
        for x in (46, 90):
            pygame.draw.circle(sprite, (5, 10, 22), (x, 45), 12)
            pygame.draw.circle(sprite, (102, 130, 155), (x, 45), 7)
            for a in range(3):
                angle = car.wheel + a * math.tau / 3
                pygame.draw.line(sprite, (21, 37, 56), (x, 45), (x + math.cos(angle)*7, 45+math.sin(angle)*7), 2)
        if math.cos(car.angle) < 0: sprite = pygame.transform.flip(sprite, False, True)
        rotated = pygame.transform.rotate(sprite, -math.degrees(car.angle))
        screen.blit(rotated, rotated.get_rect(center=(round(car.pos.x), round(car.pos.y))))

    def draw(self, screen, match, time, dt, active):
        screen.blit(self.background, (0, 0))
        ball = match.ball
        if active:
            self.trail.append([ball.pos.x, ball.pos.y, .18])
        for p in self.trail: p[2] -= dt
        self.trail = [p for p in self.trail if p[2] > 0][-24:]
        for x, y, life in self.trail:
            pygame.draw.circle(screen, (34, 63, 81), (round(x), round(y)), max(1, int(16*life/.18)))
        for car in match.cars:
            shadow_x = round(car.pos.x)
            pygame.draw.ellipse(screen, (5, 14, 25), (shadow_x-40, FLOOR-6, 80, 10))
            self.car(screen, car, time)
        center = (round(ball.pos.x), round(ball.pos.y))
        pygame.draw.circle(screen, (49, 91, 108), center, 27, 2)
        pygame.draw.circle(screen, (229, 239, 237), center, ball.radius)
        points = [(center[0]+math.cos(ball.angle+a*math.tau/5)*10,
                   center[1]+math.sin(ball.angle+a*math.tau/5)*10) for a in range(5)]
        pygame.draw.polygon(screen, (39, 64, 81), points)
        for x, y in points:
            d = math.atan2(y-center[1], x-center[0])
            pygame.draw.line(screen, (77, 105, 119), (x, y), (center[0]+math.cos(d)*22, center[1]+math.sin(d)*22), 2)
        pygame.draw.circle(screen, (255, 255, 255), (center[0]-7, center[1]-9), 4)
