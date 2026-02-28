# RogueGame Codebase Navigation Skill

## Project Overview

RogueGame is a tile-based roguelike dungeon crawler built with Python, pygame, and pygame_gui. The codebase lives at the project root and uses no virtual environment or package manager -- it runs directly with Python imports from the project root directory.

**Root path**: `/sessions/sharp-brave-thompson/mnt/ClaudeWork/RogueGame-main/`

**Tech stack**: Python 3, pygame, pygame_gui, dill (serialization)

**Save format**: `data.dill` (binary dill pickle of entire game state)

---

## 1. Class Hierarchy and Inheritance

### Base Entity: `Objects` (objects.py)

All game entities inherit from `Objects`. This is the universal base class.

```
Objects (objects.py, line 2)
  |-- Player (player.py, line 17)
  |-- Monster (monsters/monster.py, line 14)
  |-- Item (item_implementation/items.py, line 7)
  |     |-- Gold (item_implementation/items.py, line 41)
  |     |-- Consumeable (item_implementation/items.py, line 63)
  |     |     |-- YellowFlowerPetal (item_implementation/items.py, line 95)
  |     |     |-- (various potions in item_implementation/consumables/)
  |     |-- Equipment (item_implementation/equipment.py, line 6)
  |           |-- (various weapons/armor in item_implementation/weapons/ and armor/)
  |-- Tile classes (dungeon_generation/tiles/)
       |-- Floor, Wall, Stairs, Gateway, Door, etc.
```

**Key `Objects` attributes and methods** (objects.py):
- `__init__(self, x=-1, y=-1, id_tag=-1, render_tag=-1, name="Unknown object")` -- line 3
- `self.traits = {"object": True}` -- dictionary-based trait system, line 8
- `has_trait(self, trait)` -- line 15, returns `self.traits[trait]` or `False`
- `get_location(self)` -- line 24, returns `(self.x, self.y)` tuple
- `get_distance(self, x, y)` -- line 27, Euclidean distance
- `set_location(self, x, y)` -- line 54
- `get_render_tag(self)` -- line 30, integer ID for sprite lookup in TileDict
- `gain_ID(self, ID)` -- line 21, sets `id_tag` from TrackingMap

### Composition Pattern for Characters

Both `Player` and `Monster` use composition, NOT deep inheritance. They both contain:

| Component | Class | File | Purpose |
|-----------|-------|------|---------|
| `character` | `Character` | `character_implementation/character.py:12` | Health, mana, energy, action costs, status |
| `fighter` | `Fighter` | `character_implementation/fighter.py:3` | Combat damage, attack/defend |
| `inventory` | `Inventory` | `character_implementation/inventory.py` | Item storage |
| `body` | `Body` | `character_implementation/body_slot.py` | Equipment slots |
| `mage` | `Mage` | `character_implementation/mage.py` | Spell list, casting |

**Player** (player.py, line 17-18):
```python
class Player(Objects):
    def __init__(self, x, y):
        super().__init__(x, y, 1, 1000, "Player")  # render_tag=1000
        self.character = C.Character(self, mana=PlayerConfig.STARTING_MANA, health=PlayerConfig.STARTING_HEALTH)
        self.mage = Mage(self)
        self.inventory = Inventory(self)
        self.body = Body(self)
        self.fighter = Fighter(self)
        self.statistics = statistics.StatTracker()
        self.traits["player"] = True
```

**Monster** (monsters/monster.py, line 14-17):
```python
class Monster(O.Objects):
    def __init__(self, x=-1, y=-1, render_tag=-1, name="Unknown monster",
                 experience_given=0, rarity="Common", health=10,
                 min_damage=2, max_damage=3, mana=0, gold=0):
        self.character = C.Character(self, health=health, mana=mana, experience_given=experience_given)
        self.brain = MonsterAI(self, create_base_behaviors())
        self.inventory = Inventory(self, gold=gold)
        self.body = Body(self, min_damage=min_damage, max_damage=max_damage)
        self.fighter = Fighter(self)
        self.mage = Mage(self)
        self.traits["monster"] = True
```

### Map Hierarchy

```
Maps (dungeon_generation/maps/maps.py)
  |-- TileMap (dungeon_generation/maps/tilemap.py, line 74)
  |-- TrackingMap (dungeon_generation/maps/trackingmap.py, line 16)
```

### Spell Hierarchy

The codebase has TWO spell systems in transition:

1. **Old system**: `old/spell.py` -> `Spell` class, `old/spell_data.py` -> `SpellData`/`EffectData`, `old/spell_builder.py` -> `spell()` builder function
2. **New class-based system**: `spell_system/base_spell.py` -> `BaseSpell` (line 28)

```
BaseSpell (spell_system/base_spell.py, line 28)
  |-- Specific spell classes in spell_system/spells/
```

### GameState Hierarchy (State Pattern)

