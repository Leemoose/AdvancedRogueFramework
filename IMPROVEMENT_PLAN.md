# RogueGame Improvement Plan

**Goal:** Tighten code, improve structure, fix UI cross-platform issues, and create distributable builds for PC/Mac.

**Context:** Python roguelike using pygame + pygame_gui. ~209 Python files.

**Last Updated:** January 29, 2026 (Phase 6 Quick Wins + Medium Priority Complete)

**See also:** `COMPLETED_WORK.md` for finished items.

---

## Version Control Policy

**All notable changes must be backed up to GitHub.** Before starting new features or refactoring:

1. Commit current work with descriptive message
2. Push to remote repository
3. Create feature branches for large changes
4. Use `git status` to verify clean working tree

```bash
# Standard workflow
git add -A
git commit -m "Brief description of changes"
git push origin main

# For larger changes
git checkout -b feature/your-feature-name
# ... make changes ...
git push -u origin feature/your-feature-name
```

---

## Status Summary

| Phase | Status | Remaining |
|-------|--------|-----------|
| Phase 1: Foundation | ✅ Complete | - |
| Phase 2: Performance | ✅ 95% | Minor optimizations |
| Phase 3: Code Quality | ✅ 90% | Minor style fixes |
| Phase 4: Architecture | ✅ 90% | Data-driven design |
| Phase 5: Features | 🔲 Not Started | Settings menu, bugs |
| **Phase 6: Code Simplification** | ✅ 80% | Tasks 1-8 complete, Tasks 9-12 remaining |

---

## Phase 6: Code Simplification for Developer Experience

**Goal:** Make the codebase easy for new developers to understand and extend. Remove hardcoding, reduce duplication, improve extensibility.

### Quick Wins (1-2 hours each)

#### 1. Extract Direction Vectors
**Problem:** Direction vectors `[(0, 1), (0, -1), (1, 0), (-1, 0), ...]` are hardcoded in 5+ files with inconsistent ordering.

**Files affected:**
- `player.py` (line 385)
- `dungeon_generation/mapping_utility.py`
- `dungeon_generation/mapping.py` (2 occurrences)
- `navigation_utility/pathfinding.py`
- `loop_workflow/keyboard.py`

**Solution:** Create `src/core/directions.py`:
```python
class Directions:
    CARDINAL_4 = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    DIAGONAL_4 = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
    ALL_8 = CARDINAL_4 + DIAGONAL_4
```

- [x] Create `src/core/directions.py`
- [x] Replace all hardcoded direction vectors with `Directions.ALL_8`
- [x] Update imports in affected files

---

#### 2. Add Game Time Constants
**Problem:** Magic number `100` (energy per turn) is hardcoded in `loops.py` (lines 385, 416).

**Solution:** Add to `src/core/constants.py`:
```python
class GameTime:
    ENERGY_PER_TURN = 100  # Energy units that constitute one game turn
```

- [x] Add `GameTime` class to `constants.py`
- [x] Replace `100` in `loops.py` with `GameTime.ENERGY_PER_TURN`

---

#### 3. Add Tile Size Constant
**Problem:** `(32, 32)` hardcoded 13+ times in `static_configs.py`.

**Solution:** Add to `src/core/constants.py`:
```python
TILE_SIZE = 32
```

- [x] Add `TILE_SIZE` constant
- [x] Update `static_configs.py` to use it

---

#### 4. Consolidate Spawn Parameter Classes
**Problem:** Three nearly identical classes in `dungeon_generation/spawning/spawn_params.py` with duplicated `AllowedAtDepth()` logic.

**Solution:** Create base class:
```python
class BaseSpawnParams:
    def __init__(self, entity, minFloor=1, maxFloor=10, branch="all"):
        self.entity = entity
        self.minFloor = minFloor
        self.maxFloor = maxFloor
        self.branch = branch

    def allowed_at_depth(self, depth, branch="all"):
        return (depth >= self.minFloor and depth <= self.maxFloor
                and (self.branch == "all" or self.branch == branch))
```

