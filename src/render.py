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
        # Cached architectural ribs, stands, and pitch perspective lines.
        for x in range(160, 1200, 160):
            pygame.draw.line(surface, (37,68,91), (640,130), (x,445), 3)
            pygame.draw.line(surface, (20,45,67), (640,135), (x+8,445), 6)
        for y in (220, 270, 320, 370, 420):
            pygame.draw.line(surface, (65,92,113), (70,y), (1210,y), 2)
        for x in range(100, 1250, 120):
            pygame.draw.line(surface, (30,78,96), (640,450), (x,638), 1)
        for x, color in ((LEFT,CYAN),(RIGHT,ORANGE)):
            pygame.draw.line(surface, (20,55,74), (x-7,GOAL_TOP), (x-7,FLOOR), 12)
            pygame.draw.line(surface, color, (x,GOAL_TOP), (x,FLOOR), 3)
        return surface

    def car(self, screen, car, time, scale=1):
        sprite = pygame.Surface((160, 90), pygame.SRCALPHA)
        color = getattr(car, 'paint', CYAN if car.player == 0 else ORANGE)
        style = getattr(car, 'cosmetics', {})
        body = style.get('body', 0)
        shade = lambda factor: tuple(min(255, int(c * factor)) for c in color)
        if style.get('underglow', 0):
            glow = [(0,0,0), (70,220,255), (255,70,180), (255,205,70)][style['underglow']]
            pygame.draw.ellipse(sprite, (*glow, 85), (35, 60, 90, 12))
        if car.boosting:
            colors = [(255,136,46), (55,180,255), (200,120,255), (255,90,150)]
            boost_color = colors[style.get('boost_style', 0)]
            length = 23 + 9 * math.sin(time * 35)
            pygame.draw.polygon(sprite, boost_color, [(39,40), (39-length,45), (39,50)])
            pygame.draw.polygon(sprite, (255,245,190), [(39,43), (26-length*.5,45), (39,47)])
        roofs = [[(49,35),(62,21),(91,21),(109,35)], [(47,35),(68,24),(100,25),(112,35)], [(53,35),(64,17),(91,17),(105,35)], [(47,35),(57,22),(96,22),(110,35)]]
        roof = roofs[body]
        pygame.draw.polygon(sprite, (8,14,24), [(37,39),(48,33),*roof[1:3],(110,33),(122,40),(121,57),(37,57)])
        pygame.draw.polygon(sprite, shade(.48), [(39,39),(50,34),*roof[1:3],(109,34),(120,40),(119,53),(39,53)])
        pygame.draw.polygon(sprite, shade(.78), [(40,39),(51,34),*roof[1:3],(109,35),(119,40),(117,47),(41,47)])
        pygame.draw.polygon(sprite, shade(1.12), [(42,39),(53,35),(109,35),(116,39),(100,41),(49,41)])
        pygame.draw.polygon(sprite, (18,43,58), [roof[1],roof[2],(103,35),(56,35)])
        pygame.draw.line(sprite, (155,208,225), (roof[1][0]+3, roof[1][1]+2), (roof[2][0]-2, roof[2][1]+2), 2)
        pygame.draw.line(sprite, (77,115,132), (80,25), (82,35), 2)
        pygame.draw.line(sprite, shade(.36), (43,50), (116,50), 2)
        pygame.draw.line(sprite, (202,230,239), (109,40), (118,40), 3)
        pygame.draw.line(sprite, (255,76,85), (39,40), (43,40), 3)
        pygame.draw.line(sprite, (14,24,33), (38,55), (120,55), 3)
        decal = style.get('decal', 0)
        if decal == 1:
            pygame.draw.line(sprite, (235,240,248), (63,44), (92,44), 2)
            pygame.draw.line(sprite, (235,240,248), (63,47), (92,47), 2)
        elif decal == 2:
            pygame.draw.lines(sprite, (235,240,248), False, [(68,42),(75,47),(68,51)], 2)
        elif decal == 3:
            pygame.draw.lines(sprite, (255,230,100), False, [(81,41),(76,46),(82,46),(78,51)], 2)
        wheel_style = style.get('wheels', 0)
        for x in (54, 105):
            pygame.draw.circle(sprite, (5,9,15), (x,54), 12)
            pygame.draw.circle(sprite, (49,62,76), (x,54), 9, 2)
            rim = [(133,155,175),(210,220,230),(74,231,255),(255,204,106)][wheel_style]
            pygame.draw.circle(sprite, rim, (x,54), 7)
            pygame.draw.circle(sprite, (25,37,49), (x,54), 5)
            spokes = [3,5,4,8][wheel_style]
            for a in range(spokes):
                angle = car.wheel + a * math.tau / spokes
                pygame.draw.line(sprite, rim, (x,54), (x+math.cos(angle)*6,54+math.sin(angle)*6), 1)
            pygame.draw.circle(sprite, (235,244,248), (x,54), 2)
        if math.cos(car.angle) < 0: sprite = pygame.transform.flip(sprite, False, True)
        rotated = pygame.transform.rotate(sprite, -math.degrees(car.angle))
        if scale != 1:
            rotated = pygame.transform.smoothscale(rotated, (int(rotated.get_width()*scale), int(rotated.get_height()*scale)))
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
        pygame.draw.ellipse(screen, (5,14,25), (center[0]-22,FLOOR-7,44,8))
        for radius in range(ball.radius, 0, -1):
            shade = int(140 + 85*(1-radius/ball.radius))
            pygame.draw.circle(screen, (shade, min(255,shade+7), min(255,shade+12)), (center[0]-int((ball.radius-radius)*.27), center[1]-int((ball.radius-radius)*.32)), radius)
        points = [(center[0]+math.cos(ball.angle+a*math.tau/5)*10,
                   center[1]+math.sin(ball.angle+a*math.tau/5)*10) for a in range(5)]
        pygame.draw.polygon(screen, (39, 64, 81), points)
        for x, y in points:
            d = math.atan2(y-center[1], x-center[0])
            pygame.draw.line(screen, (77, 105, 119), (x, y), (center[0]+math.cos(d)*22, center[1]+math.sin(d)*22), 2)
        pygame.draw.circle(screen, (255, 255, 255), (center[0]-7, center[1]-9), 4)