```
GameState (loop_workflow/game_states.py, line 30) -- ABC
  |-- ActionState (loop_workflow/states/gameplay_states.py)
  |-- TargetingState (loop_workflow/states/gameplay_states.py)
  |-- ExamineState (loop_workflow/states/gameplay_states.py)
  |-- SpecificExamineState (loop_workflow/states/gameplay_states.py)
  |-- MainMenuState (loop_workflow/states/menu_states.py)
  |-- PausedState (loop_workflow/states/menu_states.py)
  |-- HelpState (loop_workflow/states/menu_states.py)
  |-- StoryState (loop_workflow/states/menu_states.py)
  |-- InventoryState (loop_workflow/states/inventory_states.py)
  |-- EquipmentState (loop_workflow/states/inventory_states.py)
  |-- ItemScreenState (loop_workflow/states/inventory_states.py)
  |-- EnchantState (loop_workflow/states/inventory_states.py)
  |-- SpellListState (loop_workflow/states/spell_states.py)
  |-- SpellIndividualState (loop_workflow/states/spell_states.py)
  |-- QuickcastState (loop_workflow/states/spell_states.py)
  |-- DeathState (loop_workflow/states/modal_states.py)
  |-- VictoryState (loop_workflow/states/modal_states.py)
  |-- QuestState (loop_workflow/states/modal_states.py)
  |-- TradeState (loop_workflow/states/modal_states.py)
  |-- LevelUpState (loop_workflow/states/modal_states.py)
  |-- RestingState (loop_workflow/states/automated_states.py)
  |-- PathingState (loop_workflow/states/automated_states.py)
  |-- BindingState (loop_workflow/states/binding_state.py)
  |-- ClassState (loop_workflow/states/class_state.py)
```

---

## 2. Game Loop / State Machine

### Central Controller: `Loops` (loops.py, line 39)

The `Loops` class is the central coordinator. It is instantiated once and passed around as `loop` everywhere.

**Constructor** (line 59):
```python
def __init__(self, tileDict, display, keyboard, dungeon_data):
```

**Key attributes on `loop` (the Loops instance)**:
- `loop.display` -- Display instance
- `loop.player` -- Player instance
- `loop.generator` -- current floor's DungeonGenerator
- `loop.memory` -- Memory instance for save/load and floor storage
- `loop.state_manager` -- StateManager instance
- `loop.messages` -- MessageHandler
- `loop.targets` -- Target helper for targeting mode
- `loop.tileDict` -- TileDict sprite dictionary
- `loop.dungeon_data` -- DungeonData configuration
- `loop.keyboard` -- keyboard handler
- `loop.timer` / `loop.total_time` -- time tracking
- `loop.daytime` -- True=day, False=night (toggles every 50 turns)
- `loop.tide_level` -- ocean tide level (-50 to -5)
- `loop.quest_recieved` / `loop.quest_completed` -- quest state flags

### Main Loop Flow

`action_loop(keyboard, display)` (line 138) is called each frame:

1. `_process_events(keyboard, display)` -- handles pygame events (quit, keydown, mouse click, resize, UI button)
2. `_process_keyboard_queue(keyboard)` -- dispatches queued input to `state_manager.handle_input(key)`
3. `_run_state_tick()` -- calls `state_manager.tick()` for automated states
4. `_process_game_time()` -- if `player.character.energy < 0`, calls `time_passes()` and `monster_loop()`
5. `_check_player_death()` -- transitions to death state if player HP <= 0

### State Transitions

State changes go through: `loop.change_loop(LoopType.xyz)` (line 119)
  -> `state_manager.change_state(new_loop_type)` (game_states.py, line 146)
  -> calls `old_state.on_exit()`, then `new_state.on_enter()`
  -> then `state_manager.create_display(display)` refreshes the UI

**LoopType enum** (src/core/enums.py, line 9): `none, action, spell, inventory, equipment, main, classes, items, examine, trade, paused, targeting, specific_examine, enchant, quest, level_up, victory, help, death, story, resting, pathing, binding, spell_individual, quickcast`

### GameState Abstract Methods (game_states.py, line 30)

Every state must implement:
- `create_display(self, display)` -- set up UI when entering state
- `update_display(self, display)` -- render each frame
- `handle_input(self, key)` -- process keyboard input, return False to quit

Optional overrides: `on_enter()`, `on_exit()`, `tick()`

### StateManager (game_states.py, line 109)

- `register_state(state)` / `register_states(states)` -- adds to `self._states` dict keyed by `LoopType`
- `change_state(new_loop_type)` -- handles enter/exit callbacks
- Delegates: `create_display()`, `update_display()`, `handle_input()`, `tick()`

### All States Factory

`create_all_states(loop)` in `loop_workflow/states/__init__.py` (line 40) returns list of all 23 state instances.

---

## 3. Energy / Turn System

The game uses an energy-based turn system. Actions cost energy. When energy goes negative, game time advances.

### Constants (src/core/constants.py)

- `GameTime.ENERGY_PER_TURN = 100` (line 178)
- `ActionCost.MOVE = 100`, `ATTACK = 100`, `GRAB = 50`, `REST = 100`, `CAST_SPELL = 100`, `USE_ITEM = 50`, `EQUIP = 50`, `FAST_MOVE = 80`, `SLOW_MOVE = 300` (lines 192-207)

### Per-Entity Action Costs

Each entity's `Character` has its own `action_costs` dict (character.py, line 22):
```python
self.action_costs = {
    "attack": 100, "move": 100, "grab": 30, "equip": 100,
    "unequip": 50, "quaff": 10, "read": 20, "drop": 10, "activate": 25
}
```

### Energy Flow