- [x] Create `BaseSpawnParams` class
- [x] Have `SpawnParams`, `ItemSpawnParams`, `MonsterSpawnParams` inherit from it
- [x] Remove duplicated `AllowedAtDepth()` methods (with backward compatibility)

---

### Medium Priority (3-5 hours each)

#### 5. Create Centralized Asset Registry
**Problem:** Tile IDs (render_tags) are hardcoded in item/monster constructors with no central documentation. Adding new content requires knowing arbitrary ID numbers.

**Files affected:**
- `static_configs.py` (298 lines of hardcoded tile loading)
- Every item class in `item_implementation/`
- Every monster class in `monsters/`

**Solution:** Create `src/core/asset_registry.py`:
```python
TILE_ASSETS = {
    # Tiles
    'colorful_wall': {'id': 1, 'path': 'assets/tiles/colorful_wall.png', 'scaled': True},
    'colorful_floor': {'id': 2, 'path': 'assets/tiles/colorful_floor.png', 'scaled': True},
    # Items
    'leather_armor': {'id': 3000, 'path': 'assets/items/armor/leather.png'},
    'dagger': {'id': 321, 'path': 'assets/items/weapons/dagger.png'},
    # ...
}

def get_render_tag(name):
    return TILE_ASSETS[name]['id']
```

- [x] Create `asset_registry.py` with all tile mappings
- [ ] Update item classes to use registry lookups instead of hardcoded IDs (future)
- [ ] Update `static_configs.py` to load from registry (future)
- [x] Document tile ID ranges in registry

---

#### 6. Create Player Configuration
**Problem:** Player initial state is hardcoded in `player.py`: starting health (10), mana (5), max level (20), debug settings.

**Solution:** Create `src/core/player_config.py`:
```python
class PlayerConfig:
    STARTING_HEALTH = 10
    STARTING_MANA = 5
    STARTING_X = 0
    STARTING_Y = 0
    MAX_LEVEL = 20
    DEBUG_MODE = False
    DEBUG_STARTING_STATS = 20
```

- [x] Create `player_config.py`
- [x] Update `player.py` to use config values
- [x] Move debug spell initialization behind config flag

---

#### 7. Extract Movement Validator
**Problem:** Movement validation is duplicated between `attack_move()` and `move()` in `player.py` (lines 89-122).

**Solution:** Create `MovementValidator` class:
```python
class MovementValidator:
    @staticmethod
    def can_move_to(loop, from_pos, to_pos, character):
        if not loop.generator.in_map(*to_pos):
            return False, "Out of bounds"
        if not character.can_take_action():
            return False, "Cannot act"
        if not character.can_move():
            return False, "Cannot move"
        if not loop.generator.get_passable(to_pos):
            return False, "Blocked"
        return True, "OK"
```

- [x] Create `MovementValidator` in `src/core/movement.py`
- [x] Refactor `player.py` to use validator
- [x] Eliminate duplicate condition checks

---

#### 8. Add Energy Helper Method
**Problem:** Same energy deduction pattern repeated 4 times in `player.py` (lines 91, 112, 126, 343).

**Solution:** Add method to Player class:
```python
def spend_energy(self, action_type):
    if action_type in self.character.action_costs:
        self.character.energy -= self.character.action_costs[action_type]
        return True
    return False
```

- [x] Add `spend_energy()` method to Player
- [x] Replace all `self.character.energy -= self.character.action_costs[...]` calls

---

### Lower Priority (Future Refactoring)

#### 9. Split Loops Class State Management
**Problem:** `Loops` class in `loops.py` has 30+ attributes mixing game state, UI state, and NPC state.

**Solution:** Create state manager classes:
```python
class GameState:
    class PlayerState:
        quest_received = False
        quest_completed = False

    class UIState:
        current_stat = 0
        current_spell = None

    class NPCState:
        next_dialogue = False
        dialogue_options = 0
```

- [ ] Create `src/core/game_state.py`
- [ ] Move state attributes from Loops to GameState
- [ ] Update references throughout codebase

---

#### 10. Create Spell Type Hierarchy
**Problem:** All spells inherit from single `Spell` base class with no categorization.

