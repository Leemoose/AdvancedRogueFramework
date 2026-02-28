# RogueGame Architecture Reference

This is the detailed reference companion to the main SKILL.md. It contains full function signatures with line numbers, complete behavior tables, and the full directory tree.

## Table of Contents

1. [Key Function Signatures](#1-key-function-signatures)
2. [Combat Formula Detail](#2-combat-formula-detail)
3. [Monster Behavior Table](#3-monster-behavior-table)
4. [Spell System Detail](#4-spell-system-detail)
5. [Save/Load System](#5-saveload-system)
6. [FOV and Pathfinding](#6-fov-and-pathfinding)
7. [Display Pipeline](#7-display-pipeline)
8. [Dungeon Generation Detail](#8-dungeon-generation-detail)
9. [Full Directory Tree](#9-full-directory-tree)

---

## 1. Key Function Signatures

### Player Actions (player.py)

```python
def attack_move(self, move_x, move_y, loop)         # line 96 - main movement/combat entry point
def move(self, move_x, move_y, loop)                 # line 122 - raw movement
def attack(self, defender, loop)                      # line 135 - melee attack
def spend_energy(self, action_type: str) -> bool      # line 77 - energy deduction
def autopath(self, loop)                              # line 146 - auto-movement along path
def autoexplore(self, loop)                           # line 187 - BFS-based auto-explore
def find_stairs(self, loop)                           # line 234 - pathfind to stairs/gateways
def smart_attack(self, loop)                          # line 315 - auto-target nearest visible monster
def do_grab(self, item, loop)                         # line 392 - pick up item
def do_equip(self, item)                              # line 406 - equip item
def cast_spell(self, *args)                           # line 385 - delegates to mage.cast_spell
def gain_experience(self, experience)                 # line 92 - XP gain + level check
def check_for_levelup(self)                           # line 295 - level up loop
def down_stairs(self, loop)                           # line 348 - use stairs/gateway going down
```

### Combat (character_implementation/fighter.py)

```python
def do_attack(self, defender, loop)                   # line 46 - full attack resolution
def get_damage(self)                                  # line 69 - weapon damage + base
def do_defend(self)                                   # line 22 - returns armor value
def get_physical_hit_chance(self)                     # line 61 - accuracy roll
def get_dodge_chance(self)                            # line 65 - evasion roll
def do_on_hit_effect(self, target, loop)              # line 73 - weapon on-hit effects
def do_on_damage_effect(self, target, loop)           # line 77 - weapon on-damage effects
```

### Character (character_implementation/character.py)

```python
def __init__(self, parent, mana=0, health=10, experience_given=0)  # line 12
def take_damage(self, dealer, damage)                 # line 65 - damage application, death handling
def tick_all_status_effects(self, loop)               # line 102 - process status effects per turn
def tick_regen(self)                                  # line 152 - health/mana regen
def needs_rest(self)                                  # line 156 - check if rest needed
def rest(self, loop, returnLoop)                      # line 164 - rest mechanic
def is_alive(self)                                    # line 59 - health check
def can_take_action(self)                             # line 309 - status allows actions
def can_move(self)                                    # line 312 - status allows movement
def add_skill(self, new_skill)                        # line 205 - add spell to mage
def get_attribute(self, attribute)                    # line 241 - universal attribute getter
def change_attribute(self, attribute, change)         # line 265 - universal attribute setter
def skill_damage_increase(self)                       # line 82 - intelligence-based damage bonus
```

Action costs dict (character.py, line 22):
```python
self.action_costs = {
    "attack": 100, "move": 100, "grab": 30, "equip": 100,
    "unequip": 50, "quaff": 10, "read": 20, "drop": 10, "activate": 25
}
```

### Loops Controller (loops.py)

```python
def __init__(self, tileDict, display, keyboard, dungeon_data)  # line 59
def change_loop(self, new_loop)                       # line 119 - state transition
def action_loop(self, keyboard, display) -> bool      # line 138 - main frame loop
def monster_loop(self, energy)                        # line 321 - monster AI processing
def time_passes(self, time)                           # line 382 - game time advancement
def change_floor(self, level_change=-1, random_location=False)  # line 489 - floor transition
def change_branch(self)                               # line 547 - branch transition via gateway
def init_game(self)                                   # line 607 - new game initialization
def load_game(self)                                   # line 751 - load saved game
def clean_up(self)                                    # line 343 - remove dead/destroyed entities
def add_message(self, message, color=(255,255,255))   # line 825 - add to message log
def start_targetting(self, start_on_player=False)     # line 778 - enter targeting mode
def render_screen(self, display)                      # line 299 - render current frame
```

### DungeonGenerator (dungeon_generation/mapping.py)

```python
def __init__(self, depth, player, branch, dungeon_data, use_legacy_spawning=False, gateway_data=None)  # line 91
def get_passable(self, location: tuple) -> bool       # line 270 - checks all maps
def get_random_passable_location(self, stairs_block=True)  # line 214
def get_monsters_in_sight(self)                       # line 246 - visible monsters list
def place_monster_at_location(self, creature, x, y)   # line 300
def place_item_at_location(self, item, x, y)          # line 307
def get_is_in_corridor(self, x, y)                    # line 327 - corridor detection heuristic
```

### Objects Base (objects.py)

```python
def __init__(self, x=-1, y=-1, id_tag=-1, render_tag=-1, name="Unknown object")  # line 3
def has_trait(self, trait)                             # line 15 - returns self.traits[trait] or False
def get_location(self)                                # line 24 - returns (self.x, self.y)
def get_distance(self, x, y)                          # line 27 - Euclidean distance
def set_location(self, x, y)                          # line 54
def get_render_tag(self)                              # line 30 - sprite ID for TileDict
def gain_ID(self, ID)                                 # line 21 - sets id_tag from TrackingMap
```

---

## 2. Combat Formula Detail

Full attack resolution in `fighter.py`, `do_attack()` (line 46):

1. `dodge_percentage = defender.get_dodge_chance() - attacker.get_physical_hit_chance()`
2. `damage_shave = 1 - (max(min(dodge_percentage, 100), 0) / 100)`
3. Apply on-hit effects to defender (from weapon)
4. `damage = self.get_damage() * physical_damage_multiplier` (multiplier from attributes/buffs)
5. `defense = defender.do_defend() - self.get_armor_piercing()`
6. `finalDamage = max(0, int(damage * damage_shave) - defense)`
7. Apply on-damage effects if damage > 0
8. `defender.character.take_damage(self.parent, finalDamage)`

Damage sources:
- `get_damage()`: weapon min/max (from body_slot) + base damage + strength bonus
- `do_defend()`: total armor from all equipped items
- `get_physical_hit_chance()`: dexterity-based
- `get_dodge_chance()`: dexterity-based

---

## 3. Monster Behavior Table

Each monster has a behavior factory function in `monster_implementation/behaviors.py`:

| Monster | Factory | Special Behaviors | Notes |
|---|---|---|---|
| Base | `create_base_behaviors()` L499 | combat + move + wait | Default for unspecialized monsters |
| Ooze | `create_ooze_behaviors()` L504 | `OozeMovesBehavior` | Destroys items when it moves over them |
| Goblin | `create_goblin_behaviors()` L509 | `FindItemBehavior` + `PickupBehavior` + `FleeBehavior` | Steals items, flees when hurt |
| Orc | `create_orc_behaviors()` L521 | `BerserkBehavior` | One-time berserk at <25% HP |
| Spider | `create_spider_behaviors()` L526 | `SpinWebBehavior` | One-time web placement |
| Kobold | `create_kobold_behaviors()` L531 | `RangedCombatBehavior` + `RepositionBehavior` + `BurningHandsBehavior` | Ranged kiter with spell |
| Skeleton | `create_skeleton_behaviors()` L542 | — | Aggressive combat (80,10) + move (40,25) |
| Gargoyle | `create_gargoyle_behaviors()` L604 | `PetrifyGazeBehavior` | Random chance petrify |
| Minotaur | `create_minotaur_behaviors()` L643 | `ShrugOffBehavior` | 75% chance to clear crowd control |
| Hobgoblin | `create_hobgoblin_behaviors()` L681 | `BlinkStrikeBehavior` | Teleport + attack combo |
| Stumpy | `create_stumpy_behaviors()` L830 | `StumpyBehavior` | Ambush when player <3 tiles |
| Treant | `create_treant_behaviors()` L840 | — | Slow but powerful (move 25,10) |
| Metallic Bear | `create_metallic_bear_behaviors()` L879 | `FuryBehavior` | Berserk + haste at <25% HP |
| Insect Nest | `create_insect_nest_behaviors()` L910 | `NestDefenseBehavior` | Immobile spawner |
| Hornet | `create_hornet_behaviors()` L915 | — | Fast aggressive (combat 90, move 60) |
| Goblin Shaman | `create_goblin_shaman_behaviors()` L734 | `SummonBehavior` | Summons goblin minions |
| Tormentorb | `create_tormentorb_behaviors()` L772 | `TormentBehavior` | Torment spell at range |
| Golem | `create_golem_behaviors()` L954 | — | Very slow (move 20,5) |

### Behavior Base Class (line 22)

```python
class Behavior:
    def __init__(self, name, tendency=(50, 10)):
        self.avg, self.spread = tendency
    def rank(self, monster, loop) -> int:   # Return utility 1-100, or -1 if invalid
    def execute(self, monster, loop):        # Perform the action
    def randomize(self) -> int:              # Random score from Gaussian(avg, spread)
```

Core behaviors and their default tendencies:
- `CombatBehavior` (80, 10) — attacks when player in weapon range AND visible
- `MoveBehavior` (40, 20) — moves toward player when distance > 1.5
- `WaitBehavior` (1, 0) — always valid, fallback
- `FleeBehavior` (100, 10) — flees when health < threshold (default 25%)

---

## 4. Spell System Detail

### Dual System Warning

Two spell systems coexist. The old system (`old/`) is being migrated to the new one (`spell_system/`). New spells should use `spell_system/`.

### New System: BaseSpell (spell_system/base_spell.py, line 28)

```python
class BaseSpell:
    name = "Unnamed Spell"
    cost = 5; cooldown = 10; range = 5; action_cost = 50
    icon = 9100; required_intelligence = 0
    target_type = TargetType.SINGLE_ENEMY
    effects = []; terrain_effects = []

    def __init__(self, caster):
        self.caster = caster; self.ready = 0

    def castable(self, target=None) -> bool
    def try_to_activate(self, target, loop) -> bool
    def activate(self, target, loop) -> bool
    def in_range(self, target) -> bool
    def tick_cooldown(self)
```

### SpellRegistry (spell_registry.py, line 16)

```python
class SpellRegistry:
    _instance = None    # Singleton via __new__
    def load_spells(self, spells_dir=None)
    def create_spell(self, spell_id, caster, **overrides) -> Spell
    def get_spell_data(self, spell_id) -> Optional[SpellData]
    def get_spells_by_school(self, school) -> List[SpellData]
    def get_learnable_spells(self, intelligence) -> List[SpellData]
```

### Effect Builders (spell_system/effects/builders.py)

Available imports: `damage`, `heal`, `lifesteal`, `apply_status`, `self_buff`, `message`, `custom`, `aoe_damage`, `teleport`, `blink`, `swap_positions`, `blink_to_target`, `summon`, `restore_mana`, `self_damage`

### Casting Flow

1. `player.cast_spell(args)` → `player.mage.cast_spell(args)`
2. `spell.try_to_activate(target, loop)` checks `castable()`, sets cooldown
3. `spell.activate(target, loop)`:
   - Creates `SpellContext(caster, loop, target)`
   - Deducts mana: `self.caster.character.mana -= self.cost`
   - Gets entity targets via `get_targets(target, context)`
   - Gets terrain targets via `get_terrain_targets(target, context)`
   - Applies each effect to each target
   - Adds messages from context

### Giving Spells to Entities

```python
from spell_system import give_spell
give_spell(entity, 'burning_attack')
```

Or via old system: `from old.game_integration import give_spell`

---

## 5. Save/Load System

### Memory (loop_workflow/memory.py, line 6)

```python
class Memory:
    def __init__(self):
        self.floor_level = 0
        self.branch = ""
        self.generators = {}   # {branch: {depth: DungeonGenerator}}
        self.player = None
        self.keyboard = None

    def set_floor(self, branch, depth, generator)
    def get_saved_floor(self, branch, depth) -> DungeonGenerator
    def get_current_saved_floor(self) -> DungeonGenerator
    def set_memory(self, floor_level, branch, player, keyboard)
    def save_objects(self)       # line 39 - serializes to data.dill
    def load_objects(self)       # line 49 - deserializes from data.dill
```

Save format: `[floor_level, generators, player, branch, keyboard]` serialized via `dill.dump()`.

The entire game state is in one binary blob. Everything must be dill-serializable.

---

## 6. FOV and Pathfinding

### FOV: Symmetric Shadowcasting (navigation_utility/shadowcasting.py)

`compute_fov(loop)` (line 4):
1. Gets player origin and tile_map
2. Clears all `tile.visible = False`
3. Sets player tile as seen + visible
4. For each of 4 quadrants (N, E, S, W), runs recursive `scan()` with `Row` and slope tracking
5. Visibility radius: 8 tiles

Key classes: `Quadrant(cardinal, origin)`, `Row(depth, start_slope, end_slope)`

Tile visibility properties:
- `tile.visible` — currently visible this turn
- `tile.seen` — has ever been seen (fog of war)

### Pathfinding (navigation_utility/pathfinding.py)

```python
def astar(maze, start, goal, monster_map, player, monster_blocks=False, player_blocks=False)
def astar_multi_goal(maze, start, goals, monster_map, player, monster_blocks=False, player_blocks=False)
def conditional_bfs(maze, start, goal_condition, npc_ID)
```

- A* uses `Node(parent, position, g, f)` with max 500 nodes
- Multi-goal variant searches from goals to start (reverse)
- BFS uses callback `goal_condition(position) -> bool`
- `npc_ID` is the interact_map dict, used to avoid NPCs

---

## 7. Display Pipeline

### Display (display_generation/display.py, line 12)

```python
def __init__(self, width, height, textSize, textWidth, textHeight)
def update_main(self, loop)              # renders main menu
def draw_player(self, loop)              # player sprite + equipment overlays
def screen_to_tile(self, player, x, y)   # pixel coords → tile coords (line 52)
def update_sizes(self)                   # recalculate after resize
def handle_resize(self)                  # window resize handling
def get_pixel_location_from_entity_location(self, entity)
```

### Rendering Flow Per Frame

`loop.render_screen(display)` (loops.py, line 299):
1. `state_manager.update_display(display)` — delegates to current state
2. Quest popup if needed
3. `pygame.display.update()`

For `ActionState`, `update_display` does:
1. Fill screen black
2. Calculate viewport around player
3. Draw tiles in visible range
4. Draw items, monsters, player with equipment overlays
5. Draw UI (minimap, health/mana orbs, exp bar, message log, context help)

### UI Constants (display_generation/ui_constants.py)

- `UIColors` — color definitions
- `UILayout` — layout calculations (`get_tile_viewport()`, etc.)
- `HelpText` — per-state context help text
- `EquipmentTileIDs` — tile IDs for equipment overlays on player
- `UITileIDs` — tile IDs for UI elements

---

## 8. Dungeon Generation Detail

### DungeonGenerator Constructor (mapping.py, line 91)

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

### Map Generator Types

Selected by `mapData.generator_type`:
- `"rooms_corridors"` → `RoomsAndCorridorsGenerator(width, height, num_rooms, room_size, circularity)`
- `"cave"` → `CaveGenerator(width, height, fill_probability, smooth_iterations, wall_threshold, connect_regions)`
- `"pillar_hall"` → `PillarHallGenerator(width, height, pillar_spacing, pillar_size, border_width, randomize_pillars, pillar_density)`

### Monster Spawn Strategies

Selected by `mapData.spawn_strategy`:
- `"random"` → `RandomSpawnStrategy`
- `"elite_group"` → `EliteWithGroupStrategy`
- `"guarding_items"` → `GuardingItemsStrategy`

### TrackingMap (dungeon_generation/maps/trackingmap.py, line 16)

```python
self.dict = {}                    # maps entity IDs to entity objects
def place_thing(self, thing)      # assigns unique ID, places on grid
def remove_thing(self, thing)     # removes from grid and ID dict
def move_entity(self, x1, y1, x2, y2)
def get_entity(self, x, y)       # returns entity object (not just ID)
def get_all_entities(self)
def get_nearest_entity(self, x, y)
def get_has_entity(self, x, y)
def get_has_no_entity(self, x, y)
```

### Branches

- **Dungeon**: Standard dungeon, rooms_corridors generator
- **Ocean**: Tide system (`tide_level` oscillates -35 to -5), `TileMap.apply_tide()` changes water tiles
- **Forest**: Day/night cycle affects monster damage (`nightify()`/`dayify()`), no health regen, forest-themed tiles

### Game Initialization (loops.py, `init_game()`, line 607)

1. Creates `GatewayData()` configuration
2. Iterates all branches and depths, creating `DungeonGenerator` for each floor
3. Stores each in `memory.set_floor(branch, level, generator)`
4. `_pair_all_gateways()` connects gateway tiles between floors/branches
5. Player starts at Dungeon branch, floor 1, at up stairs

---

## 9. Full Directory Tree

```
RogueGame-main/
  roguewriting.py                    # Entry point
  loops.py                           # Central game controller (Loops class)
  objects.py                         # Base Objects class
  player.py                          # Player class
  global_vars.py                     # Debug flags
  static_configs.py                  # TileDict sprite loading
  logging_config.py                  # Logger configuration
  requirements.txt                   # Dependencies: pygame, pygame_gui, dill

  src/core/
    enums.py                         # LoopType enum
    constants.py                     # GameTime, ActionCost, Colors, NO_ENTITY, TILE_SIZE
    player_config.py                 # PlayerConfig (starting health/mana, debug mode)
    directions.py                    # Directions.ALL_8
    movement.py                      # MovementValidator.can_move_to()
    asset_registry.py                # Tile ID documentation and ranges
    asset_cache.py                   # AssetCache for image loading

  character_implementation/
    character.py                     # Character (HP, mana, energy, status effects)
    attributes.py                    # Attributes (str, dex, int, end, armor, xp)
    fighter.py                       # Fighter (combat damage, attack/defend)
    inventory.py                     # Inventory (item storage)
    body_slot.py                     # Body (equipment slots)
    mage.py                          # Mage (spell list, casting)
    status.py                        # Status effect handling
    statistics.py                    # StatTracker

  monsters/
    monster.py                       # Base Monster class
    (specific monster submodules)

  monster_implementation/
    behaviors.py                     # Behavior classes + MonsterAI + all factory functions
    __init__.py                      # Exports MonsterAI, create_base_behaviors, etc.

  item_implementation/
    items.py                         # Item, Gold, Consumeable base classes
    equipment.py                     # Equipment class
    weapons/                         # Weapon definitions
    armor/                           # Armor definitions
    consumables/                     # Potion/scroll definitions
    jewelry/                         # Ring/amulet definitions

  dungeon_generation/
    mapping.py                       # DungeonGenerator class
    mapping_utility.py               # Spawn placement helpers
    maps/
      maps.py                        # Maps base class
      tilemap.py                     # TileMap class
      trackingmap.py                 # TrackingMap class
      map_utility.py                 # Stairs, gateway, water, forest placement
    generators/
      rooms_corridors.py             # RoomsAndCorridorsGenerator
      cave.py                        # CaveGenerator (cellular automata)
      pillar_hall.py                 # PillarHallGenerator
    spawn_strategies/
      random_spawn.py                # RandomSpawnStrategy
      elite_group.py                 # EliteWithGroupStrategy
      guarding_items.py              # GuardingItemsStrategy
    spawning/
      branch_params.py               # Per-branch spawn parameters
      monster_spawner.py             # Monster list generation
      item_spawner.py                # Item list generation
      interactable_spawner.py        # NPC/interactable generation
    tiles/                           # Tile classes (Floor, Wall, Door, Stairs, Gateway)
    terrain/                         # Terrain effects (Water, Web, Fire, etc.)
    configuration_data/              # MapData, DungeonData, GatewayData

  spell_system/
    __init__.py                      # Package exports
    base_spell.py                    # BaseSpell class
    spell_registry.py                # SpellRegistry singleton
    context.py                       # SpellContext
    targeting.py                     # TargetType enum, targeting helpers
    school.py                        # School class
    effects/
      builders.py                    # damage(), heal(), apply_status(), etc.
    spells/                          # Concrete spell definitions
    status_effects.py                # Berserk, Haste, Burn, etc.

  old/                               # Legacy spell system (being migrated)
    spell.py                         # Spell class
    spell_data.py                    # SpellData, EffectData
    spell_builder.py                 # spell() builder function
    game_integration.py              # give_spell(), initialize_spell_system()

  loop_workflow/
    game_states.py                   # GameState ABC + StateManager
    states/
      __init__.py                    # create_all_states() factory
      gameplay_states.py             # ActionState, TargetingState, ExamineState, SpecificExamineState
      menu_states.py                 # MainMenuState, PausedState, HelpState, StoryState
      inventory_states.py            # InventoryState, EquipmentState, ItemScreenState, EnchantState
      spell_states.py                # SpellListState, SpellIndividualState, QuickcastState
      modal_states.py                # DeathState, VictoryState, QuestState, TradeState, LevelUpState
      automated_states.py            # RestingState, PathingState
      binding_state.py               # BindingState
      class_state.py                 # ClassState
    memory.py                        # Memory (save/load with dill)
    message_handler.py               # MessageHandler
    targets.py                       # Target helper
    loop_utility.py                  # Utility functions

  display_generation/
    display.py                       # Display class
    ui.py                            # UI component creation
    ui_constants.py                  # UIColors, UILayout, HelpText, EquipmentTileIDs, UITileIDs
    ui_utils.py                      # draw_on_button, get_status_text, etc.

  navigation_utility/
    pathfinding.py                   # A* and BFS
    shadowcasting.py                 # Symmetric shadowcasting FOV
    spatial_queries.py               # Spatial query helpers

  interactable_implementation/       # NPCs, fountains, idols, etc.

  assets/                            # Sprite/image assets
    tiles/                           # Floor, wall, door, stairs tiles
    items/                           # Item sprites
    player/                          # Player sprites
    npc/                             # NPC sprites
    skills/                          # Skill icon sprites
    ui/                              # UI element sprites
    crawl-tiles/                     # Crawl tileset assets
    theme.json                       # pygame_gui theme

  Notes/                             # Developer notes
  Sprites/                           # Additional sprite references
```