1. **Player acts**: `player.spend_energy("move")` (player.py, line 77) subtracts `character.action_costs["move"]` from `character.energy`
2. **Energy check** (loops.py, `_process_game_time()`, line 277):
   ```python
   if self.player.character.energy < 0:
       energy_spent = -self.player.character.energy
       self.time_passes(energy_spent)
       self.monster_loop(energy_spent)
       self.player.character.energy = 0
   ```
3. **Monster loop** (loops.py, `monster_loop()`, line 321): Each awake monster gets `energy += energy_spent`, then acts while `energy > 0`:
   ```python
   monster.character.energy += energy
   while monster.character.energy > 0:
       monster.brain.rank_actions(self)
   ```
4. **Time passes** (loops.py, `time_passes()`, line 382): For each full turn of energy, ticks status effects, cooldowns, regen, quests, terrain effects, day/night cycle (every 50 turns), and ocean tides.

### Monster AI Energy

In `MonsterAI.rank_actions()` (behaviors.py, line 59), the monster always loses 1 energy per evaluation: `self.parent.character.energy -= 1`. Each behavior's `execute()` then subtracts the actual action cost.

---

## 4. Module Import Patterns and References

### Cross-Module Reference Pattern

The entire game state is accessible through the `loop` object (Loops instance). States, monsters, and utility functions all receive `loop` as a parameter.

**Accessing game data through `loop`:**
- Tile map: `loop.generator.tile_map`
- Monster map: `loop.generator.monster_map`
- Item map: `loop.generator.item_map`
- Interact map: `loop.generator.interact_map`
- Player: `loop.player`
- Messages: `loop.add_message("text", color_tuple)`
- State changes: `loop.change_loop(LoopType.action)`

### Import Conventions

- `LoopType` lives in `src/core/enums.py` (moved from `loop_workflow` to break circular imports)
- `from src.core.constants import GameTime, ActionCost, Colors, NO_ENTITY, TILE_SIZE`
- `from logging_config import get_logger` -- every file uses this
- Display imports: `from display_generation import *` in loops.py
- Character components: `from character_implementation import character as C, Inventory, Body, Fighter, Mage`
- Dungeon generation uses lazy/conditional imports to avoid circulars:
  ```python
  if TYPE_CHECKING:
      from ..generators.base import MapGenerator
  ```

### Circular Import Avoidance

- `LoopType` was moved from `loop_workflow/` to `src/core/enums.py`
- `display_generation/display.py` imports `LoopType` from `src.core.enums`
- Dungeon generators use `TYPE_CHECKING` guards
- `character.py` imports `LoopType` from `src.core.enums` for rest state transition

---

## 5. Key Function Signatures Commonly Modified

### Player Actions (player.py)

```python
def attack_move(self, move_x, move_y, loop)         # line 96 - main movement/combat entry point
def move(self, move_x, move_y, loop)                 # line 122 - raw movement
def attack(self, defender, loop)                      # line 135 - melee attack
def spend_energy(self, action_type: str) -> bool      # line 77 - energy deduction
def autopath(self, loop)                              # line 146 - auto-movement along path
def autoexplore(self, loop)                            # line 187 - BFS-based auto-explore
def find_stairs(self, loop)                            # line 234 - pathfind to stairs/gateways
def smart_attack(self, loop)                           # line 315 - auto-target nearest visible monster
def do_grab(self, item, loop)                          # line 392 - pick up item
def do_equip(self, item)                               # line 406 - equip item
def cast_spell(self, *args)                            # line 385 - delegates to mage.cast_spell
def gain_experience(self, experience)                  # line 92 - XP gain + level check
def check_for_levelup(self)                            # line 295 - level up loop
def down_stairs(self, loop)                            # line 348 - use stairs/gateway going down
```

### Combat (fighter.py)

```python
def do_attack(self, defender, loop)                    # line 46 - full attack resolution
def get_damage(self)                                   # line 69 - weapon damage + base
def do_defend(self)                                    # line 22 - returns armor value
def get_physical_hit_chance(self)                      # line 61 - accuracy roll
def get_dodge_chance(self)                             # line 65 - evasion roll
```

**Attack formula** (fighter.py, `do_attack`, line 46):
1. `dodge_percentage = defender.get_dodge_chance() - self.get_physical_hit_chance()`
2. `damage_shave = 1 - (max(min(dodge_percentage, 100), 0) / 100)`
3. Apply on-hit effects
4. `damage = self.get_damage() * physical_damage_multiplier`
5. `defense = defender.do_defend() - self.get_armor_piercing()`
6. `finalDamage = max(0, int(damage * damage_shave) - defense)`
7. Apply on-damage effects
8. `defender.character.take_damage(self.parent, finalDamage)`

### Character (character.py)

```python
def take_damage(self, dealer, damage)                  # line 65 - damage application, death handling
def tick_all_status_effects(self, loop)                # line 102 - process status effects per turn
def tick_regen(self)                                   # line 152 - health/mana regen
def needs_rest(self)                                   # line 156 - check if rest needed
def rest(self, loop, returnLoop)                       # line 164 - rest mechanic
def is_alive(self)                                     # line 59 - health check
def can_take_action(self)                              # line 309 - status allows actions
def can_move(self)                                     # line 312 - status allows movement
def add_skill(self, new_skill)                         # line 205 - add spell to mage
def get_attribute(self, attribute)                     # line 241 - universal attribute getter
def change_attribute(self, attribute, change)          # line 265 - universal attribute setter
def skill_damage_increase(self)                        # line 82 - intelligence-based damage bonus
```