**Solution:** Add spell type hierarchy:
```python
class SpellType(Enum):
    DAMAGE = "damage"
    UTILITY = "utility"
    BUFF = "buff"
    DEBUFF = "debuff"
    HEAL = "heal"

class DamageSpell(Spell):
    spell_type = SpellType.DAMAGE

class BuffSpell(Spell):
    spell_type = SpellType.BUFF
```

- [ ] Create spell type enum
- [ ] Create intermediate base classes
- [ ] Categorize existing spells

---

#### 11. Create Monster/Item Definition Format
**Problem:** Adding new monsters/items requires changes in 4-5 files.

**Solution:** Create unified definition format:
```python
MONSTER_DEFINITIONS = {
    'goblin': {
        'class': Goblin,
        'render_tag': 1010,
        'asset': 'assets/crawl-tiles/dc-mon/goblin.png',
        'spawn': {'min_floor': 2, 'max_floor': 6, 'branch': 'Dungeon'},
        'ai': 'base_behaviors',
    },
}
```

- [ ] Create `monsters/definitions.py`
- [ ] Create `item_implementation/definitions.py`
- [ ] Auto-generate spawn lists from definitions

---

#### 12. Move to Data-Driven Design (JSON/YAML)
**Problem:** Game balance values hardcoded throughout Python files.

**Solution:** Extract to configuration files:
- `data/monsters.yaml` - Monster stats, spawn rates
- `data/items.yaml` - Item stats, spawn rates
- `data/dungeon.yaml` - Level progression, branch configs

- [ ] Create `data/` directory
- [ ] Extract monster definitions to YAML
- [ ] Extract item definitions to YAML
- [ ] Create loader classes

---

## Remaining Work (Previous Items)

### Code Quality (Low Priority)

**Constants Migration**
- Replace remaining `== -1` with `NO_ENTITY` where applicable
- Replace magic tile IDs with `TileIDRange.*`
- Replace hardcoded colors with `Colors.*`

**Style Fixes**
- ~~Fix remaining `== None` → `is None` (1 occurrence in `summon_school.py`)~~ ✅ Fixed
- Replace remaining `print()` with `logging`
- Remove commented code blocks
- Add type hints to core files

**Dead Code**
- ~~Remove unused import in `monsters/monster.py` (references deleted `unused/` folder)~~ ✅ Already clean

---

### Features (Phase 5)

**From Notes/todo.txt:**
- [ ] Range weapons system
- [ ] Fix mini examine window
- [ ] Spell hotkey hover display
- [ ] Skill vs Spell distinction (cooldown vs mana)
- [ ] Monster AI escape behavior fix
- [ ] Split item screen description/buttons

**New Features:**
- [ ] Settings menu (volume, keybindings, display)
- [ ] Windowed/fullscreen toggle
- [ ] Resolution selection
- [ ] Accessibility options

---

### Known Bugs (from bugs.txt)

| Bug | Severity |
|-----|----------|
| IndexError on fire terrain | 🔴 Crash |
| Duplicate skill from item + book | 🟡 Gameplay |
| Dojo art covering stairs | 🟡 Visual |
| Gateway direction issues | 🟡 Gameplay |
| Loading into wrong room | 🟡 Gameplay |
| Dialogue font apostrophes | 🟢 Minor |
| Enchant scroll inventory filter | 🟢 Minor |
| Summon hornet damage effect | 🟢 Minor |
| Blink scroll range validation | 🟡 Gameplay |

---

## Build Commands

```bash
# Install dependencies
pip install -r requirements.txt pyinstaller

# Run game
python roguewriting.py

# Build executable
pyinstaller RogueGame.spec

# Mac: Create distributable zip
cd dist && zip -r RogueGame-Mac.zip RogueGame.app
```

---

## Key Files

| Purpose | File |
|---------|------|
| Entry point | `roguewriting.py` |
| Asset loading | `static_configs.py` |
| Main display | `display_generation/display.py` |
| UI components | `display_generation/ui.py` |
| UI theme | `assets/theme.json` |
| Screen helpers | `display_generation/ui_utils.py` |
| Event system | `src/core/events.py` |
| Constants | `src/core/constants.py` |
| Developer guide | `DEVELOPER_GUIDE.md` |
