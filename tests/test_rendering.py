"""Run with SDL dummy driver: exercise every screen and draw path when installed."""
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
import importlib.util
import unittest

@unittest.skipUnless(importlib.util.find_spec('pygame'), 'Pygame is not installed')
class RenderingTests(unittest.TestCase):
    def test_all_screens_and_game_events(self):
        import pygame
        from src.game import Game
        game = Game()
        try:
            for state in ('menu', 'controls', 'pause', 'over', 'garage', 'stats'):
                game.state = state
                game.draw(1/60)
                self.assertTrue(game.buttons)
            game.profiles.players[0]['total_xp'] = 200
            game.rewards = [150, 50]
            game.state = 'over'
            game.time = 5
            game.draw(1/60)
            game.action('play')
            game.match.phase = 'play'
            for car in game.match.cars:
                car.boosting = True
                car.angle = .7 if car.player == 0 else 2.6
            game.draw(1/60)
            game.match.ball.pos.x = 1250
            game.match.ball.pos.y = 510
            game.update(1/60)
            self.assertEqual(game.match.scores, [1, 0])
            game.draw(1/60)
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))
            game.events()
            self.assertEqual(game.state, 'pause')
            time = game.match.remaining
            game.update(.05)
            self.assertEqual(game.match.remaining, time)
        finally:
            pygame.quit()

    def test_boost_bindings(self):
        import pygame
        from src.game import read_controls
        class Keys:
            def __init__(self, active): self.active = active
            def __getitem__(self, key): return key in self.active
        for key in (pygame.K_RSHIFT, pygame.K_RCTRL):
            controls = read_controls(Keys({pygame.K_LSHIFT, key}), [False, False])
            self.assertTrue(controls[0].boost)
            self.assertTrue(controls[1].boost)
        self.assertFalse(read_controls(Keys(set()), [False, False])[1].boost)