### Loops Controller (loops.py)

```python
def change_loop(self, new_loop)                        # line 119 - state transition
def action_loop(self, keyboard, display) -> bool       # line 138 - main frame loop
def monster_loop(self, energy)                         # line 321 - monster AI processing
def time_passes(self, time)                            # line 382 - game time advancement
def change_floor(self, level_change=-1, random_location=False)  # line 489 - floor transition
def change_branch(self)                                # line 547 - branch transition via gateway
def init_game(self)                                    # line 607 - new game initialization
def load_game(self)                                    # line 751 - load saved game
def clean_up(self)                                     # line 343 - remove dead/destroyed entities
def add_message(self, message, color=(255,255,255))    # line 825 - add to message log
def start_targetting(self, start_on_player=False)      # line 778 - enter targeting mode
```

### DungeonGenerator (dungeon_generation/mapping.py)

```python
def get_passable(self, location: tuple) -> bool        # line 270 - checks monster_map + player + tile_map + interact_map
def get_random_passable_location(self, stairs_block=True)  # line 214 - random open position
def get_monsters_in_sight(self)                        # line 246 - visible monsters list
def place_monster_at_location(self, creature, x, y)    # line 300 - place monster
def place_item_at_location(self, item, x, y)           # line 307 - place item
def get_is_in_corridor(self, x, y)                     # line 327 - corridor detection heuristic
```

---

## 6. Display / Rendering Pipeline

### Display class (display_generation/display.py, line 12)

**Constructor**: `__init__(self, width, height, textSize, textWidth, textHeight)`
- Creates pygame window with `pygame.RESIZABLE`
- Creates `pygame_gui.UIManager` with `./assets/theme.json`
- Calculates tile viewport center: `self.r_x`, `self.r_y` from `UILayout.get_tile_viewport()`

**Key methods:**
- `update_main(loop)` -- renders main menu (title screen)
- `draw_player(loop)` -- renders player sprite + equipment overlays (boots, gloves, helmet, armor)
- `screen_to_tile(player, x, y)` -- converts pixel coords to tile coords (line 52)
- `update_sizes()` / `handle_resize()` -- window resize handling
- `get_pixel_location_from_entity_location(entity)` -- entity position to screen pixel

### Rendering Flow

Each frame, `loop.render_screen(display)` (loops.py, line 299) calls:
1. `state_manager.update_display(display)` -- delegates to current state
2. Quest popup if needed
3. `pygame.display.update()`

For the main gameplay `ActionState`, the `update_display` typically:
1. Fill screen black
2. Calculate viewport around player
3. Draw tiles in visible range
4. Draw items
5. Draw monsters
6. Draw player with equipment overlays
7. Draw UI elements (minimap, health/mana orbs, exp bar, message log, context help)

### Tile Sprite System (static_configs.py)

`TileDict` (line 32) loads all sprites keyed by integer IDs:

**ID Ranges:**
| Range | Type |
|-------|------|
| 0 | Placeholder |
| 100-195 | Floors (colorful, dirty, carpet, wood, stone, forest, sand, ocean, blood, rounded) |
| 200-250 | Walls |
| 300-323 | Doors (closed/open) |
| 400-435 | Stairs and Gateways |
| 500 | Fire effect |
| 600 | Traps |
| 700-743 | Interactables (fountains, idols, campfires, plants, orb pedestals) |
| 1000-1034 | Player + overlays |
| 1100-1131 | NPCs |
| 1200 | Gold |
| 2000-2501 | Monsters (ooze, goblin, kobold, orc, spider, undead) |
| 3000-3610 | Weapons (swords, axes, hammers, daggers, bows, wands, shields) |
| 4000-4401 | Armor (body, helmet, gloves, boots, pants) |
| 5000-5110 | Accessories (rings, amulets) |
| 6000-6400 | Consumables (potions, scrolls, books, flowers) |
| 7000-7001 | Key orbs (forest, ocean) |
| 8000-8108 | UI equipment slot icons (closed/open) |
| 9000-9901 | UI skills, buttons, speech bubble |

Negative IDs (e.g., `-9102`) are dark/disabled versions of skill icons.

### Constants (display_generation/ui_constants.py)

- `UIColors` -- color definitions for UI elements
- `UILayout` -- layout calculations and constants
- `HelpText` -- per-state help bar text
- `EquipmentTileIDs` -- tile IDs for equipment overlays
- `UITileIDs` -- tile IDs for UI elements

---

## 7. Dungeon Generation Flow

### DungeonGenerator (dungeon_generation/mapping.py, line 91)

Constructor creates a complete floor:

```python
def __init__(self, depth, player, branch, dungeon_data, use_legacy_spawning=False, gateway_data=None):
    self.mapData = dungeon_data.get_map_data(branch, depth)
    self.spawn_params = branch_params[branch]
    self.tile_map = TileMap(self.mapData, depth, branch, gateway_data=gateway_data)
    self.monster_map = TrackingMap(self.get_width(), self.get_height())
    self.interact_map = TrackingMap(self.get_width(), self.get_height())
    self.item_map = TrackingMap(self.get_width(), self.get_height())
    place_spawn_interactables(self, interactable_spawner)
    place_spawn_items(self, item_spawner)
    self._spawn_monsters_with_strategy()
```

