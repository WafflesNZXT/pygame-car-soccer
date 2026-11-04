"""Keyboard and mouse menus share the same buttons."""
import pygame
from .settings import CYAN, ORANGE, WHITE
from .progression import COLORS, level_info

class Menus:
    def __init__(self, ui): self.ui = ui

    def draw(self, screen, state, match, mouse, profiles=None, rewards=None):
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
                ui.panel(screen, (x-200, 270, 400, 235))
                ui.text(screen, f'PLAYER {i+1}  /  LEVEL {level}', (x, 305), 36, CYAN if i == 0 else ORANGE)
                ui.text(screen, f'{progress} / {needed} XP   |   TOTAL {profile["total_xp"]}', (x, 345), 24)
                ui.text(screen, f'W {profile["wins"]}   L {profile["losses"]}   D {profile["draws"]}', (x, 383), 28)
                ui.text(screen, f'PAINT: {COLORS[profile["color"]][0]}', (x, 425), 28, COLORS[profile['color']][1])
                if state == 'garage':
                    rect = pygame.Rect(x-120, 450, 240, 40)
                    ui.panel(screen, rect)
                    ui.text(screen, 'NEXT UNLOCKED PAINT', rect.center, 20)
                    buttons.append((rect, f'color{i}'))
            options = [('BACK', 'menu')]
        else:
            if state == 'over':
                winner = 'DRAW GAME' if match.scores[0] == match.scores[1] else f'PLAYER {1 if match.scores[0] > match.scores[1] else 2} WINS'
                ui.text(screen, f'{winner}    /    {match.scores[0]} : {match.scores[1]}', (640, 260), 48)
                if rewards is not None: ui.text(screen, f'PLAYER 1  +{rewards[0]} XP     |     PLAYER 2  +{rewards[1]} XP', (640, 310), 28)
            else:
                ui.text(screen, 'Two cars. One ball. Ninety seconds.', (640, 274), 36, (149, 174, 205))
            options = [('RESUME' if state == 'pause' else 'PLAY MATCH', 'resume' if state == 'pause' else 'play'), ('CONTROLS', 'controls'), ('MAIN MENU' if state in ('pause', 'over') else 'QUIT', 'menu' if state in ('pause', 'over') else 'quit')]
        if state == 'menu' and profiles is not None:
            ui.text(screen, f"P1 LEVEL {level_info(profiles.players[0]['total_xp'])[0]}           P2 LEVEL {level_info(profiles.players[1]['total_xp'])[0]}", (640, 310), 24)
            options = [('PLAY MATCH', 'play'), ('GARAGE', 'garage'), ('PLAYER STATS', 'stats'), ('CONTROLS', 'controls'), ('QUIT', 'quit')]
        for i, (label, action) in enumerate(options):
            rect = pygame.Rect(460, 570 if state in ('controls', 'garage', 'stats') else 335 + i * (58 if state == 'menu' else 68), 360, 50)
            hovered = rect.collidepoint(mouse)
            ui.panel(screen, rect, (27, 64, 87) if hovered else (16, 30, 51), CYAN if hovered else (55, 79, 105))
            ui.text(screen, label, rect.center, 28)
            buttons.append((rect, action))
        ui.text(screen, 'ENTER  PLAY / RESUME     •     C  CONTROLS     •     ESC  BACK / PAUSE', (640, 662), 20, (139, 160, 189))
        return buttons
