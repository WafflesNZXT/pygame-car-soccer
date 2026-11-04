"""Pygame shell: events once per frame, simulation at 120 Hz, drawing at 60 FPS."""
import argparse
import math
import pygame
from .settings import *
from .car import Controls
from .match import Match
from .physics import axes
from .render import Renderer
from .particles import Particles
from .menus import Menus
from .ui import UI
from .progression import Profiles, COLORS, level_info
from .customization import OPTIONS

def read_controls(keys, jumps):
    """Convert held keys and jump edges to two independent control snapshots."""
    return [Controls(keys[pygame.K_d]-keys[pygame.K_a], keys[pygame.K_s]-keys[pygame.K_w], jumps[0], keys[pygame.K_LSHIFT]),
            Controls(keys[pygame.K_RIGHT]-keys[pygame.K_LEFT], keys[pygame.K_DOWN]-keys[pygame.K_UP], jumps[1], keys[pygame.K_RSHIFT] or keys[pygame.K_RCTRL])]

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Neon Kickoff | Local Car Soccer')
        self.clock = pygame.time.Clock()
        self.ui = UI()
        self.menus = Menus(self.ui)
        self.renderer = Renderer()
        self.match = Match()
        self.profiles = Profiles()
        self.rewards = [0, 0]
        self.results_start = 0
        self.particles = Particles()
        self.state, self.back = 'menu', 'menu'
        self.buttons = []
        self.running = True
        self.accumulator = self.time = 0
        self.jumps = [False, False]

    def action(self, action):
        if action == 'quit': self.running = False
        elif action == 'play':
            self.match = Match()
            self.particles = Particles()
            self.renderer.trail.clear()
            self.state = 'play'
        elif action == 'resume': self.state = 'play'
        elif action in ('garage', 'stats'): self.state = action
        elif action.startswith('item:'):
            _, key, player = action.split(':')
            profile = self.profiles.players[int(player)]
            choices = OPTIONS[key]
            current = profile[key]
            # Cycle every option, but equip only items already unlocked.
            level = level_info(profile['total_xp'])[0]
            for step in range(1, len(choices)+1):
                candidate = (current+step) % len(choices)
                if choices[candidate][1] <= level:
                    profile[key] = candidate
                    break
            self.profiles.save()
        elif action.startswith('color'):
            i = int(action[-1])
            profile = self.profiles.players[i]
            level = level_info(profile['total_xp'])[0]
            for step in range(1, len(COLORS) + 1):
                choice = (profile['color'] + step) % len(COLORS)
                if COLORS[choice][2] <= level:
                    profile['color'] = choice
                    break
            self.profiles.save()
        elif action == 'controls': self.back, self.state = self.state, 'controls'
        elif action == 'back': self.state = self.back
        elif action == 'menu': self.state = 'menu'
        self.accumulator = 0
        self.jumps = [False, False]

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            elif event.type == pygame.WINDOWFOCUSLOST and self.state == 'play':
                self.state = 'pause'
                self.accumulator = 0
                self.jumps = [False, False]
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect, action in self.buttons:
                    if rect.collidepoint(event.pos): self.action(action); break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == 'play': self.state = 'pause'; self.accumulator = 0
                    elif self.state == 'pause': self.action('resume')
                    elif self.state == 'controls': self.action('back')
                    elif self.state in ('garage', 'stats'): self.action('menu')
                    else: self.action('menu')
                elif self.state == 'play':
                    if event.key == pygame.K_SPACE: self.jumps[0] = True
                    if event.key == pygame.K_RETURN: self.jumps[1] = True
                elif event.key == pygame.K_RETURN:
                    self.action('back' if self.state == 'controls' else 'resume' if self.state == 'pause' else 'play')
                elif event.key == pygame.K_c and self.state != 'controls': self.action('controls')

    def update(self, dt):
        self.time += dt
        if self.state != 'play': return
        keys = pygame.key.get_pressed()
        self.accumulator += dt
        while self.accumulator >= STEP:
            inputs = read_controls(keys, self.jumps)
            scorer = self.match.step(STEP, inputs)
            self.jumps = [False, False]
            if scorer is not None:
                self.particles.emit(self.match.ball.pos, CYAN if scorer == 0 else ORANGE, 180, True)
            for car in self.match.cars:
                if car.boosting and self.match.phase == 'play':
                    direction, _ = axes(car.angle)
                    self.particles.emit(car.pos-direction*42, CYAN if car.player == 0 else ORANGE, direction=direction)
            self.particles.update(STEP)
            self.accumulator -= STEP
        if self.match.phase == 'over':
            self.rewards = self.profiles.reward(self.match.scores)
            self.results_start = self.time
            self.state = 'over'

    def draw(self, dt):
        for i, car in enumerate(self.match.cars):
            car.paint = COLORS[self.profiles.players[i]['color']][1]
            car.cosmetics = self.profiles.players[i]
        self.renderer.draw(self.screen, self.match, self.time, dt if self.state == 'play' else 0, self.state == 'play')
        self.particles.draw(self.screen)
        self.ui.hud(self.screen, self.match)
        self.buttons = []
        if self.state != 'play':
            self.buttons = self.menus.draw(self.screen, self.state, self.match, pygame.mouse.get_pos(), self.profiles, self.rewards, self.renderer, self.time, self.results_start)
        elif self.match.phase == 'kickoff':
            self.ui.text(self.screen, str(max(1, math.ceil(self.match.delay))), (640, 310), 100)
            self.ui.text(self.screen, 'GET READY', (640, 385), 28, CYAN)
        elif self.match.phase == 'goal':
            self.ui.text(self.screen, 'GOAL!', (640, 290 + math.sin(self.time*9)*5), 100,
                         CYAN if self.match.scorer == 0 else ORANGE)
            self.ui.text(self.screen, f'PLAYER {self.match.scorer+1} SCORES', (640, 365), 36)
        if self.profiles.error:
            self.ui.text(self.screen, self.profiles.error, (640, 705), 24, (255, 110, 100))
        pygame.display.flip()

    def run(self, frames=None, screenshot=None):
        count = 0
        try:
            while self.running:
                dt = min(self.clock.tick(FPS) / 1000, .05)
                self.events()
                self.update(dt)
                self.draw(dt)
                count += 1
                if frames and count >= frames: break
            if screenshot: pygame.image.save(self.screen, screenshot)
        finally: pygame.quit()


def run():
    parser = argparse.ArgumentParser(description='Neon Kickoff: two-player car soccer')
    parser.add_argument('--smoke', type=int, metavar='FRAMES', help='exit after N frames (for headless checks)')
    parser.add_argument('--screenshot', help='save final rendered frame as PNG')
    parser.add_argument('--play', action='store_true', help='start directly in a match')
    args = parser.parse_args()
    game = Game()
    if args.play: game.action('play')
    game.run(args.smoke, args.screenshot)
