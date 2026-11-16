# Tamagotchi Simulator

A command-line virtual pet game written in Python, made for the EPITA *Introduction to Python Programming* course (2026-2027).

The player picks **3 pets** out of 15 and keeps them alive by feeding them, playing with them, putting them to sleep and healing them. Every action takes time, so neglected pets get hungry, bored and tired, lose health, and can die.

## How to run

You need **Python 3** (no extra library to install).

```bash
python main.py
```

All four `.py` files must be in the same folder. The save file `save.json` is created automatically the first time you save.

## How to play

1. At the start, choose to **load a saved game** or start a new one.
2. For a new game, choose **3 different pets** from the list, separated by spaces (for example `Rima Bubbles Plume`).
3. Each turn, every pet's status is shown. Then type:

| Command | What it does | Counts as a turn? |
| --- | --- | --- |
| a pet's name (e.g. `Rima`) | select that pet, then choose `feed`, `play`, `sleep` or `heal` | Yes |
| `stats` | number of living and dead pets, and average stats of living pets | No |
| `save` | save the game to `save.json` | No |
| `load` | load the game from `save.json` | No |
| `quit` | leave the game | No |

The game ends when you quit or when all your pets are dead.

## The pets

There are 15 pets in 3 categories. Each category has a weakness: one need that grows faster than the others.

| Category | Pets | Weakness |
| --- | --- | --- |
| **Land** | Rima (Bunny), Pistashe (Froggie), Noisette (Hedgehog), Biscuit (Puppy), Mochi (Hamster) | gets **bored** faster |
| **Sea** | Bubbles (Sealion), Coral (Turtle), Splash (Dolphin), Inky (Octopus), Nemo (Clownfish) | gets **hungry** faster |
| **Sky** | Plume (Owl), Kiwi (Parrot), Nuage (Bat), Pepper (Sparrow), Flamme (Phoenix) | gets **tired** faster |

## Game rules

Every pet has 4 stats, from 0 to 100: **health** (100 is best), and **hunger**, **boredom** and **exhaustion** (0 is best).

| Action | Effect |
| --- | --- |
| Feed | hunger −10, health +5 (only if hungry) |
| Play | boredom −10, hunger +10, exhaustion +10 (only if bored) |
| Sleep | exhaustion −10 (only if tired) |
| Heal | health +20 (only if not at full health) |

- **Time:** after each action, every living pet gets +4 hunger, boredom and exhaustion (+6 for its category's weakness).
- **Neglect:** for each need that reaches 100, the pet loses 10 health per turn.
- **Death:** a pet dies when its health reaches 0. It can no longer be cared for.
- **Random events:** after each turn, there is a 20% chance that a random living pet finds a snack, catches a cold, finds a toy or has a nightmare.

The full rules are in [`rules.txt`](rules.txt).

## Project structure

```
Tamagotchi-Simulator/
|-- main.py          # entry point: creates the game and starts it
|-- tamagotchi.py    # Tamagotchi class and its Land / Sea / Sky subclasses
|-- game.py          # Game class: pet choice, menu loop, time passing, statistics
|-- storage.py       # saving and loading the game in JSON
|-- rules.txt        # the game rules
```

## Python concepts used

- **Object-oriented programming:** a `Tamagotchi` class with three subclasses (**inheritance**). Each subclass overrides `get_status()` and changes class attributes to set its own weakness.
- **Data structures:** dictionaries for the pets, lists, tuples, and list and dictionary comprehensions.
- **Modules:** the code is split into 4 files, and uses the `random` and `json` standard libraries.
- **File handling:** the game is saved and loaded as JSON (**serialization** with `to_dict()`, **deserialization** in `load_game()`).
- **Exception handling:** invalid inputs never crash the game. A missing save file (`FileNotFoundError`), a broken one (`json.JSONDecodeError`) or invalid content (`ValueError`) each show a clear message.

## Error handling

| Situation | What happens |
| --- | --- |
| Invalid or duplicate pet names at the start | a message, then the question is asked again |
| Unknown pet or unknown command in the menu | a message, and the menu is shown again |
| Action on a dead pet | "*name* is dead." |
| Missing, broken or invalid save file | a clear message, and the game continues |
