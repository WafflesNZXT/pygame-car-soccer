"""Keyboard and mouse menus share the same buttons."""
import pygame
from .settings import CYAN, ORANGE, WHITE

class Menus:
    def __init__(self, ui): self.ui = ui

    def draw(self, screen, state, match, mouse):
        veil = pygame.Surface((1280, 720), pygame.SRCALPHA)
        veil.fill((3, 9, 22, 205))
        screen.blit(veil, (0, 0))
        ui = self.ui
        ui.text(screen, 'LOCAL MULTIPLAYER  /  2 PLAYERS', (640, 120), 24, CYAN)
        title = {'menu': 'NEON KICKOFF', 'pause': 'TIME OUT', 'controls': 'TAKE CONTROL', 'over': 'FULL TIME'}[state]
        ui.text(screen, title, (640, 188), 100)
        buttons = []
        if state == 'controls':
            ui.panel(screen, (190, 258, 900, 230))
            for index, (name, color, lines) in enumerate([
                ('PLAYER 1', CYAN, ['A / D     Drive', 'W / S     Rotate in air', 'SPACE     Jump', 'LEFT SHIFT     Boost']),
                ('PLAYER 2', ORANGE, ['LEFT / RIGHT     Drive', 'UP / DOWN     Rotate in air', 'ENTER     Jump', 'RIGHT CTRL     Boost'])]):
                x = 420 + index * 440
                ui.text(screen, name, (x, 290), 36, color)
                for row, line in enumerate(lines): ui.text(screen, line, (x, 332 + row * 36), 24)
            ui.text(screen, 'Point your nose with rotation, then boost to fly. Boost refills fastest on the ground.', (640, 524), 24)
            options = [('BACK', 'back')]
        else:
            if state == 'over':
                winner = 'DRAW GAME' if match.scores[0] == match.scores[1] else f'PLAYER {1 if match.scores[0] > match.scores[1] else 2} WINS'
                ui.text(screen, f'{winner}    /    {match.scores[0]} : {match.scores[1]}', (640, 285), 48)
            else:
                ui.text(screen, 'Two cars. One ball. Ninety seconds.', (640, 274), 36, (149, 174, 205))
            options = [('RESUME' if state == 'pause' else 'PLAY MATCH', 'resume' if state == 'pause' else 'play'), ('CONTROLS', 'controls'), ('MAIN MENU' if state in ('pause', 'over') else 'QUIT', 'menu' if state in ('pause', 'over') else 'quit')]
        for i, (label, action) in enumerate(options):
            rect = pygame.Rect(460, 570 if state == 'controls' else 345 + i * 68, 360, 54)
            hovered = rect.collidepoint(mouse)
            ui.panel(screen, rect, (27, 64, 87) if hovered else (16, 30, 51), CYAN if hovered else (55, 79, 105))
            ui.text(screen, label, rect.center, 28)
            buttons.append((rect, action))
        ui.text(screen, 'ENTER  PLAY / RESUME     •     C  CONTROLS     •     ESC  BACK / PAUSE', (640, 662), 20, (139, 160, 189))
        return buttons