### Map Generation (TileMap)

`TileMap.__init__()` (dungeon_generation/maps/tilemap.py, line 86):
1. Gets generator via `_get_generator(mapData)` factory (line 23)
2. Calls `generator.generate()` + `generator.get_rooms()` + `generator.get_entity_map()`
3. Branch-specific: Ocean -> `add_ocean_water()`, Forest -> `apply_forest_theme()`
4. `place_stairs(self)` and optionally `place_gateways(self, gateway_data)`

**Generator types** (selected by `mapData.generator_type`):
- `"rooms_corridors"` -> `RoomsAndCorridorsGenerator(width, height, num_rooms, room_size, circularity)` -- default
- `"cave"` -> `CaveGenerator(width, height, fill_probability, smooth_iterations, wall_threshold, connect_regions)`
- `"pillar_hall"` -> `PillarHallGenerator(width, height, pillar_spacing, pillar_size, border_width, randomize_pillars, pillar_density)`

### Monster Spawning Strategies

Selected by `mapData.spawn_strategy`:
- `"random"` -> `RandomSpawnStrategy` -- random placement
- `"elite_group"` -> `EliteWithGroupStrategy` -- elite + minion pack
- `"guarding_items"` -> `GuardingItemsStrategy` -- monsters near items

### Game Initialization (loops.py, `init_game()`, line 607)

1. Creates `GatewayData()` configuration
2. Iterates all branches and depths, creating `DungeonGenerator` for each floor
3. Stores each generator in `memory.set_floor(branch, level, generator)`
4. `_pair_all_gateways()` connects gateway tiles between floors/branches
5. Sets starting position (player starts at Dungeon branch, floor 1, at up stairs)

### TrackingMap (dungeon_generation/maps/trackingmap.py, line 16)

Extends `Maps` with an ID-based entity tracking system:
- `self.dict = {}` -- maps entity IDs to entity objects
- `place_thing(thing)` -- assigns unique ID, places on grid
- `remove_thing(thing)` -- removes from grid and ID dict
- `move_entity(x1, y1, x2, y2)` -- moves between cells
- `get_entity(x, y)` -- returns entity object (not just ID)
- `get_all_entities()` -- returns all tracked entities
- `get_nearest_entity(x, y)` -- closest entity by distance
- `get_has_entity(x, y)` / `get_has_no_entity(x, y)` -- presence checks

### Branches

The game has multiple dungeon branches: `"Dungeon"`, `"Ocean"`, `"Forest"` (and potentially `"Hub"`)

Branch-specific features:
- **Ocean**: Tide system (tide_level oscillates -35 to -5), water terrain applied via `TileMap.apply_tide()`
- **Forest**: Day/night cycle affects monster damage (`nightify()`/`dayify()`), no health regen, forest-themed tiles

---

## 8. Monster AI and Combat System

### MonsterAI (monster_implementation/behaviors.py, line 46)

```python
class MonsterAI:
    def __init__(self, monster, behaviors: list):
        self.parent = monster
        self.behaviors = behaviors
        self.target = None
```

**`rank_actions(self, loop)`** (line 59):
- Evaluates all behaviors, picks highest score
- Always costs 1 energy: `self.parent.character.energy -= 1`
- Executes best behavior if score > 0

### Behavior Base Class (line 22)

```python
class Behavior:
    def __init__(self, name, tendency=(50, 10)):
        self.avg, self.spread = tendency
    def rank(self, monster, loop) -> int:   # Return utility 1-100, or -1 if invalid
    def execute(self, monster, loop):        # Perform the action
    def randomize(self) -> int:              # Random score from tendency
```

### Core Behaviors

| Behavior | File Line | Tendency | Triggers When |
|----------|-----------|----------|---------------|
| `CombatBehavior` | 96 | (80, 10) | Player in weapon range AND visible |
| `MoveBehavior` | 129 | (40, 20) | Player distance > 1.5 |
| `WaitBehavior` | 165 | (1, 0) | Always (fallback) |
| `FleeBehavior` | 178 | (100, 10) | Health < threshold (default 25%) |

### Monster-Specific Behaviors

| Monster | Factory Function | Special Behaviors |
|---------|-----------------|-------------------|
| Base | `create_base_behaviors()` (line 499) | combat + move + wait |
| Ooze | `create_ooze_behaviors()` (line 504) | `OozeMovesBehavior` -- destroys items on movement |
| Goblin | `create_goblin_behaviors()` (line 509) | `FindItemBehavior` + `PickupBehavior` + `FleeBehavior` |
| Orc | `create_orc_behaviors()` (line 521) | `BerserkBehavior` -- one-time berserk when HP < 25% |
| Spider | `create_spider_behaviors()` (line 526) | `SpinWebBehavior` -- one-time web placement |
| Kobold | `create_kobold_behaviors()` (line 531) | `RangedCombatBehavior` + `RepositionBehavior` + `BurningHandsBehavior` |
| Skeleton | `create_skeleton_behaviors()` (line 542) | Aggressive combat (80, 10) + move (40, 25) |
| Gargoyle | `create_gargoyle_behaviors()` (line 604) | `PetrifyGazeBehavior` -- random chance petrify |
| Minotaur | `create_minotaur_behaviors()` (line 643) | `ShrugOffBehavior` -- 75% chance to clear CC |
| Hobgoblin | `create_hobgoblin_behaviors()` (line 681) | `BlinkStrikeBehavior` -- teleport + attack |
| Stumpy | `create_stumpy_behaviors()` (line 830) | `StumpyBehavior` -- ambush when player < 3 tiles |
| Treant | `create_treant_behaviors()` (line 840) | Slow but powerful (move tendency 25, 10) |
| Metallic Bear | `create_metallic_bear_behaviors()` (line 879) | `FuryBehavior` -- berserk + haste when HP < 25% |
| Insect Nest | `create_insect_nest_behaviors()` (line 910) | `NestDefenseBehavior` -- immobile |
| Hornet | `create_hornet_behaviors()` (line 915) | Aggressive fast (combat 90, move 60) |
| Goblin Shaman | `create_goblin_shaman_behaviors()` (line 734) | `SummonBehavior` -- summons goblins |
| Tormentorb | `create_tormentorb_behaviors()` (line 772) | `TormentBehavior` -- torment spell at range |
| Golem | `create_golem_behaviors()` (line 954) | Very slow (move 20, 5) |

