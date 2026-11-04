"""Local profiles and match rewards. Total XP is the source of truth."""
import json
import os
from pathlib import Path

COLORS = [('Cyan', (55,219,255), 1), ('Orange', (255,157,66), 1), ('Red', (240,75,80), 1), ('Blue', (70,120,250), 1), ('Green', (65,220,150), 1), ('Purple', (177,98,245), 3), ('White', (235,245,250), 5), ('Black', (45,50,65), 8)]

def level_info(total):
    level = 1
    while total >= 200 + 100 * (level - 1):
        total -= 200 + 100 * (level - 1)
        level += 1
    return level, total, 200 + 100 * (level - 1)

def default_profile(index):
    return {'total_xp': 0, 'wins': 0, 'losses': 0, 'draws': 0, 'color': index}

class Profiles:
    def __init__(self, path=None):
        self.path = Path(path) if path else Path.home() / '.neon_kickoff' / 'profiles.json'
        self.players = [default_profile(0), default_profile(1)]
        self.error = None
        try:
            data = json.loads(self.path.read_text())
            for i in range(2):
                source = data['players'][i]
                for key in ('total_xp', 'wins', 'losses', 'draws'):
                    value = source.get(key, 0)
                    if type(value) is int and 0 <= value <= 10000000: self.players[i][key] = value
                color = source.get('color', i)
                if type(color) is int and 0 <= color < len(COLORS): self.players[i]['color'] = color
        except FileNotFoundError: pass
        except (OSError, ValueError, TypeError, KeyError, IndexError):
            self.error = 'Could not read profiles; using defaults.'

    def save(self):
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            temp = self.path.with_suffix('.tmp')
            temp.write_text(json.dumps({'players': self.players}, indent=2))
            os.replace(temp, self.path)
            self.error = None
            return True
        except OSError:
            self.error = 'Could not save profiles.'
            return False

    def reward(self, scores):
        rewards = []
        for i, p in enumerate(self.players):
            result = 'draws' if scores[0] == scores[1] else 'wins' if scores[i] > scores[1-i] else 'losses'
            xp = {'wins': 150, 'losses': 50, 'draws': 75}[result]
            p[result] += 1
            p['total_xp'] += xp
            rewards.append(xp)
        self.save()
        return rewards
