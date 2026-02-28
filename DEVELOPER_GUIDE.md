# RogueGame Developer Guide

A comprehensive guide for developers contributing to this Python roguelike built with Pygame.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Core Systems](#core-systems)
3. [Adding New Monsters](#adding-new-monsters)
4. [Adding New Items](#adding-new-items)
5. [Adding New Spells](#adding-new-spells)
6. [Dungeon Generation](#dungeon-generation)
7. [Game States & UI](#game-states--ui)
8. [Monster AI (Behavior System)](#monster-ai-behavior-system)
9. [NPC & Dialogue System](#npc--dialogue-system)
10. [Status Effect System](#status-effect-system)
11. [Combat System](#combat-system)
12. [Experience & Leveling](#experience--leveling)
13. [Save/Load System](#saveload-system)
14. [Event System](#event-system)
15. [Game Time & Turns](#game-time--turns)
16. [Configuration & Constants](#configuration--constants)
17. [File Structure Reference](#file-structure-reference)
18. [Common Patterns](#common-patterns)
19. [Testing](#testing)
20. [Debugging Tips](#debugging-tips)

---

## Architecture Overview

The game follows a composition-based architecture where entities (Player, Monsters, Items) share components for their functionality.

```
Objects (base class)
    ├── Player
    │   ├── Character (stats, status effects, energy)
    │   ├── Inventory
    │   ├── Body (equipment slots)
    │   ├── Fighter (combat)
    │   └── Mage (spells)
    │
    ├── Monster
    │   ├── Character
    │   ├── Inventory
    │   ├── Body
    │   ├── Fighter
    │   ├── Mage
    │   └── MonsterAI (behaviors)
    │
    └── Item
        ├── Equipment (weapons, armor)
        └── Consumable (potions, scrolls)
```

### Main Entry Points

- **`loops.py`** - Main game controller (`Loops` class)
- **`player.py`** - Player entity
- **`objects.py`** - Base `Objects` class for all game entities

---

## Core Systems

### The Loops Class (`loops.py`)

Central game coordinator handling:

- **State transitions** - Managing different screens (action, inventory, targeting, etc.)
- **Event processing** - Keyboard, mouse, window events via Pygame
- **Game time** - Energy-based turn system and monster AI updates
- **Floor transitions** - Moving between dungeon levels

```python
# Main game loop (called every frame)
loop.action_loop(keyboard, display)

# Change game state
loop.change_loop(LoopType.inventory)

# Initialize a new game
loop.init_game()
```

### The Energy System

Actions cost energy. When a character's energy goes negative, time passes:

```python
# In character.py
self.action_costs = {
    "attack": 100,
    "move": 100,
    "grab": 30,
    "equip": 100,
    # ...
}
```

When `player.character.energy < 0`, the game calls:
1. `time_passes()` - Tick status effects, cooldowns, regeneration
2. `monster_loop()` - Give monsters energy and let them act

### The Trait System

Entities use a trait dictionary for type checking:

```python
self.traits["monster"] = True
self.traits["goblins"] = True

# Check traits
if entity.has_trait("monster"):
    # ...
```

---

## Adding New Monsters

### Step 1: Create the Monster Class

Create a new file in `monsters/<category>/` (e.g., `monsters/demons/demon.py`):

```python
from monsters.monster import Monster
from monster_implementation import MonsterAI, create_base_behaviors

class Demon(Monster):
    def __init__(self, x=-1, y=-1, render_tag=1100, name="Demon",
                 experience_given=25, health=30, min_damage=5, max_damage=10,
                 rarity="Rare"):
        super().__init__(
            x=x, y=y, render_tag=render_tag, name=name,
            experience_given=experience_given, health=health,
            min_damage=min_damage, max_damage=max_damage,
            rarity=rarity, gold=10
        )
        # Use default behaviors or create custom ones
        self.brain = MonsterAI(self, create_base_behaviors())

        # Customize action costs (optional)
        self.character.action_costs["move"] = 80

        # Set description
        self.description = "A fearsome demon from the underworld."

        # Set base stats
        self.strength = 3
        self.dexterity = 2
        self.endurance = 2
        self.intelligence = 1

        # Add custom traits
        self.traits["demon"] = True
```

### Step 2: Register the Monster for Spawning

Edit `dungeon_generation/spawning/monster_initializations.py`:

```python
from monsters.demons.demon import Demon

# Add to the monster spawns list
MonsterSpawns.append(
    MonsterSpawnParams(
        Demon(),              # Instance of the monster
        minFloor=3,           # First floor it can appear
        maxFloor=10,          # Last floor it can appear
        branches=["Dungeon"], # Which branches
        rarity="Rare",        # Common or Rare
        group="demons",       # For pack spawning
        boss=False            # Is it a boss?
    )
)
```

### Step 3: Add Sprite

1. Add sprite image to `assets/` or `assets/crawl-tiles/`
2. Register in `static_configs.py`:

```python
tiles[1100] = image.load('assets/monsters/demon.png')
```

### Custom Monster Behaviors

Override `do_attack` for special attack effects:

```python
def do_attack(self, target, loop):
    self.character.change_energy(-self.character.get_action_cost("attack"))
    damage = self.fighter.do_attack(target, loop)
    if damage > 0:
        # Special effect: steal gold
        gold_taken = target.inventory.get_gold() // 2
        self.inventory.change_gold_amount(gold_taken)
        target.inventory.change_gold_amount(-gold_taken)
    return damage
```

---

## Adding New Items

### Equipment (Weapons, Armor)

Create in the appropriate subdirectory of `item_implementation/`:

```python
# item_implementation/weapons/swords/flaming_sword.py
from item_implementation.weapons.weapons import Weapon
from spell_implementation.effects.burn import Burn

class FlamingSword(Weapon):
    def __init__(self, render_tag=331):
        super().__init__(
            render_tag=render_tag,
            name="Flaming Sword",
            min_damage=5,
            max_damage=12
        )
        self.description = "A sword wreathed in eternal flames."
        self.rarity = "Rare"
        self.on_hit_effects = [self.apply_burn]

    def apply_burn(self, target, attacker, loop):
        effect = Burn(duration=3, damage=2, source=attacker)
        target.character.status.add_status_effect(effect)
```

### Consumables (Potions, Scrolls)

```python
# item_implementation/consumables/potions/fire_potion.py
from item_implementation.items import Consumeable

class FirePotion(Consumeable):
    def __init__(self, render_tag=406):
        super().__init__(render_tag, "Fire Resistance Potion")
        self.description = "Grants temporary fire resistance."
        self.equipment_type = "Potiorb"  # For potions
        self.traits["potion"] = True

    def activate_once(self, entity):
        # Add fire resistance status effect
        from spell_implementation.effects.fire_resist import FireResist
        entity.character.status.add_status_effect(FireResist(duration=20))
```

### Registering Items for Spawning

Edit `dungeon_generation/spawning/item_initializations.py`:

```python
from item_implementation.weapons.swords.flaming_sword import FlamingSword

SPAWN_CONFIG = [
    # ... existing items ...
    (FlamingSword, None, 3, 10),  # (Class, constructor_args, min_floor, max_floor)
]
```

---

## Adding New Spells

### Step 1: Create the Spell Class

Spells go in `spell_implementation/` organized by school:

```python
# spell_implementation/ice_school/frost_bolt.py
from spell_implementation import Spell
from spell_implementation.effects.slow import Slow

class FrostBolt(Spell):
    def __init__(self, parent, name="Frost Bolt", cooldown=8, cost=5,
                 range=6, action_cost=100, damage=4, slow_duration=3):
        super().__init__(parent, name, cooldown, cost, range, action_cost)
        self.damage = damage
        self.slow_duration = slow_duration
        self.targetted = True        # Requires target selection
        self.targets_monster = True  # Targets monsters
        self.render_tag = 920        # Icon asset ID

    def activate(self, defender, loop):
        # Deduct mana
        self.parent.character.change_mana(-self.cost)

        # Deal damage (scales with intelligence)
        total_damage = self.damage + self.parent.character.skill_damage_increase()
        defender.character.take_damage(self.parent, total_damage)

        # Apply slow effect
        effect = Slow(self.slow_duration + self.parent.character.skill_duration_increase())
        defender.character.status.add_status_effect(effect)

        loop.add_message(f"Frost bolt hits {defender.name}!")
        return True

    def castable(self, target):
        return super().castable(target) and self.in_range(target)

    def description(self):
        return f"{self.name}({self.cost} cost, {self.cooldown} CD, {self.damage} damage, slows)"
```

### Step 2: Add to a Spell School (Optional)

```python
# spell_implementation/ice_school/ice_school.py
from .frost_bolt import FrostBolt

ICE_SPELLS = [FrostBolt]
```

### Step 3: Add to Learnable Spells

Spells can be learned from books or granted by items. See `item_implementation/consumables/books/book.py`.

---

## Dungeon Generation

### Map Generators

Located in `dungeon_generation/generators/`:

| Generator | Description |
|-----------|-------------|
| `rooms_corridors.py` | Traditional rooms connected by L-shaped corridors |
| `cave.py` | Cellular automata organic caves |
| `pillar_hall.py` | Open space with pillar columns |

### Spawn Strategies

Located in `dungeon_generation/spawn_strategies/`:

| Strategy | Description |
|----------|-------------|
| `random_spawn.py` | Random monster placement |
| `elite_group.py` | Elite monster with minion pack |
| `guarding_items.py` | Monsters positioned near valuable items |

### Configuration

Dungeon layouts are configured in `dungeon_generation/configuration_data/`:

```python
# dungeon_data.py - Define branches and depths
# map_data.py - Define per-floor map parameters

class MapData:
    def __init__(self, width=50, height=50, generator_type='rooms_corridors',
                 spawn_strategy='random', spawn_params=None):
        # ...
```

### Adding a New Branch

1. Add branch configuration in `configuration_data/dungeon_data.py`
2. Add spawn parameters in `spawning/branch_params.py`
3. Add monster distributions in the branch params

---

## Game States & UI

### State Pattern

The game uses a State pattern (`loop_workflow/game_states.py`):

```python
class GameState(ABC):
    """Base class for all game states."""

    @abstractmethod
    def create_display(self, display): ...

    @abstractmethod
    def update_display(self, display): ...

    @abstractmethod
    def handle_input(self, key): ...

    def tick(self): ...  # For continuous updates (resting, pathing)
```

### Available States (`loop_workflow/looptype.py`)

| LoopType | Description |
|----------|-------------|
| `action` | Main gameplay - moving, attacking |
| `inventory` | Inventory management |
| `equipment` | Equipment/gear screen |
| `targeting` | Selecting spell targets |
| `spellbook` | Viewing known spells |
| `resting` | Auto-rest until healed |
| `pathing` | Auto-explore/auto-path |
| `levelup` | Allocating stat points |
| `death` | Game over screen |
| `victory` | Win screen |

### Adding a New Screen

1. Create screen in `display_generation/`:

```python
# display_generation/my_screen.py
def my_screen(display, loop):
    # Render your screen using display methods
    display.draw_text("Hello World", x=100, y=100)
```

2. Create state in `loop_workflow/states/`:

```python
# loop_workflow/states/my_state.py
from loop_workflow.game_states import GameState
from loop_workflow.looptype import LoopType

class MyState(GameState):
    loop_type = LoopType.my_state

    def create_display(self, display):
        pass

    def update_display(self, display):
        from display_generation.my_screen import my_screen
        my_screen(display, self.loop)

    def handle_input(self, key):
        if key == "escape":
            self._change_state(LoopType.action)
        return True
```

3. Register state in `loop_workflow/states/__init__.py`:

```python
def create_all_states(loop):
    return [
        # ... existing states ...
        MyState(loop),
    ]
```

4. Add LoopType enum in `loop_workflow/looptype.py`:

```python
class LoopType(Enum):
    # ... existing ...
    my_state = "my_state"
```

---

## Monster AI (Behavior System)

### Overview

Monsters use a behavior-based AI system (`monster_implementation/behaviors.py`). Each behavior:

1. **Ranks itself** (0-100 utility score, -1 if invalid)
2. **Executes** if selected as highest-ranked

### Creating Custom Behaviors

```python
from monster_implementation.behaviors import Behavior

class TeleportBehavior(Behavior):
    """Teleport away when health is low."""

    def __init__(self, tendency=(90, 10), threshold=0.3):
        super().__init__("teleport", tendency)
        self.threshold = threshold
        self.used = False

    def rank(self, ai, loop):
        if self.used:
            return -1
        char = ai.parent.character
        if char.get_health() / char.get_max_health() < self.threshold:
            return self.randomize()
        return -1

    def execute(self, ai, loop):
        monster = ai.parent
        x, y = loop.generator.get_random_passable_location()
        monster.set_location(x, y)
        loop.add_message(f"{monster.name} teleports away!")
        self.used = True
```

### Behavior Factory Functions

```python
# Add to monster_implementation/behaviors.py

def create_teleporter_behaviors():
    """Behaviors for a teleporting monster."""
    return [
        CombatBehavior(),
        MoveBehavior(),
        TeleportBehavior(),
        WaitBehavior(),
    ]
```

### Pre-built Behaviors

| Behavior | Description |
|----------|-------------|
| `CombatBehavior` | Attack player if in range |
| `MoveBehavior` | Path toward player |
| `WaitBehavior` | Do nothing (fallback) |
| `FleeBehavior` | Run away when low health |
| `FindItemBehavior` | Path to items on ground |
| `PickupBehavior` | Pick up items |
| `BerserkBehavior` | Activate berserk at low health |
| `SpinWebBehavior` | Create web terrain |
| `RangedCombatBehavior` | Attack from range only |
| `RepositionBehavior` | Maintain optimal distance |

---

## File Structure Reference

```
RogueGame-main/
├── loops.py                    # Main game controller
├── player.py                   # Player entity
├── objects.py                  # Base Objects class
├── static_configs.py           # Asset loading (TileDict)
├── logging_config.py           # Logging setup
│
├── character_implementation/   # Character components
│   ├── character.py           # Stats, energy, actions
│   ├── attributes.py          # STR, DEX, INT, END
│   ├── status.py              # Status effects
│   ├── inventory.py           # Item management
│   ├── body_slot.py           # Equipment slots
│   ├── fighter.py             # Combat calculations
│   └── mage.py                # Spell casting
│
├── monsters/                   # Monster definitions
│   ├── monster.py             # Base Monster class
│   ├── goblins/
│   ├── orcs/
│   ├── kobolds/
│   ├── spiders/
│   ├── oozes/
│   └── undead/
│
├── monster_implementation/     # Monster AI
│   └── behaviors.py           # Behavior-based AI system
│
├── item_implementation/        # Items
│   ├── items.py               # Base Item, Gold, Consumeable
│   ├── equipment.py           # Base Equipment class
│   ├── weapons/               # Weapon types
│   ├── armor/                 # Armor types
│   ├── talismans/             # Rings, amulets, orbs
│   └── consumables/           # Potions, scrolls, books
│
├── spell_implementation/       # Spells
│   ├── spell.py               # Base Spell class
│   ├── effects/               # Status effects (burn, slow, etc.)
│   ├── fire_school/
│   ├── necromancy_school/
│   └── mind_school/
│
├── dungeon_generation/         # Map generation
│   ├── mapping.py             # DungeonGenerator
│   ├── tiles.py               # Tile definitions
│   ├── maps/                  # TileMap, TrackingMap, Room
│   ├── generators/            # Map layout generators
│   ├── spawn_strategies/      # Monster placement strategies
│   ├── spawning/              # Monster/item spawn configs
│   ├── terrain/               # Terrain effects (web, etc.)
│   └── configuration_data/    # Branch/floor configs
│
├── display_generation/         # UI/Rendering
│   ├── display.py             # Main Display class
│   ├── main_screen.py         # Game world view
│   ├── inventory_screen.py
│   ├── spell_screen.py
│   └── ...                    # Other screens
│
├── loop_workflow/              # Game state management
│   ├── game_states.py         # State pattern implementation
│   ├── looptype.py            # LoopType enum
│   ├── states/                # State implementations
│   ├── keyboard.py            # Input handling
│   ├── bindings.py            # Key bindings
│   └── messages.py            # Message log
│
├── navigation_utility/         # Pathfinding & FOV
│   ├── pathfinding.py         # A* pathfinding
│   └── shadowcasting.py       # Field of view
│
└── assets/                     # Sprites and images
    ├── tiles/
    ├── player/
    ├── items/
    ├── skills/
    └── crawl-tiles/           # Dungeon Crawl tiles
```

---

## NPC & Dialogue System

### Overview

NPCs use a node-based `DialogueTree` system for conversations. Each node represents what the NPC says plus available player options. Options can trigger actions, set traits, and navigate to other nodes.

**Key files:**
- `interactable_implementation/dialogue.py` - Core dialogue tree system
- `interactable_implementation/npc.py` - NPC classes
- `interactable_implementation/quest.py` - Quest system

### Creating a Simple NPC

```python
from interactable_implementation.npc import NPC
from interactable_implementation.dialogue import DialogueTree, Option, END

class Merchant(NPC):
    def __init__(self, x=-1, y=-1, render_tag=121, name="Merchant"):
        super().__init__(x=x, y=y, render_tag=render_tag, name=name)

    def build_dialogue_tree(self) -> DialogueTree:
        tree = DialogueTree("greeting")

        tree.add_node("greeting", "Welcome to my shop!", [
            Option("What do you sell?", goto="wares"),
            Option("Goodbye.", goto=END),
        ])

        tree.add_node("wares", "I have potions and scrolls.", [
            Option("I'll browse.", goto=END),
            Option("Not interested.", goto=END),
        ])

        return tree
```

### Creating a Quest-Giving NPC

```python
from interactable_implementation.npc import QuestGiver
from interactable_implementation.quest import KillCountQuest
from interactable_implementation.dialogue import DialogueTree, Option, END

class BountyHunter(QuestGiver):
    def __init__(self, x=-1, y=-1, render_tag=125, name="Bounty Hunter"):
        self._custom_quest = KillCountQuest(
            name="Orc Bounty",
            target_count=3,
            monster_type="Orc",
            experience_given=50
        )
        super().__init__(x=x, y=y, render_tag=render_tag, name=name)
        self.quest = self._custom_quest

    def build_dialogue_tree(self) -> DialogueTree:
        tree = DialogueTree("greeting")

        tree.add_node("greeting", "Looking for work, adventurer?", [
            Option("What kind of work?", goto="explain"),
            Option("Not interested.", goto=END),
        ])

        tree.add_node("explain", "Orcs have been raiding caravans. Kill 3 of them.", [
            Option("I'll do it.", goto="accept", action=self._give_quest_action),
            Option("Too dangerous.", goto=END),
        ])

        tree.add_node("accept", "Good luck. Return when the job is done.", [
            Option("Farewell.", goto=END),
        ])

        # Quest completion node (QuestGiver routes here automatically)
        tree.add_node("quest_complete", "Well done! Here's your reward.", [
            Option("Thanks.", goto=END),
        ])

        return tree
```

### Dialogue System Features

**Random NPC text** - Pass a list for variety:
```python
tree.add_node("greet", ["Hello!", "Hi there!", "Greetings!"], [...])
```

**Conditional options** - Show only when condition is true:
```python
Option("Secret option", goto="secret",
       condition=lambda npc, loop: npc.has_trait("trusted"))
```

**Actions on selection** - Execute code when chosen:
```python
Option("Accept quest", goto="accepted",
       action=lambda npc, loop: npc.give_quest(loop))
```

**Set traits** - Mark state changes:
```python
Option("Earn trust", goto="next", sets=["trusted"])
```

**Node entry callbacks** - Run code when entering a node:
```python
tree.add_node("shop", "Welcome!", on_enter=lambda npc, loop: open_shop(loop))
```

### Registering NPCs for Spawning

Edit `dungeon_generation/spawning/interact_init.py`:

```python
from interactable_implementation import Merchant

InteractableSpawns.append(
    InteractableSpawnParams(Merchant(), minFloor=1, maxFloor=3, branch="Hub")
)
```

### Quest Types

| Quest Type | Description |
|------------|-------------|
| `KillCountQuest` | Kill X monsters (optionally specific type) |
| `ItemCollectionQuest` | Collect items with specific trait |
| `ExplorationQuest` | Reach a dungeon depth |

---

## Status Effect System

### Overview

Status effects modify entity behavior and stats temporarily. Located in `spell_system/status_effects/`.

### Architecture

All effects inherit from `StatusEffect` base class with these core methods:

```python
class StatusEffect:
    def apply_effect(self, target):
        """Called when effect is first added. Setup code here."""
        pass

    def tick(self, target):
        """Called each turn. Decrements duration, triggers per-turn effects."""
        self.duration -= 1
        if self.duration <= 0:
            self.active = False

    def remove(self, target):
        """Called when effect expires. Cleanup code here."""
        pass

    def change_duration(self, change):
        """Modifies duration by change amount."""
        self.duration += change
```

### Creating a Custom Status Effect

```python
# spell_system/status_effects/regeneration.py
from spell_system.status_effects.base import StatusEffect

class Regeneration(StatusEffect):
    def __init__(self, duration=10, heal_per_tick=2):
        super().__init__(name="Regeneration", duration=duration)
        self.heal_per_tick = heal_per_tick
        self.cumulative = False  # Duration resets on reapply

    def apply_effect(self, target):
        # Optional: Visual or message on apply
        pass

    def tick(self, target):
        # Heal each turn
        target.character.change_health(self.heal_per_tick)
        super().tick(target)  # Handles duration decrement

    def remove(self, target):
        # Cleanup if needed
        pass
```

### Stacking & Duration Behavior

Effects have two stacking modes controlled by the `cumulative` property:

**Non-cumulative (default):** When applied again, duration **resets** to new effect's duration.
```python
# Example: Burn for 3 turns, apply again → still 3 turns total
self.cumulative = False
```

**Cumulative:** Duration is **extended** by the new effect's duration.
```python
# Example: Slow for 3 turns, apply again → now 6 turns
self.cumulative = True
```

The stacking logic in `status.py`:
```python
if existing_effect.is_cumulative():
    existing_effect.change_duration(new_effect.get_duration())  # Extend
else:
    existing_effect.change_duration(new_effect.get_duration() - existing_effect.get_duration())  # Reset
```

### Immunity System

Entities can be immune to specific effects:

```python
# Make entity immune to poison
entity.character.status.status_effects_immunity.append("Poison")

# Check immunity before applying
if effect.name not in self.status_effects_immunity:
    self.add_status_effect(effect)
```

### Effect Factory

Use `StatusEffectFactory` to create effects by name:

```python
from spell_system.status_effects.status_factory import StatusEffectFactory

# Create effect by name
burn = StatusEffectFactory.create("burn", duration=3, damage=2)
slow = StatusEffectFactory.create("slow", duration=5)

# Returns None if unknown
unknown = StatusEffectFactory.create("nonexistent")  # None
```

### Built-in Effect Types

| Effect | Type | Mechanics |
|--------|------|-----------|
| `Burn` | DoT | Per-tick fire damage |
| `Poison` | DoT | Per-tick poison damage |
| `Slow` | Debuff | +50% action costs; restores on removal |
| `Haste` | Buff | -50% action costs |
| `Weak` | Debuff | Reduces damage multiplier |
| `Berserk` | Buff | +20% max HP, +33% STR, +base damage; applies Slow on removal |
| `Charm` | Control | Swaps AI to friendly; restores on removal |
| `Root` | Control | Disables movement |
| `Stun` | Control | Disables all actions |
| `Sleep` | Control | Disables actions; breaks on damage |
| `Fear` | Control | Reverses movement direction |
| `Invincible` | Special | Sets invincible flag true |

### Special Duration

Use `INFINITE_DURATION` for permanent effects:

```python
from src.core.constants import INFINITE_DURATION

permanent_buff = MyEffect(duration=INFINITE_DURATION)
# Effect never expires naturally
```

---

## Combat System

### Overview

Combat calculations are handled in `character_implementation/fighter.py`. The system uses accuracy vs evasion for hit chance and flat armor reduction for defense.

### Damage Formula

```python
# Step 1: Calculate hit chance
dodge_percentage = defender.get_dodge_chance() - attacker.get_physical_hit_chance()
damage_shave = 1 - (max(min(dodge_percentage, 100), 0) / 100)

if damage_shave == 0:
    return 0  # Miss!

# Step 2: Calculate base damage
weapon_damage = random.randint(weapon.min_damage, weapon.max_damage)
damage = weapon_damage * attacker.physical_damage_multiplier

# Step 3: Apply defense
defense = defender_armor - attacker.armor_piercing
final_damage = max(0, int(damage * damage_shave) - defense)
```

### Hit Chance System

Based on Dexterity stat:

```python
# Attacker
accuracy = attacker.dexterity
physical_hit_chance = accuracy  # Can be modified by equipment

# Defender
evasion = defender.dexterity
dodge_chance = evasion  # Can be modified by equipment

# Effective hit rate
hit_modifier = accuracy - evasion
# Clamped to 0-100%, affects damage_shave multiplier
```

### Physical Damage Multiplier

Scales with Strength:

```python
physical_damage_multiplier = 1 + (strength * 0.01)
# STR 10 → 1.10x damage (10% bonus)
# STR 25 → 1.25x damage (25% bonus)
# STR 50 → 1.50x damage (50% bonus)
```

### Armor System

Flat damage reduction:

```python
effective_armor = defender.armor - attacker.armor_piercing
damage_after_armor = max(0, damage - effective_armor)
```

### Weapon On-Hit Effects

Weapons can trigger effects on hit:

```python
class VampiricSword(Weapon):
    def __init__(self):
        super().__init__(name="Vampiric Sword", min_damage=4, max_damage=8)
        self.on_hit_effects = [self.lifesteal]

    def lifesteal(self, target, attacker, damage, loop):
        """Triggered via do_on_damage_effect() when damage > 0"""
        heal = damage // 4
        attacker.character.change_health(heal)
        loop.add_message(f"The sword drains {heal} life!")
```

Two hook points:

| Method | When Called |
|--------|-------------|
| `do_on_hit_effect()` | Any attack that connects (even if blocked) |
| `do_on_damage_effect()` | Only if damage > 0 dealt |

---

## Experience & Leveling

### Overview

Located in `character_implementation/attributes.py` and `player.py`.

### Experience Requirements

Experience to next level uses a scaling formula:

```python
# Initial
experience_to_next_level = 20

# After each level up
experience_to_next_level += 20 + (experience_to_next_level // 4)
```

Resulting progression:
| Level | XP Required | Cumulative |
|-------|-------------|------------|
| 2 | 20 | 20 |
| 3 | 25 | 45 |
| 4 | 31 | 76 |
| 5 | 39 | 115 |
| 6 | 49 | 164 |

### Level Up Rewards

Automatic bonuses per level:
- **+5 Max Health**
- **+3 Max Mana**
- **+2 Stat Points** (player allocates)

### Stat Point Allocation

Players distribute points in the levelup screen:

```python
# In levelup state
stat_decisions = [str_points, dex_points, end_points, int_points]

# Applied via
player.character.level_up_stats(str_inc, dex_inc, end_inc, int_inc)
```

### Attribute Scaling

Each stat provides specific bonuses:

**Strength:**
- Physical damage multiplier: `1 + (STR * 0.01)`

**Dexterity:**
- Accuracy (hit chance): `DEX`
- Evasion (dodge chance): `DEX`

**Endurance:**
- Max health: `END * 3 + level * 5`
- Health regen: `END * 0.01 + 0.2` per turn

**Intelligence:**
- Max mana: `INT * 2 + level * 3`
- Mana regen: `INT * 0.01 + 0.2` per turn
- Magical resistance: `INT`
- Magical power: `INT`
- Spell damage bonus: `(INT * 1.5) // 2`
- Spell duration bonus: `INT // 3`

### Spell Scaling

Spells can scale with Intelligence:

```python
class Fireball(Spell):
    def activate(self, target, loop):
        base_damage = 10
        bonus = self.parent.character.skill_damage_increase()
        total_damage = base_damage + bonus

        duration_bonus = self.parent.character.skill_duration_increase()
        burn_duration = 3 + duration_bonus
```

---

## Save/Load System

### Overview

Located in `loop_workflow/memory.py`. Uses **dill** library for serialization.

### What Gets Saved

```python
save_data = [
    floor_level,    # Current depth (int)
    generators,     # Dict[branch][depth] → DungeonGenerator
    player,         # Full player state
    branch,         # Current branch name (str)
    keyboard        # Input state
]
```

The `DungeonGenerator` contains:
- `tile_map` - Terrain data
- `monster_map` - All monsters and positions
- `item_map` - All items and positions
- `interact_map` - NPCs, stairs, etc.

### Save/Load API

```python
from loop_workflow.memory import Memory

# Save game
memory = Memory()
memory.update_memory(floor_level, generators, player, branch, keyboard)
memory.save_objects()  # Writes to data.dill

# Load game
memory.load_objects()  # Reads from data.dill
generator = memory.get_current_saved_floor()
player = memory.player
```

### Save Triggers

Saves occur automatically:
- Before floor transitions (stairs up/down)
- Manual save via keybind (if implemented)

### Load Process in Loops

```python
def load_game(self):
    self.memory.load_objects()
    self.generator = self.memory.get_current_saved_floor()
    self.player = self.memory.player
    self.player.character.energy = 0  # Reset energy
    self.change_loop(LoopType.action)
```

---

## Event System

### Overview

A pub/sub event system located in `src/core/events.py`. Enables decoupled communication between game systems.

### Available Events

```python
class GameEvent(Enum):
    # Combat
    DAMAGE_DEALT = "damage_dealt"
    MONSTER_DEATH = "monster_death"
    PLAYER_DEATH = "player_death"

    # Items
    ITEM_PICKED_UP = "item_picked_up"
    ITEM_DROPPED = "item_dropped"
    ITEM_USED = "item_used"
    ITEM_EQUIPPED = "item_equipped"
    ITEM_UNEQUIPPED = "item_unequipped"

    # Player
    LEVEL_UP = "level_up"
    EXPERIENCE_GAINED = "experience_gained"
    HEALTH_CHANGED = "health_changed"
    MANA_CHANGED = "mana_changed"

    # Spells
    SPELL_CAST = "spell_cast"
    SPELL_LEARNED = "spell_learned"

    # World
    FLOOR_CHANGED = "floor_changed"
    DOOR_OPENED = "door_opened"
    TRAP_TRIGGERED = "trap_triggered"

    # Status
    STATUS_APPLIED = "status_applied"
    STATUS_REMOVED = "status_removed"
    STATUS_TICK = "status_tick"

    # Quests
    QUEST_RECEIVED = "quest_received"
    QUEST_UPDATED = "quest_updated"
    QUEST_COMPLETED = "quest_completed"

    # UI
    MESSAGE_ADDED = "message_added"
    TARGET_CHANGED = "target_changed"
```

### Usage

**Subscribe to events:**
```python
from src.core.events import EventBus, GameEvent

def on_monster_death(data):
    monster = data['monster']
    killer = data['killer']
    print(f"{monster.name} was slain by {killer.name}!")

EventBus.subscribe(GameEvent.MONSTER_DEATH, on_monster_death)
```

**Emit events:**
```python
EventBus.emit(GameEvent.MONSTER_DEATH, {
    'monster': dead_monster,
    'killer': player,
    'damage': final_blow_damage
})
```

**Using decorators:**
```python
from src.core.events import on_level_up

@on_level_up
def handle_level_up(data):
    player = data['player']
    new_level = data['level']
    # Trigger achievement check, etc.
```

**Unsubscribe:**
```python
EventBus.unsubscribe(GameEvent.MONSTER_DEATH, on_monster_death)
```

### Example: Achievement System

```python
class AchievementTracker:
    def __init__(self):
        self.kills = 0
        EventBus.subscribe(GameEvent.MONSTER_DEATH, self.on_kill)

    def on_kill(self, data):
        self.kills += 1
        if self.kills == 100:
            self.unlock_achievement("Century Slayer")
```

---

## Game Time & Turns

### Overview

The game uses an energy-based turn system. Actions cost energy; when energy goes negative, time passes.

### Energy System Flow

```
1. Player takes action (move, attack, etc.)
2. Action deducts energy (typically 100)
3. If player.energy < 0:
   a. time_passes() is called
   b. Status effects tick
   c. Cooldowns decrement
   d. Regeneration applies
   e. monster_loop() gives monsters energy
   f. Monsters with energy >= 0 take actions
4. Loop continues
```

### Action Costs

Default costs defined in `character.py`:

```python
action_costs = {
    "attack": 100,
    "move": 100,
    "grab": 30,      # Pick up item
    "equip": 100,
    "unequip": 50,
    "quaff": 10,     # Drink potion
    "read": 20,      # Read scroll
    "drop": 10,
    "activate": 25   # Use item ability
}
```

Entities can have modified costs:
```python
# Fast monster
self.character.action_costs["move"] = 50  # Moves twice as often
```

### Time Passage Effects

Each "turn" (100 energy worth):

1. **Status effect ticks** - Duration decrements, DoT applies
2. **Spell cooldowns** - All cooldowns decrement by 1
3. **Regeneration** - Health and mana regen based on stats
4. **Terrain effects** - Standing in fire, water, etc.

### Regeneration System

Per-turn regeneration based on stats:

```python
# In character.tick_regen()
health_regen = endurance * 0.01 + 0.2
mana_regen = intelligence * 0.01 + 0.2
```

| Stat Value | Regen Per Turn |
|------------|----------------|
| 10 | 0.30 |
| 20 | 0.40 |
| 30 | 0.50 |
| 50 | 0.70 |

**Note:** Some branches (e.g., Forest) disable natural regeneration.

### Special Branch Mechanics

**Day/Night Cycle (Forest):**
```python
# Every 50 turns
if turn_count % 50 == 0:
    is_night = not is_night
    for monster in monsters:
        monster.nightify() if is_night else monster.dayify()
```

**Ocean Tides:**
```python
# Each turn, tide_level oscillates 0-50
# Affects which tiles are underwater vs dry
```

---

## Configuration & Constants

### Player Configuration

Located in `src/core/player_config.py`:

```python
# Starting stats
STARTING_HEALTH = 25
STARTING_MANA = 10

# Progression
MAX_LEVEL = 20
DEBUG_STARTING_STAT_POINTS = 2

# Debug mode
DEBUG_MODE = False  # Enables invincibility, debug spells
```

### Game Constants

Located in `src/core/constants.py`:

```python
# Render tag ranges
TILE_RANGE = (0, 99)
ITEM_RANGE = (100, 999)
MONSTER_RANGE = (1000, 1999)
NPC_RANGE = (2000, 2999)

# Special values
INFINITE_DURATION = -100

# Game timing
class GameTime:
    ENERGY_PER_TURN = 100

# Dungeon generation
MIN_ROOM_SIZE = 4
MAX_ROOM_SIZE = 12
MIN_ROOMS = 5
MAX_ROOMS = 15

# Colors (RGB tuples)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (220, 20, 60)
COLOR_GREEN = (50, 205, 50)
COLOR_BLUE = (30, 144, 255)
COLOR_GOLD = (255, 215, 0)
```

### Modifying Action Costs

Per-entity customization:

```python
class QuickMonster(Monster):
    def __init__(self):
        super().__init__()
        # This monster moves 50% faster
        self.character.action_costs["move"] = 50
        # But attacks slower
        self.character.action_costs["attack"] = 150
```

---

## Common Patterns

### Getting Player Reference

```python
player = loop.player
```

### Getting Current Floor Data

```python
generator = loop.generator
tile_map = generator.tile_map
monster_map = generator.monster_map
item_map = generator.item_map
```

### Adding Messages to Log

```python
loop.add_message("Something happened!")
loop.add_message("Damage dealt!", (220, 20, 60))  # With color
```

### Checking Passability

```python
if loop.generator.get_passable((x, y)):
    # Tile is walkable and unoccupied
```

### Getting Distance

```python
distance = entity.get_distance(target_x, target_y)
```

### Spawning Entities

```python
# Monsters
loop.generator.monster_map.place_thing(monster)

# Items
loop.generator.item_map.place_thing(item)

# Interactables
loop.generator.interact_map.place_thing(interactable)
```

### Working with Status Effects

```python
# Add effect
entity.character.status.add_status_effect(effect)

# Check for effect
effects = entity.character.get_status_effects()

# Remove effect
entity.character.status.remove_status_effect(effect)

# Check specific effect
has_burn = any(e.name == "Burn" for e in effects)
```

### Movement Validation

```python
from src.core.movement import MovementValidator

result = MovementValidator.can_move_to(entity, target_x, target_y)
if result.valid:
    entity.move_to(target_x, target_y)
else:
    loop.add_message(f"Cannot move: {result.reason}")
```

### Learning Spells

```python
from spell_system import give_spell

# Give player a spell by ID
give_spell(player, 'fireball')

# Or directly
from spell_system.fire_school.fireball import Fireball
player.mage.known_spells.append(Fireball(player))
```

---

## Testing

### Test Infrastructure

Located in `test_refactoring.py`. Uses unittest framework.

### Running Tests

```bash
# Run all tests
python test_refactoring.py

# With pytest (verbose)
pytest test_refactoring.py -v

# Run specific test
pytest test_refactoring.py::TestLogging -v
```

### Test Coverage

Current test modules:
- Logging configuration
- Map/entity tracking
- Room generation algorithms

### Writing New Tests

```python
import unittest

class TestMyFeature(unittest.TestCase):
    def setUp(self):
        """Called before each test"""
        self.loop = create_test_loop()
        self.player = self.loop.player

    def test_damage_calculation(self):
        """Test basic damage formula"""
        monster = create_test_monster(health=100)
        damage = self.player.fighter.do_attack(monster, self.loop)
        self.assertGreater(damage, 0)

    def tearDown(self):
        """Called after each test"""
        pass

if __name__ == '__main__':
    unittest.main()
```

---

## Debugging Tips

1. **Enable logging**: Check `logging_config.py` for log levels
2. **Invincibility mode**: Set `DEBUG_MODE = True` in `src/core/player_config.py`
3. **Force spawn monsters**: Set `forceSpawn` in `monster_spawner.py`
4. **Debug spells**: Debug spells auto-added when `DEBUG_MODE = True`
5. **Skip to floor**: Use debug commands or modify `floor_level` on load

### Common Debug Techniques

```python
# Add debug message with color
loop.add_message(f"DEBUG: {variable}", (255, 255, 0))

# Print monster positions
for monster in loop.generator.monster_map.get_all():
    print(f"{monster.name} at ({monster.x}, {monster.y})")

# Check player status
print(f"HP: {player.character.get_health()}/{player.character.get_max_health()}")
print(f"Effects: {[e.name for e in player.character.get_status_effects()]}")
```

---

## Updating This Guide

**Important**: When you make changes to the codebase, please update this documentation:

- New systems → Add new section
- New patterns → Add to Common Patterns
- Changed APIs → Update examples
- New file types → Update File Structure Reference

This keeps the guide accurate for future developers.
