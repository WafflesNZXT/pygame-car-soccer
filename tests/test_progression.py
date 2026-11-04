import json
import tempfile
import unittest
from pathlib import Path
from src.progression import Profiles, level_info

class ProgressionTests(unittest.TestCase):
    def test_levels_can_advance_more_than_once(self):
        self.assertEqual(level_info(900), (4, 0, 500))

    def test_rewards_and_persistence(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'profiles.json'
            profiles = Profiles(path)
            self.assertEqual(profiles.reward([2, 1]), [150, 50])
            self.assertEqual(profiles.reward([0, 0]), [75, 75])
            profiles.players[0]['color'] = 2
            profiles.save()
            again = Profiles(path)
            self.assertEqual(again.players[0]['total_xp'], 225)
            self.assertEqual(again.players[1]['total_xp'], 125)
            self.assertEqual(again.players[0]['wins'], 1)
            self.assertEqual(again.players[1]['losses'], 1)
            self.assertEqual(again.players[0]['color'], 2)
            self.assertEqual(again.players[1]['color'], 1)

    def test_corrupt_save(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'profiles.json'
            path.write_text('{bad')
            p = Profiles(path)
            self.assertEqual(p.players[0]['total_xp'], 0)
            self.assertIsNotNone(p.error)

if __name__ == '__main__': unittest.main()
