import pygame
from .settings import WIDTH, HEIGHT, WHITE, CYAN, ORANGE

class UI:
    def __init__(self):
        self.fonts = {size: pygame.font.Font(None, size) for size in (20, 24, 28, 36, 48, 72, 100)}

    def text(self, screen, text, pos, size=28, color=WHITE, center=True):
        image = self.fonts[size].render(str(text), True, color)
        rect = image.get_rect(center=pos) if center else image.get_rect(topleft=pos)
        screen.blit(image, rect)

    def panel(self, screen, rect, color=(14, 25, 47), border=(44, 66, 96)):
        pygame.draw.rect(screen, color, rect, border_radius=14)
        pygame.draw.rect(screen, border, rect, 1, border_radius=14)

    def hud(self, screen, match):
        self.panel(screen, (440, 22, 400, 78))
        self.text(screen, match.scores[0], (490, 61), 48, CYAN)
        self.text(screen, match.scores[1], (790, 61), 48, ORANGE)
        seconds = int(max(0, match.remaining) + .999)
        self.text(screen, f'{seconds // 60}:{seconds % 60:02}', (640, 56), 48)
        self.text(screen, 'MATCH TIME', (640, 84), 20, (119, 146, 180))
        for index, car in enumerate(match.cars):
            x = 90 if index == 0 else 970
            color = CYAN if index == 0 else ORANGE
            self.text(screen, f'P{index + 1}  /  BOOST {int(car.boost):02}', (x, 666), 24, color, False)
            pygame.draw.rect(screen, (24, 39, 61), (x, 695, 220, 7), border_radius=3)
            if car.boost > 0:
                pygame.draw.rect(screen, color, (x, 695, round(220 * car.boost / 100), 7), border_radius=3)
        self.text(screen, 'ESC  PAUSE', (1180, 45), 20, (119, 146, 180))