### Combat Flow (fighter.py, `do_attack`, line 46)

1. Calculate dodge: `dodge_percentage = defender.get_dodge_chance() - attacker.get_physical_hit_chance()`
2. Damage shave from dodge (0-100% reduction)
3. On-hit effects applied to defender (from weapon)
4. Damage = weapon damage * physical_damage_multiplier (from attributes)
5. Defense = armor - armor_piercing
6. Final damage = max(0, damage * shave - defense)
7. On-damage effects if damage > 0
8. `defender.character.take_damage(attacker, finalDamage)`

### Monster Day/Night (monsters/monster.py)

```python
def nightify(self):  # +2 min damage, +3 max damage
def dayify(self):    # revert night bonuses
```

---

## 9. Spell System Architecture

### Dual System (Old + New)

**Old system** (still active, being migrated):
- `old/spell.py` -- `Spell` class
- `old/spell_data.py` -- `SpellData` (NamedTuple-like), `EffectData`
- `old/spell_builder.py` -- `spell()` builder function, `get_all_spell_definitions()`
- `old/game_integration.py` -- `initialize_spell_system()`, `give_spell()`, `give_school_spells()`, etc.

**New class-based system**:
- `spell_system/base_spell.py` -- `BaseSpell` class (line 28)
- `spell_system/spell_registry.py` -- `SpellRegistry` singleton (line 16)
- `spell_system/effects/` -- composable effect building blocks
- `spell_system/spells/` -- concrete spell definitions
- `spell_system/status_effects.py` -- status effect classes (Berserk, Haste, Burn, etc.)
- `spell_system/school.py` -- School class

### SpellRegistry Singleton (spell_registry.py, line 16)

```python
class SpellRegistry:
    _instance = None
    def __new__(cls):    # Singleton via __new__
    def load_spells(self, spells_dir=None)   # loads from spell_system.spells package
    def create_spell(self, spell_id, caster, **overrides)  # -> Spell instance
    def get_spell_data(self, spell_id) -> Optional[SpellData]
    def get_spells_by_school(self, school) -> List[SpellData]
    def get_learnable_spells(self, intelligence) -> List[SpellData]
```

### BaseSpell (base_spell.py, line 28)

```python
class BaseSpell:
    name = "Unnamed Spell"
    cost = 5; cooldown = 10; range = 5; action_cost = 50
    icon = 9100; required_intelligence = 0
    target_type = TargetType.SINGLE_ENEMY
    effects = []; terrain_effects = []

    def __init__(self, caster):
        self.caster = caster; self.ready = 0

    def castable(self, target=None) -> bool    # checks cooldown + mana + range
    def try_to_activate(self, target, loop) -> bool  # sets cooldown, calls activate
    def activate(self, target, loop) -> bool   # creates context, deducts mana, applies effects
    def in_range(self, target) -> bool         # distance check, -1 = unlimited
    def tick_cooldown(self)                    # reduce ready by 1
```

### Casting Flow

1. `player.cast_spell(args)` -> `player.mage.cast_spell(args)`
2. Spell's `try_to_activate(target, loop)` checks `castable()`, sets `self.ready = self.cooldown`
3. `activate(target, loop)`:
   a. Creates `SpellContext(caster, loop, target)`
   b. Deducts `self.caster.character.mana -= self.cost`
   c. Gets entity targets via `get_targets(target, context)`
   d. Gets terrain targets via `get_terrain_targets(target, context)`
   e. Applies each effect to each target
   f. Adds messages from context

### Effect Builders (spell_system/effects/builders.py)

Available as direct imports from `spell_system`:
`damage, heal, lifesteal, apply_status, self_buff, message, custom, aoe_damage, teleport, blink, swap_positions, blink_to_target, summon, restore_mana, self_damage`

### Game Integration

`give_spell(entity, spell_id)` -- from `old/game_integration.py`, gives a spell to an entity:
```python
from spell_system import give_spell
give_spell(self, 'burning_attack')
```

---

## 10. Save/Load System

### Memory class (loop_workflow/memory.py, line 6)

Uses `dill` (extended pickle) for serialization.

```python
class Memory:
    def __init__(self):
        self.floor_level = 0
        self.branch = ""
        self.generators = {}   # {branch: {depth: DungeonGenerator}}
        self.player = None
        self.keyboard = None
```

