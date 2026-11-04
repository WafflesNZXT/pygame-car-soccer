# Neon Kickoff

An original two-player 2D car soccer game for our programming club, inspired by the mechanics of Rocket League Sideswipe. Built with Python and Pygame. All stadium art, cars, ball graphics and effects are drawn in code; no Rocket League artwork, branding or audio is included.

## Install and play

Use **Python 3.10–3.13** (3.12 recommended). Pygame 2.6.1 may not provide wheels for newer Python releases. Run commands from the repository folder.

Windows (PowerShell):
```powershell
git clone https://github.com/WafflesNZXT/pygame-car-soccer.git
cd pygame-car-soccer
git switch feature/neon-car-soccer
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```
If PowerShell blocks activation, use `.venv\Scripts\python.exe` directly in the last two commands.

macOS / Linux:
```sh
git clone https://github.com/WafflesNZXT/pygame-car-soccer.git
cd pygame-car-soccer
git switch feature/neon-car-soccer
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```
On Linux, install your distribution's `python3-venv` package if creating the environment fails. After this feature is merged, use `main` instead of the feature branch. No accounts, asset downloads, or services are needed to play.

## Controls

| Action | Player 1 (cyan) | Player 2 (orange) |
| --- | --- | --- |
| Drive | A / D | Left / Right |
| Rotate in air | W / S | Up / Down |
| Jump | Space | Enter |
| Boost | Left Shift | Right Shift (or Right Ctrl) |

W / Up rotates counterclockwise on screen; S / Down rotates clockwise. Point the car's nose upward and boost to fly. Drive direction determines facing on the ground. Boost regenerates automatically, faster while grounded. Cars stay inside the main field; the ball can enter the goal pockets.

Enter starts/resumes a match; C opens controls from menus. Esc pauses/resumes or returns from controls. Menus also support mouse clicks. Losing window focus pauses play.

## Features

- 1280 × 720 window, 60 FPS target, fixed 120 Hz physics with delta-time animations.
- Gravity, momentum, drag, jumping, aerial rotation and limited boost.
- Rotated car-to-ball contacts, car-to-car separating-axis contacts, arena bounces and rounded goalposts.
- Whole-ball goal detection; 90 seconds of active play; kickoff countdowns, goal celebrations, rematches and winner/draw screens.
- Procedural neon stadium, distinct detailed cars, spinning wheels, animated flames and boost trails, rotating ball seams and trails, goal bursts, scoreboard and boost meters.
- Main menu, controls, pause and full-time screens. No sound in this first version.

## Code map and group workflow

| Module | Responsibility |
| --- | --- |
| `main.py` | Entry point and launch |
| `src/settings.py` | Tuning constants and colors |
| `src/physics.py` | Vectors and collision geometry |
| `src/car.py`, `src/ball.py` | Body movement and car-ball impulse |
| `src/arena.py` | Arena bounds, posts and goal detection |
| `src/match.py` | Match clock, scoring and state transitions |
| `src/game.py` | Pygame events, fixed-step loop and orchestration |
| `src/render.py` | Cached stadium art and animated body graphics |
| `src/particles.py` | Bounded time-based effects |
| `src/ui.py`, `src/menus.py` | HUD and interactive screens |
| `tests/` | Physics, match and headless rendering checks |

Create a branch for each change, keep commits focused and open a pull request into `main`. Agree on shared interfaces before editing another student's module. Suggested areas to split: physics/tuning, stadium/car art, menus/HUD, and testing. Tune values in `settings.py` and movement values in `car.py`; keep physics free of rendering dependencies.

## Tests

Core tests run without Pygame. The rendering test runs automatically when Pygame is installed:
```sh
python -m unittest discover -s tests -v
```
Headless graphics smoke test (macOS/Linux):
```sh
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy python main.py --smoke 180 --play --screenshot smoke-play.png
```
PowerShell equivalent:
```powershell
$env:SDL_VIDEODRIVER='dummy'
$env:SDL_AUDIODRIVER='dummy'
python main.py --smoke 180 --play --screenshot smoke-play.png
```
Unset those variables to return to a normal window. GitHub Actions installs Pygame, runs both test suites and uploads a rendered frame as `game-preview`.

Implementation-environment validation: core logic tests and Python compilation passed. Pygame was unavailable and package installation was blocked by network DNS restrictions, so local rendering and interactive gameplay were not executed there. Check the PR's Actions results for graphics verification.

### Manual playtest before approval

Play a complete match with two people. Check simultaneous keyboard inputs, both jumps and boosts, aerial steering, both goals, celebrations, clock freeze while paused, focus loss, rematch and quitting. Some keyboards cannot register every simultaneous key combination (hardware ghosting); try another keyboard if inputs drop. Assess visual layout, frame rate and physics feel on the actual club computers.

### Prototype limitations

Arcade contacts use linear impulses without angular impulse or suspension. Fixed 120 Hz steps and capped speed reduce tunneling; this is not a swept continuous collision solver. Ground contact automatically levels the car. There is no AI, online multiplayer, audio, key rebinding, controller input or overtime; tied games end in a draw. Resolution is fixed. A long frame is clamped to 50 ms to avoid an unstable catch-up loop, so severe stalls slow simulated match time.

## Progress and paint

Completed matches award 150 XP for a win, 50 for a loss and 75 each for a draw. Levels need 200 XP initially, increasing by 100 XP per level. Select Garage to cycle through each player's unlocked paint; later paints unlock at levels 3, 5 and 8. Profile XP, match statistics and paint save locally to `~/.neon_kickoff/profiles.json`. Leaving a match before the end awards no XP.

The garage offers four body styles, four wheel styles, four boost styles, four decals, and four underglow choices. Click each player's category to cycle through unlocked options; the next locked item's required level is shown. Cosmetics are visual and do not affect physics. Profiles created by earlier versions continue to work. If a save cannot be read, saving is disabled for that session to protect the original file.

The results screen animates XP and shows a level-up message. The stadium, cars and ball use original layered procedural graphics.

Remaining work: dedicated new-item unlock announcements, collision sparks and camera shake, richer boost-specific effects, keyboard garage navigation and interactive MacBook performance/playtesting.
