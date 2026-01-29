# RogueGame

A Python roguelike dungeon crawler with procedural generation, turn-based combat, spell casting, and item management.

## Project Structure

```
RogueGame-main/
├── src/                          # NEW: Refactored source code
│   ├── core/                     # Constants, configuration, base classes
│   │   ├── constants.py          # Centralized game constants
│   │   ├── config.py             # Configuration management
│   │   └── base.py               # Base GameObject class
│   ├── world/                    # World generation and maps
│   │   ├── maps.py               # Map system (FIXED list initialization bug)
│   │   └── spawning/             # Unified spawning system
│   └── ...
│
├── assets/                       # Game assets (sprites, sounds, fonts)
├── Sprites/                      # Source sprite files (.piskel, .aseprite)
├── Notes/                        # Design documents and ideas
│
├── roguewriting.py               # Main entry point
├── loops.py                      # Game state machine
├── player.py                     # Player character
├── objects.py                    # Base entity class (legacy)
├── spawnparams.py                # Spawn configuration (LEGACY - use src/world/spawning)
│
├── character_implementation/     # Character stats, inventory, equipment
├── display_generation/           # Rendering and UI screens
├── dungeon_generation/           # Dungeon and map generation
├── interactable_implementation/  # NPCs, fountains, etc.
├── item_implementation/          # Items, weapons, armor
├── loop_workflow/                # Input handling and game loops
├── monster_implementation/       # Monster AI
├── monsters/                     # Monster definitions
├── navigation_utility/           # Pathfinding and FOV
├── spell_implementation/         # Spells and effects
└── unused/                       # Deprecated code (can be removed)
```

## Requirements

- Python 3.8+
- pygame
- pygame_gui

## Installation

```bash
pip install pygame pygame_gui
```

## Running the Game

```bash
python roguewriting.py
```

## Controls

| Key | Action |
|-----|--------|
| W/A/S/D or Arrow Keys | Move |
| Q/E/Z/C | Diagonal movement |
| . (Period) | Wait/Rest |
| G | Pick up item |
| I | Inventory |
| U | Equipment |
| M | Spells |
| X | Examine |
| > / < | Use stairs |
| O | Auto-explore |
| Escape | Pause menu |

## Architecture Overview

### Game Loop (loops.py)
The game uses a state machine pattern where `LoopType` enum defines all possible game states (action, inventory, targeting, etc.). The `Loops` class manages transitions between states and coordinates rendering/input.

### Entity System
- `Objects` (objects.py) - Base class for all game entities
- `Character` - Health, mana, stats, equipment
- `Monster` - NPCs with AI brains
- `Item` - Equipment, consumables, etc.

### Dungeon Generation
- Procedural room-based generation
- Multiple dungeon branches supported
- Item and monster spawning with rarity distributions

### Combat System
- Turn-based with energy costs
- Weapons, armor, and stat modifiers
- Status effects (burn, poison, slow, etc.)
- Spell casting system

## Development Notes

See [REFACTORING_NOTES.md](REFACTORING_NOTES.md) for detailed technical documentation about:
- Critical bugs that were fixed
- Code redundancies that were consolidated
- Recommended future improvements
- Asset organization changes

## License

This project is for educational purposes.