**Key methods:**
- `set_floor(branch, depth, generator)` -- stores a floor's generator
- `get_saved_floor(branch, depth)` -- retrieves generator
- `get_current_saved_floor()` -- returns `generators[branch][floor_level]`
- `set_memory(floor_level, branch, player, keyboard)` -- sets current state
- `save_objects()` (line 39) -- serializes `[floor_level, generators, player, branch, keyboard]` to `data.dill`
- `load_objects()` (line 49) -- deserializes from `data.dill`

**Save/Load Flow:**
- Save: `loop.memory.update_memory(floor_level, branch)` -> `save_objects()` -> writes `data.dill`
- Load: `loop.load_game()` (loops.py, line 751) -> `memory.load_objects()` -> restores all state

The entire game state (all floor generators, player, keyboard bindings) is serialized in one dill dump. This means every entity, map, and component must be pickle-compatible.

---

## 11. FOV / Visibility System

### Symmetric Shadowcasting (navigation_utility/shadowcasting.py)

`compute_fov(loop)` (line 4):
1. Gets player origin and tile_map
2. Clears all `tile.visible = False`
3. Sets player tile as seen+visible
4. For each of 4 quadrants (N, E, S, W), runs recursive `scan()` with `Row` and slope tracking
5. Visibility radius is hardcoded to 8 tiles: `if distance(tile) < 8: reveal(tile)`

**Classes:**
- `Quadrant(cardinal, origin)` -- transforms local coordinates to map coordinates
- `Row(depth, start_slope, end_slope)` -- tracks a row of tiles being scanned

**Tile visibility properties** (set by shadowcasting):
- `tile.visible` -- currently visible this turn
- `tile.seen` -- has been seen at least once (for fog of war)

---

## 12. Pathfinding (navigation_utility/pathfinding.py)

### A* Pathfinding

```python
def astar(maze, start, goal, monster_map, player, monster_blocks=False, player_blocks=False)
def astar_multi_goal(maze, start, goals, monster_map, player, monster_blocks=False, player_blocks=False)
```

- `Node` class: parent, position, g (cost so far), f (g + heuristic)
- Multi-goal variant searches in reverse (from goals to start)
- Max 500 nodes checked before giving up
- `monster_blocks` parameter controls whether monsters are treated as obstacles

### BFS for Auto-Explore

```python
def conditional_bfs(maze, start, goal_condition, npc_ID)
```

- Uses a callback `goal_condition(position_tuple) -> bool` to find first matching position
- `npc_ID` is the interact_map dict, used to avoid NPCs
- Returns path as list of `(x, y)` tuples

---

## 13. Key Configuration Files

| File | Purpose |
|------|---------|
| `src/core/constants.py` | Game constants (tile IDs, action costs, colors, dungeon config) |
| `src/core/enums.py` | `LoopType` enum (all game states) |
| `src/core/player_config.py` | Player starting values (health, mana, debug mode) |
| `src/core/directions.py` | `Directions.ALL_8` -- 8-directional movement tuples |
| `src/core/movement.py` | `MovementValidator.can_move_to()` -- movement validation |
| `src/core/asset_registry.py` | Tile ID documentation and ranges |
| `global_vars.py` | Debug flags (`global_bugtesting`, `SHOW_PATHFINDING_DEBUG`, etc.) |
| `static_configs.py` | `TileDict` -- loads all sprite assets |
| `logging_config.py` | Logger setup (`get_logger(__name__)`) |
| `dungeon_generation/configuration_data/` | `MapData`, `DungeonData`, `GatewayData` config classes |
| `dungeon_generation/spawning/branch_params.py` | Per-branch spawn parameters |

---

## 14. Directory Structure (Key Directories)

