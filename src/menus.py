"""Keyboard and mouse menus share the same buttons."""
import pygame
from types import SimpleNamespace
from .physics import Vec
from .customization import OPTIONS
from .settings import CYAN, ORANGE, WHITE
from .progression import COLORS, level_info

class Menus:
    def __init__(self, ui): self.ui = ui

    def draw(self, screen, state, match, mouse, profiles=None, rewards=None, renderer=None, time=0, results_start=0):
        veil = pygame.Surface((1280, 720), pygame.SRCALPHA)
        veil.fill((3, 9, 22, 205))
        screen.blit(veil, (0, 0))
        ui = self.ui
        ui.text(screen, 'LOCAL MULTIPLAYER  /  2 PLAYERS', (640, 120), 24, CYAN)
        title = {'menu': 'NEON KICKOFF', 'pause': 'TIME OUT', 'controls': 'TAKE CONTROL', 'over': 'FULL TIME', 'garage': 'GARAGE', 'stats': 'PLAYER STATS'}[state]
        ui.text(screen, title, (640, 188), 100)
        buttons = []
        if state == 'controls':
            ui.panel(screen, (190, 258, 900, 230))
            for index, (name, color, lines) in enumerate([
                ('PLAYER 1', CYAN, ['A / D     Drive', 'W / S     Rotate in air', 'SPACE     Jump', 'LEFT SHIFT     Boost']),
                ('PLAYER 2', ORANGE, ['LEFT / RIGHT     Drive', 'UP / DOWN     Rotate in air', 'ENTER     Jump', 'RIGHT SHIFT / CTRL     Boost'])]):
                x = 420 + index * 440
                ui.text(screen, name, (x, 290), 36, color)
                for row, line in enumerate(lines): ui.text(screen, line, (x, 332 + row * 36), 24)
            ui.text(screen, 'Point your nose with rotation, then boost to fly. Boost refills fastest on the ground.', (640, 524), 24)
            options = [('BACK', 'back')]
        elif state in ('garage', 'stats'):
            for i, profile in enumerate(profiles.players):
                x = 410 + i * 460
                level, progress, needed = level_info(profile['total_xp'])
                ui.panel(screen, (x-200, 235, 400, 320))
                ui.text(screen, f'PLAYER {i+1}  /  LEVEL {level}', (x, 257), 28, CYAN if i == 0 else ORANGE)
                if state == 'garage':
                    if renderer:
                        preview = SimpleNamespace(pos=Vec(x,305), player=i, paint=COLORS[profile['color']][1], cosmetics=profile, boosting=True, angle=0, wheel=time*3)
                        renderer.car(screen, preview, time, 2)
                    labels = [('color', 'PAINT'), *[(key, key.upper().replace('_STYLE','')) for key in OPTIONS]]
                    for row, (key, label) in enumerate(labels):
                        y = 357 + row*30
                        options_list = COLORS if key == 'color' else OPTIONS[key]
                        choice = profile[key]
                        name = options_list[choice][0]
                        next_index = (choice + 1) % len(options_list)
                        required = options_list[next_index][-1]
                        suffix = f'  (NEXT: LV {required})' if required > level else ''
                        rect = pygame.Rect(x-180, y-12, 360, 25)
                        ui.panel(screen, rect)
                        ui.text(screen, f'{label}: {name}{suffix}  >', rect.center, 20)
                        buttons.append((rect, f'color{i}' if key == 'color' else f'item:{key}:{i}'))
                else:
                    ui.text(screen, f'{progress} / {needed} XP   |   TOTAL {profile["total_xp"]}', (x, 345), 24)
                    ui.text(screen, f'W {profile["wins"]}   L {profile["losses"]}   D {profile["draws"]}', (x, 383), 28)
            options = [('BACK', 'menu')]
        else:
            if state == 'over':
                winner = 'DRAW GAME' if match.scores[0] == match.scores[1] else f'PLAYER {1 if match.scores[0] > match.scores[1] else 2} WINS'
                ui.text(screen, f'{winner}    /    {match.scores[0]} : {match.scores[1]}', (640, 260), 48)
                if rewards is not None and profiles is not None:
                    fraction = min(1, max(0, (time-results_start)/2.5))
                    for i, profile in enumerate(profiles.players):
                        x = 360 + i*400
                        before = max(0, profile['total_xp'] - rewards[i])
                        shown = before + int(rewards[i]*fraction)
                        level, progress, required = level_info(shown)
                        ui.text(screen, f'P{i+1}  +{rewards[i]} XP   /   LEVEL {level}', (x, 310), 24, CYAN if i == 0 else ORANGE)
                        pygame.draw.rect(screen, (31,48,65), (x-130, 330, 260, 12), border_radius=5)
                        pygame.draw.rect(screen, CYAN if i == 0 else ORANGE, (x-130, 330, int(260*progress/required), 12), border_radius=5)
                        ui.text(screen, f'{progress} / {required} XP', (x, 357), 20)
                        if level > level_info(before)[0]: ui.text(screen, 'LEVEL UP!', (x, 385), 28, (255,225,100))
            else:
                ui.text(screen, 'Two cars. One ball. Ninety seconds.', (640, 274), 36, (149, 174, 205))
            options = [('RESUME' if state == 'pause' else 'PLAY MATCH', 'resume' if state == 'pause' else 'play'), ('CONTROLS', 'controls'), ('MAIN MENU' if state in ('pause', 'over') else 'QUIT', 'menu' if state in ('pause', 'over') else 'quit')]
        if state == 'menu' and profiles is not None:
            ui.text(screen, f"P1 LEVEL {level_info(profiles.players[0]['total_xp'])[0]}           P2 LEVEL {level_info(profiles.players[1]['total_xp'])[0]}", (640, 310), 24)
            options = [('PLAY MATCH', 'play'), ('GARAGE', 'garage'), ('PLAYER STATS', 'stats'), ('CONTROLS', 'controls'), ('QUIT', 'quit')]
        for i, (label, action) in enumerate(options):
            rect = pygame.Rect(460, 570 if state in ('controls', 'garage', 'stats') else (425 if state == 'over' else 335) + i * (58 if state == 'menu' else 68), 360, 50)
            hovered = rect.collidepoint(mouse)
            ui.panel(screen, rect, (27, 64, 87) if hovered else (16, 30, 51), CYAN if hovered else (55, 79, 105))
            ui.text(screen, label, rect.center, 28)
            buttons.append((rect, action))
        ui.text(screen, 'ENTER  PLAY / RESUME     •     C  CONTROLS     •     ESC  BACK / PAUSE', (640, 662), 20, (139, 160, 189))
        return buttons