```
RogueGame-main/
  loops.py                           # Central game controller (Loops class)
  objects.py                         # Base Objects class
  player.py                          # Player class
  global_vars.py                     # Debug flags
  static_configs.py                  # TileDict sprite loading
  logging_config.py                  # Logger configuration
  main.py                            # Entry point

  character_implementation/          # Character composition components
    character.py                     # Character (health, mana, energy, status)
    attributes.py                    # Attributes (str, dex, int, end, armor, xp)
    fighter.py                       # Fighter (combat)
    inventory.py                     # Inventory (items)
    body_slot.py                     # Body (equipment slots)
    mage.py                          # Mage (spells)
    status.py                        # Status (effects)
    statistics.py                    # StatTracker

  monsters/                          # Monster definitions
    monster.py                       # Base Monster class
    (specific monster submodules)

  monster_implementation/            # Monster AI
    behaviors.py                     # Behavior classes + MonsterAI + factory functions
    __init__.py                      # Exports MonsterAI, create_base_behaviors, etc.

  item_implementation/               # Items and equipment
    items.py                         # Item, Gold, Consumeable base classes
    equipment.py                     # Equipment class
    weapons/                         # Weapon definitions
    armor/                           # Armor definitions
    consumables/                     # Potion/scroll definitions
    jewelry/                         # Ring/amulet definitions

  dungeon_generation/                # Map and dungeon creation
    mapping.py                       # DungeonGenerator class
    mapping_utility.py               # Spawn placement helpers
    maps/
      maps.py                        # Maps base class
      tilemap.py                     # TileMap class
      trackingmap.py                 # TrackingMap class
      map_utility.py                 # Stairs, gateway, water, forest placement
    generators/                      # Map generation strategies
      rooms_corridors.py             # RoomsAndCorridorsGenerator
      cave.py                        # CaveGenerator (cellular automata)
      pillar_hall.py                 # PillarHallGenerator
    spawn_strategies/                # Monster spawn strategies
      random_spawn.py                # RandomSpawnStrategy
      elite_group.py                 # EliteWithGroupStrategy
      guarding_items.py              # GuardingItemsStrategy
    spawning/                        # Spawn data
      branch_params.py               # Per-branch parameters
      monster_spawner.py             # Monster list generation
      item_spawner.py                # Item list generation
      interactable_spawner.py        # NPC/interactable generation
    tiles/                           # Tile classes (Floor, Wall, Door, Stairs, Gateway)
    terrain/                         # Terrain effects (Water, Web, Fire, etc.)
    configuration_data/              # MapData, DungeonData, GatewayData

  spell_system/                      # New spell system
    __init__.py                      # Package exports
    base_spell.py                    # BaseSpell class
    spell_registry.py                # SpellRegistry singleton
    context.py                       # SpellContext
    targeting.py                     # TargetType enum, targeting helpers
    school.py                        # School class
    effects/                         # Effect system
      builders.py                    # damage(), heal(), etc.
    spells/                          # Concrete spell definitions
    status_effects.py                # Berserk, Haste, Burn, etc.

  old/                               # Legacy spell system (being migrated)
    spell.py                         # Spell class
    spell_data.py                    # SpellData, EffectData
    spell_builder.py                 # spell() builder function
    game_integration.py              # give_spell(), initialize_spell_system()

  loop_workflow/                     # Game state management
    game_states.py                   # GameState ABC + StateManager
    states/                          # Concrete state implementations
      gameplay_states.py             # ActionState, TargetingState, etc.
      menu_states.py                 # MainMenuState, PausedState, etc.
      inventory_states.py            # InventoryState, EquipmentState, etc.
      spell_states.py                # SpellListState, etc.
      modal_states.py                # DeathState, VictoryState, etc.
      automated_states.py            # RestingState, PathingState
      binding_state.py               # BindingState
      class_state.py                 # ClassState
    memory.py                        # Memory (save/load)
    message_handler.py               # MessageHandler
    targets.py                       # Target helper
    loop_utility.py                  # Utility functions

  display_generation/                # Rendering
    display.py                       # Display class
    ui.py                            # UI component creation
    ui_constants.py                  # UIColors, UILayout, HelpText, etc.
    ui_utils.py                      # draw_on_button, get_status_text, etc.

  navigation_utility/                # Pathfinding and FOV
    pathfinding.py                   # A* and BFS
    shadowcasting.py                 # Symmetric shadowcasting FOV

  src/core/                          # Core constants and enums
    enums.py                         # LoopType
    constants.py                     # Game constants
    player_config.py                 # Player config
    directions.py                    # Directions.ALL_8
    movement.py                      # MovementValidator
    asset_registry.py                # Tile ID reference
    asset_cache.py                   # AssetCache for image loading

  assets/                            # Sprite/image assets
    tiles/                           # Floor, wall, door, stairs tiles
    items/                           # Item sprites
    player/                          # Player sprites
    npc/                             # NPC sprites
    skills/                          # Skill icon sprites
    ui/                              # UI element sprites
    crawl-tiles/                     # Crawl tileset assets
```

---

## 15. Common Edit Patterns

### Adding a New Monster

1. Create class in `monsters/` inheriting from `Monster`
2. Add behavior factory in `monster_implementation/behaviors.py`
3. Add sprite to `static_configs.py` TileDict
4. Add to monster spawner in `dungeon_generation/spawning/monster_spawner.py`

### Adding a New Spell

1. Create spell class in `spell_system/spells/` inheriting from `BaseSpell`
2. Register effects using builders from `spell_system/effects/builders.py`
3. Add icon to `static_configs.py`
4. Register via `SpellRegistry` or `spell_builder`

### Adding a New Item

1. Create class in `item_implementation/` inheriting from `Item`, `Equipment`, or `Consumeable`
2. Add sprite to `static_configs.py`
3. Add to item spawner in `dungeon_generation/spawning/item_spawner.py`

### Adding a New Game State

1. Create class in `loop_workflow/states/` inheriting from `GameState`
2. Set `loop_type = LoopType.your_state`
3. Add enum value to `LoopType` in `src/core/enums.py`
4. Add to `create_all_states()` in `loop_workflow/states/__init__.py`
5. Implement `create_display()`, `update_display()`, `handle_input()`

### Modifying Combat

- Damage formula is in `fighter.py`, `do_attack()` (line 46)
- Status effects are in `character_implementation/status.py` and `spell_system/status_effects.py`
- On-hit/on-damage effects come from weapons via `fighter.do_on_hit_effect()` (line 73) and `fighter.do_on_damage_effect()` (line 77)

### Floor Transitions

- Stairs: `player.down_stairs(loop)` -> `loop.change_floor()` (loops.py, line 489)
- Gateways: `player.do_gateway(loop)` -> `loop.change_branch()` (loops.py, line 547)
- Stairs are paired lazily on first use
- Gateways are paired during `init_game()` via `_pair_all_gateways()`
