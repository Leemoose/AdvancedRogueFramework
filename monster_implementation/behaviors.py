"""
Behavior-based Monster AI System

Replaces the legacy Monster_AI class hierarchy with composable Behavior objects.
Each behavior encapsulates both ranking logic and execution in a single class.

Usage:
    monster.brain = MonsterAI(monster, [
        CombatBehavior(tendency=(80, 10)),
        MoveBehavior(tendency=(40, 20)),
        WaitBehavior(),
    ])
"""

from logging_config import get_logger
from navigation_utility import pathfinding
import random

logger = get_logger(__name__)


class Behavior:
    """Base class for monster behaviors. Each behavior can rank itself and execute."""

    def __init__(self, name, tendency=(50, 10)):
        self.name = name
        self.avg, self.spread = tendency

    def rank(self, monster, loop) -> int:
        """Return utility score (1-100), or -1 if action is invalid."""
        raise NotImplementedError

    def execute(self, monster, loop):
        """Perform the action."""
        raise NotImplementedError

    def randomize(self) -> int:
        """Return randomized score based on tendency."""
        return max(-1, random.randint(self.avg - self.spread, self.avg + self.spread))

    def set_tendency(self, avg, spread):
        """Update tendency values."""
        self.avg, self.spread = avg, spread


class MonsterAI:
    """Behavior-based AI that selects and executes the highest-ranked behavior."""

    def __init__(self, monster, behaviors: list):
        self.parent = monster
        self.behaviors = behaviors
        self.target = None
        self.grouped = False
        self.stairs_location = None
        self.move_path = []
        # For backwards compatibility with kobold ungroup
        self._behavior_map = {b.name: b for b in behaviors}

    def rank_actions(self, loop):
        """Evaluate all behaviors and execute the best one."""
        logger.debug("Monster %s ranking actions (energy: %s)", self.parent, self.parent.character.energy)

        best_score, best_behavior = 0, None
        for b in self.behaviors:
            score = b.rank(self, loop)
            if score > best_score:
                best_score, best_behavior = score, b

        self.parent.character.energy -= 1

        if best_behavior and best_score > 0:
            logger.info("%s doing %s (utility %d)", self.parent, best_behavior.name, best_score)
            best_behavior.execute(self, loop)
        else:
            logger.debug("%s has no valid action", self.parent)

    def get_behavior(self, name):
        """Get behavior by name for dynamic modification."""
        return self._behavior_map.get(name)

    # Legacy compatibility methods
    def set_tendency(self, name, value):
        if b := self._behavior_map.get(name):
            b.set_tendency(*value)

    def randomize_action(self, name):
        if b := self._behavior_map.get(name):
            return b.randomize()
        return -1


# =============================================================================
# CORE BEHAVIORS (used by most monsters)
# =============================================================================

class CombatBehavior(Behavior):
    """Attack player if in range and visible."""

    def __init__(self, tendency=(80, 10)):
        super().__init__("combat", tendency)

    def rank(self, ai, loop):
        player = loop.player
        monster = ai.parent
        dist = monster.get_distance(player.get_x(), player.get_y())
        in_range = dist <= monster.fighter.get_range()
        visible = loop.generator.tile_map.get_visible(monster.get_x(), monster.get_y())

        if in_range and visible:
            ai.target = player
            return self.randomize()
        ai.target = None
        return -1

    def execute(self, ai, loop):
        monster = ai.parent
        if not monster.character.can_take_action():
            monster.character.energy -= monster.character.action_costs["move"]
            loop.add_message(f"{monster} is petrified and cannot attack.")
            return

        if ai.target:
            damage = monster.do_attack(ai.target, loop)
            loop.add_message(f"{monster} attacked {ai.target.name} for {damage} damage")
        else:
            loop.add_message(f"{monster.name} can find no suitable target.")


class MoveBehavior(Behavior):
    """Move toward player using pathfinding."""

    def __init__(self, tendency=(40, 20)):
        super().__init__("move", tendency)

    def rank(self, ai, loop):
        if ai.parent.get_distance(loop.player.get_x(), loop.player.get_y()) > 1.5:
            return self.randomize()
        return -1

    def execute(self, ai, loop):
        monster = ai.parent
        if not monster.character.can_take_action():
            monster.character.energy -= monster.character.action_costs["move"]
            loop.add_message(f"{monster} is petrified and cannot move.")
            return

        tile_map = loop.generator.tile_map
        monster_map = loop.generator.monster_map
        player = loop.player

        start = (ai.target.x, ai.target.y) if ai.target else (monster.x, monster.y)
        end = (player.x, player.y)
        close = player.get_distance(monster.x, monster.y) <= 2.5
        moves = pathfinding.astar(tile_map.get_map(), start, end, monster_map, player, monster_blocks=close)

        if len(moves) > 1:
            try:
                xmove, ymove = moves[1]
                if loop.generator.get_passable((xmove, ymove)):
                    monster.move(xmove - monster.x, ymove - monster.y, loop)
            except Exception as e:
                logger.error("Move error: %s", e)


class WaitBehavior(Behavior):
    """Do nothing."""

    def __init__(self, tendency=(1, 0)):
        super().__init__("wait", tendency)

    def rank(self, ai, loop):
        return self.randomize()

    def execute(self, ai, loop):
        logger.debug("Monster %s waiting", ai.parent)


class FleeBehavior(Behavior):
    """Run away when health is low or flee flag is set."""

    def __init__(self, tendency=(100, 10), threshold=0.25):
        super().__init__("flee", tendency)
        self.threshold = threshold

    def rank(self, ai, loop):
        char = ai.parent.character
        if char.get_flee() or char.get_health() / char.get_max_health() < self.threshold:
            return self.randomize()
        return -1

    def execute(self, ai, loop):
        monster = ai.parent
        if not monster.character.can_take_action():
            monster.character.energy -= monster.character.action_costs["move"]
            loop.add_message(f"{monster} is petrified and cannot move.")
            return

        tile_map = loop.generator.tile_map
        monster_map = loop.generator.monster_map
        player = loop.player

        start, end = (monster.x, monster.y), (player.x, player.y)
        moves = pathfinding.astar(tile_map.get_map(), start, end, monster_map, player)

        if len(moves) > 1:
            xmove, ymove = moves[1]
            opposite = (-xmove + monster.x, -ymove + monster.y)
            ox, oy = opposite

            if tile_map.get_passable(monster.x + ox, monster.y + oy):
                monster.move(ox, oy, loop)
            elif tile_map.get_passable(monster.x, monster.y + oy):
                monster.move(0, oy, loop)
            elif tile_map.get_passable(monster.x + ox, monster.y):
                monster.move(ox, 0, loop)
            else:
                monster.character.energy -= monster.character.action_costs["move"]
                loop.add_message(f"{monster} cowers in a corner.")


# =============================================================================
# ITEM BEHAVIORS (Goblin)
# =============================================================================

class FindItemBehavior(Behavior):
    """Move toward nearest item on the floor."""

    def __init__(self, tendency=(80, 10)):
        super().__init__("find_item", tendency)

    def rank(self, ai, loop):
        if loop.generator.item_map.get_num_entities() > 0:
            return self.randomize()
        return -1

    def execute(self, ai, loop):
        monster = ai.parent
        item_map = loop.generator.item_map

        if item_map.get_num_entities() > 0:
            item = item_map.get_nearest_entity(monster.get_x(), monster.get_y())
            if item:
                moves = pathfinding.astar(
                    loop.generator.tile_map.get_map(),
                    monster.get_location(),
                    item.get_location(),
                    loop.generator.monster_map.entity_map,
                    loop.player
                )
                if len(moves) > 1:
                    xmove, ymove = moves[1]
                    monster.move(xmove - monster.x, ymove - monster.y, loop)


class PickupBehavior(Behavior):
    """Pick up item at current location."""

    def __init__(self, tendency=(100, 5)):
        super().__init__("pickup", tendency)

    def rank(self, ai, loop):
        monster = ai.parent
        if not loop.generator.item_map.get_has_no_entity(monster.x, monster.y):
            return self.randomize()
        return -1

    def execute(self, ai, loop):
        item = loop.generator.item_map.get_entity(ai.parent.get_x(), ai.parent.get_y())
        ai.parent.inventory.do_grab(item, loop)


# =============================================================================
# OOZE BEHAVIOR
# =============================================================================

class OozeMovesBehavior(MoveBehavior):
    """Move and destroy items on the tile."""

    def __init__(self, tendency=(40, 20)):
        super().__init__(tendency)
        self.name = "move"  # Override to keep same name

    def execute(self, ai, loop):
        monster = ai.parent
        if not monster.character.can_take_action():
            monster.character.energy -= monster.character.action_costs["move"]
            loop.add_message(f"{monster} is petrified and cannot move.")
            return

        tile_map = loop.generator.tile_map
        monster_map = loop.generator.monster_map
        player = loop.player

        start = (ai.target.x, ai.target.y) if ai.target else (monster.x, monster.y)
        end = (player.x, player.y)
        close = player.get_distance(monster.x, monster.y) <= 2.5
        moves = pathfinding.astar(tile_map.get_map(), start, end, monster_map, player, monster_blocks=close)

        if len(moves) > 1:
            try:
                xmove, ymove = moves[1]
                if loop.generator.get_passable((xmove, ymove)):
                    monster.move(xmove - monster.x, ymove - monster.y, loop)
                    # Ooze destroys items
                    if loop.generator.item_map.get_has_entity(monster.get_x(), monster.get_y()):
                        item = loop.generator.item_map.get_entity(monster.get_x(), monster.get_y())
                        item.set_destroy(True)
                        loop.add_message(f"{item.name} consumed by {monster.name}")
            except Exception as e:
                logger.error("Ooze move error: %s", e)


# =============================================================================
# ORC BEHAVIOR
# =============================================================================

class BerserkBehavior(Behavior):
    """Activate berserk when health is low (one-time use)."""

    def __init__(self, tendency=(80, 10), threshold=0.25):
        super().__init__("berserk", tendency)
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
        from spell_system.status_effects import Berserk
        ai.parent.character.status.add_status_effect(Berserk(5))
        self.used = True
        loop.add_message(f"{ai.parent.name} goes berserk!")


# =============================================================================
# SPIDER BEHAVIOR
# =============================================================================

class SpinWebBehavior(Behavior):
    """Spin web on current tile (one-time use)."""

    def __init__(self, tendency=(40, 5)):
        super().__init__("spin_web", tendency)
        self.used = False

    def rank(self, ai, loop):
        if self.used:
            return -1
        return self.randomize()

    def execute(self, ai, loop):
        from dungeon_generation.terrain import Web
        x, y = ai.parent.get_location()
        loop.generator.tile_map.get_entity(x, y).add_terrain(Web())
        ai.parent.character.change_energy(-ai.parent.character.action_costs["spin_web"])
        loop.add_message(f"{ai.parent.name} spins a web at {x}, {y}")
        self.used = True


# =============================================================================
# KOBOLD BEHAVIORS
# =============================================================================

class RangedCombatBehavior(Behavior):
    """Attack from range but not melee (for kobolds with spears)."""

    def __init__(self, tendency=(80, 10)):
        super().__init__("combat", tendency)

    def rank(self, ai, loop):
        player = loop.player
        monster = ai.parent
        dist = monster.get_distance(player.get_x(), player.get_y())
        in_range = dist <= monster.fighter.get_range()
        not_melee = dist > 1.5
        visible = loop.generator.get_visible(monster.get_x(), monster.get_y())

        if in_range and not_melee and visible:
            ai.target = player
            return self.randomize()
        ai.target = None
        return -1

    def execute(self, ai, loop):
        monster = ai.parent
        if not monster.character.can_take_action():
            monster.character.energy -= monster.character.action_costs["move"]
            loop.add_message(f"{monster} is petrified and cannot attack.")
            return

        if ai.target:
            damage = monster.do_attack(ai.target, loop)
            loop.add_message(f"{monster} attacked {ai.target.name} for {damage} damage")


class BurningHandsBehavior(Behavior):
    """Cast burning hands spell when in melee and have mana."""

    def __init__(self, tendency=(10, 0)):
        super().__init__("burning_hands", tendency)

    def rank(self, ai, loop):
        monster = ai.parent
        has_mana = monster.character.get_mana() > 5
        in_melee = monster.get_distance(loop.player.get_x(), loop.player.get_y()) < 1.5

        if has_mana and in_melee:
            return self.randomize()
        return -1

    def execute(self, ai, loop):
        monster = ai.parent
        if monster.body.get_weapon() is not None:
            monster.inventory.do_drop(monster.body.get_weapon(), loop.generator.item_map)
        monster.mage.cast_spell(0, loop.player, loop)


class RepositionBehavior(Behavior):
    """Move to maintain range from player (kobold tactical positioning)."""

    def __init__(self, tendency=(100, 15)):
        super().__init__("reposition", tendency)

    def rank(self, ai, loop):
        monster = ai.parent
        player = loop.player

        if monster.get_distance(player.get_x(), player.get_y()) >= 1.5:
            return -1

        diffx = monster.get_x() - player.get_x()
        diffy = monster.get_y() - player.get_y()

        # Check if any valid reposition exists
        if abs(diffx) + abs(diffy) == 1:
            for x in range(-abs(diffy), abs(diffy) * 2):
                if loop.generator.get_passable((x + monster.get_x(), monster.get_y() + diffy)):
                    return self.randomize()
            for y in range(-abs(diffx), abs(diffx) * 2):
                if loop.generator.get_passable((diffx + monster.get_x(), y + monster.get_y())):
                    return self.randomize()
        elif abs(diffx) + abs(diffy) == 2 and abs(diffx) == abs(diffy):
            positions = [
                (diffx + monster.get_x(), diffy + monster.get_y()),
                (diffx + monster.get_x(), (diffy + diffx) + monster.get_y()),
                ((diffx + diffy) + monster.get_x(), diffy + monster.get_y()),
                (monster.get_x() + diffx, monster.get_y() - diffy),
                (monster.get_x() - diffx, monster.get_y() + diffy),
            ]
            for pos in positions:
                if loop.generator.get_passable(pos):
                    return self.randomize()
        return -1

    def execute(self, ai, loop):
        monster = ai.parent
        player = loop.player

        if monster.get_distance(player.get_x(), player.get_y()) >= 1.5:
            return

        diffx = monster.get_x() - player.get_x()
        diffy = monster.get_y() - player.get_y()
        options = []

        if abs(diffx) + abs(diffy) == 1:
            for x in range(-abs(diffy), abs(diffy) * 2):
                if loop.generator.get_passable((x + monster.get_x(), monster.get_y() + diffy)):
                    options.append((x, diffy))
            for y in range(-abs(diffx), abs(diffx) * 2):
                if loop.generator.get_passable((diffx + monster.get_x(), y + monster.get_y())):
                    options.append((diffx, y))
        elif abs(diffx) + abs(diffy) == 2 and abs(diffx) == abs(diffy):
            checks = [
                ((diffx + monster.get_x(), diffy + monster.get_y()), (diffx, diffy)),
                ((diffx + monster.get_x(), (diffy + diffx) + monster.get_y()), (diffx, diffy + diffx)),
                (((diffx + diffy) + monster.get_x(), diffy + monster.get_y()), (diffx + diffy, diffy)),
                ((monster.get_x() + diffx, monster.get_y() - diffy), (diffx, -diffy)),
                ((monster.get_x() - diffx, monster.get_y() + diffy), (-diffx, diffy)),
            ]
            for pos, move in checks:
                if loop.generator.get_passable(pos):
                    options.append(move)

        if options:
            move = random.choice(options)
            monster.move(move[0], move[1], loop)


# =============================================================================
# FACTORY FUNCTIONS - Create standard behavior sets for each monster type
# =============================================================================

def create_base_behaviors():
    """Standard combat/move/wait behaviors."""
    return [CombatBehavior(), MoveBehavior(), WaitBehavior()]


def create_ooze_behaviors():
    """Ooze: combat + destructive movement."""
    return [CombatBehavior(), OozeMovesBehavior(), WaitBehavior()]


def create_goblin_behaviors():
    """Goblin: combat + item hoarding + flee."""
    return [
        CombatBehavior(),
        MoveBehavior(),
        FindItemBehavior(),
        PickupBehavior(),
        FleeBehavior(),
        WaitBehavior(),
    ]


def create_orc_behaviors():
    """Orc: combat + berserk when low health."""
    return [CombatBehavior(), MoveBehavior(), BerserkBehavior(), WaitBehavior()]


def create_spider_behaviors():
    """Spider: combat + web spinning."""
    return [CombatBehavior(), MoveBehavior(), SpinWebBehavior(), WaitBehavior()]


def create_kobold_behaviors():
    """Kobold: ranged combat + reposition + burning hands."""
    return [
        RangedCombatBehavior(),
        MoveBehavior(),
        RepositionBehavior(),
        BurningHandsBehavior(),
        WaitBehavior(),
    ]


def create_skeleton_behaviors():
    """Skeleton: aggressive combat."""
    return [
        CombatBehavior(tendency=(80, 10)),
        MoveBehavior(tendency=(40, 25)),
        WaitBehavior(),
    ]


# =============================================================================
# SLIME BEHAVIOR (different from Ooze - picks up items instead of destroying)
# =============================================================================

class SlimeMoveBehavior(MoveBehavior):
    """Move slowly and pick up items (like old Slime_AI)."""

    def __init__(self, tendency=(30, 10)):
        super().__init__(tendency)
        self.name = "move"


def create_slime_behaviors():
    """Slime: slow movement + item hoarding."""
    return [
        CombatBehavior(tendency=(60, 10)),
        SlimeMoveBehavior(),
        FindItemBehavior(tendency=(70, 10)),
        PickupBehavior(),
        WaitBehavior(),
    ]


# =============================================================================
# GARGOYLE BEHAVIOR (petrify gaze)
# =============================================================================

class PetrifyGazeBehavior(Behavior):
    """Cast petrify spell when in range and have mana."""

    def __init__(self, tendency=(70, 10), activation_chance=0.3):
        super().__init__("petrify_gaze", tendency)
        self.activation_chance = activation_chance

    def rank(self, ai, loop):
        monster = ai.parent
        player = loop.player
        has_mana = monster.character.get_mana() >= 5
        in_range = monster.get_distance(player.get_x(), player.get_y()) <= 4
        visible = loop.generator.get_visible(monster.get_x(), monster.get_y())

        # Random activation chance
        if has_mana and in_range and visible and random.random() < self.activation_chance:
            return self.randomize()
        return -1

    def execute(self, ai, loop):
        monster = ai.parent
        if monster.mage.known_spells:
            monster.mage.cast_spell(0, loop.player, loop)
            loop.add_message(f"{monster.name}'s eyes flash with a petrifying gaze!")


def create_gargoyle_behaviors():
    """Gargoyle: petrify gaze + combat."""
    return [
        PetrifyGazeBehavior(),
        CombatBehavior(tendency=(70, 10)),
        MoveBehavior(tendency=(40, 15)),
        WaitBehavior(),
    ]


# =============================================================================
# MINOTAUR BEHAVIOR (shrug off CC)
# =============================================================================

class ShrugOffBehavior(Behavior):
    """Attempt to shrug off status effects when stunned/rooted."""

    def __init__(self, tendency=(90, 5), success_chance=0.75):
        super().__init__("shrug_off", tendency)
        self.success_chance = success_chance

    def rank(self, ai, loop):
        monster = ai.parent
        # Check if monster has any disabling status effects
        if not monster.character.can_take_action():
            return self.randomize()
        return -1

    def execute(self, ai, loop):
        monster = ai.parent
        if random.random() < self.success_chance:
            # Clear stun/root effects
            monster.character.status.clear_disabling_effects()
            loop.add_message(f"{monster.name} shrugs off the effect!")
        else:
            monster.character.energy -= monster.character.action_costs["move"]
            loop.add_message(f"{monster.name} struggles against the effect.")


def create_minotaur_behaviors():
    """Minotaur: shrug off CC + aggressive combat."""
    return [
        ShrugOffBehavior(),
        CombatBehavior(tendency=(85, 10)),
        MoveBehavior(tendency=(50, 15)),
        WaitBehavior(),
    ]


# =============================================================================
# HOBGOBLIN BEHAVIOR (blink strike)
# =============================================================================

class BlinkStrikeBehavior(Behavior):
    """Use blink strike to teleport to and attack target."""

    def __init__(self, tendency=(75, 10)):
        super().__init__("blink_strike", tendency)

    def rank(self, ai, loop):
        monster = ai.parent
        player = loop.player
        has_mana = monster.character.get_mana() >= 3
        dist = monster.get_distance(player.get_x(), player.get_y())
        in_range = 1.5 < dist <= 5  # Not in melee, but within blink range
        visible = loop.generator.get_visible(monster.get_x(), monster.get_y())
        spell_ready = monster.mage.known_spells and monster.mage.known_spells[0].ready == 0

        if has_mana and in_range and visible and spell_ready:
            return self.randomize()
        return -1

    def execute(self, ai, loop):
        monster = ai.parent
        monster.mage.cast_spell(0, loop.player, loop)


def create_hobgoblin_behaviors():
    """Hobgoblin: blink strike + combat + flee."""
    return [
        BlinkStrikeBehavior(),
        CombatBehavior(tendency=(75, 10)),
        MoveBehavior(tendency=(45, 15)),
        FleeBehavior(threshold=0.3),
        WaitBehavior(),
    ]


# =============================================================================
# LOOTER BEHAVIOR (fast item grabbing)
# =============================================================================

def create_looter_behaviors():
    """Looter: prioritizes items over combat, very fast grabbing."""
    return [
        FindItemBehavior(tendency=(90, 5)),
        PickupBehavior(tendency=(100, 0)),
        CombatBehavior(tendency=(50, 10)),
        MoveBehavior(tendency=(40, 15)),
        FleeBehavior(threshold=0.2),
        WaitBehavior(),
    ]


# =============================================================================
# GOBLIN SHAMAN BEHAVIOR (summons goblins)
# =============================================================================

class SummonBehavior(Behavior):
    """Summon creatures when conditions are met."""

    def __init__(self, tendency=(60, 10), summon_type='goblin'):
        super().__init__("summon", tendency)
        self.summon_type = summon_type

    def rank(self, ai, loop):
        monster = ai.parent
        has_mana = monster.character.get_mana() >= 5
        spell_ready = monster.mage.known_spells and monster.mage.known_spells[0].ready == 0

        if has_mana and spell_ready:
            return self.randomize()
        return -1

    def execute(self, ai, loop):
        monster = ai.parent
        monster.mage.cast_spell(0, loop.player, loop)
        loop.add_message(f"{monster.name} summons a {self.summon_type}!")


def create_goblin_shaman_behaviors():
    """Goblin Shaman: summons goblins + flee."""
    return [
        SummonBehavior(summon_type='goblin'),
        CombatBehavior(tendency=(40, 10)),
        MoveBehavior(tendency=(50, 15)),
        FleeBehavior(threshold=0.4),
        WaitBehavior(),
    ]


# =============================================================================
# TORMENTORB BEHAVIOR (torment spell)
# =============================================================================

class TormentBehavior(Behavior):
    """Cast torment spell at range."""

    def __init__(self, tendency=(80, 10)):
        super().__init__("torment", tendency)

    def rank(self, ai, loop):
        monster = ai.parent
        player = loop.player
        has_mana = monster.character.get_mana() >= 5
        in_range = monster.get_distance(player.get_x(), player.get_y()) <= 5
        visible = loop.generator.get_visible(monster.get_x(), monster.get_y())
        spell_ready = monster.mage.known_spells and monster.mage.known_spells[0].ready == 0

        if has_mana and in_range and visible and spell_ready:
            return self.randomize()
        return -1

    def execute(self, ai, loop):
        monster = ai.parent
        monster.mage.cast_spell(0, loop.player, loop)


def create_tormentorb_behaviors():
    """Tormentorb: torment spell + slow combat."""
    return [
        TormentBehavior(),
        CombatBehavior(tendency=(60, 10)),
        MoveBehavior(tendency=(30, 10)),
        WaitBehavior(),
    ]


# =============================================================================
# DUMMY BEHAVIOR (does nothing)
# =============================================================================

class DummyBehavior(Behavior):
    """Training dummy - doesn't attack or move."""

    def __init__(self, tendency=(100, 0)):
        super().__init__("dummy", tendency)

    def rank(self, ai, loop):
        return self.randomize()

    def execute(self, ai, loop):
        # Do nothing - just stand there
        pass


def create_dummy_behaviors():
    """Dummy: does nothing."""
    return [DummyBehavior()]


# =============================================================================
# FOREST MONSTER BEHAVIORS
# =============================================================================

class StumpyBehavior(Behavior):
    """Stumpy waits until player is close, then attacks."""

    def __init__(self, tendency=(70, 10)):
        super().__init__("ambush", tendency)

    def rank(self, ai, loop):
        monster = ai.parent
        player = loop.player
        dist = monster.get_distance(player.get_x(), player.get_y())

        # Only become aggressive when player is close
        if dist <= 3:
            return self.randomize()
        return -1

    def execute(self, ai, loop):
        # Just sets up for combat on next turn
        ai.target = loop.player


def create_stumpy_behaviors():
    """Stumpy: ambush predator, waits until close."""
    return [
        StumpyBehavior(),
        CombatBehavior(tendency=(80, 10)),
        MoveBehavior(tendency=(30, 10)),
        WaitBehavior(tendency=(50, 10)),
    ]


def create_treant_behaviors():
    """Treant: slow but powerful, root on hit handled by weapon."""
    return [
        CombatBehavior(tendency=(85, 10)),
        MoveBehavior(tendency=(25, 10)),
        WaitBehavior(),
    ]


# =============================================================================
# METALLIC BEAR BEHAVIOR (fury when low health)
# =============================================================================

class FuryBehavior(Behavior):
    """Enter fury mode when health is low - massive damage boost."""

    def __init__(self, tendency=(95, 5), threshold=0.25):
        super().__init__("fury", tendency)
        self.threshold = threshold
        self.activated = False

    def rank(self, ai, loop):
        if self.activated:
            return -1
        char = ai.parent.character
        if char.get_health() / char.get_max_health() < self.threshold:
            return self.randomize()
        return -1

    def execute(self, ai, loop):
        from spell_system.status_effects import Berserk, Haste
        monster = ai.parent
        # Apply both berserk and haste for fury mode
        monster.character.status.add_status_effect(Berserk(10))
        monster.character.status.add_status_effect(Haste(10, 50))
        self.activated = True
        loop.add_message(f"{monster.name} enters a terrifying fury!")


def create_metallic_bear_behaviors():
    """Metallic Bear: fury mode when low health."""
    return [
        FuryBehavior(),
        CombatBehavior(tendency=(85, 10)),
        MoveBehavior(tendency=(45, 15)),
        WaitBehavior(),
    ]


# =============================================================================
# INSECT NEST BEHAVIOR (summon when damaged)
# =============================================================================

class NestDefenseBehavior(Behavior):
    """Immobile nest that spawns hornets when damaged."""

    def __init__(self, tendency=(100, 0)):
        super().__init__("nest_defense", tendency)
        self.last_health = None

    def rank(self, ai, loop):
        # Always returns this behavior since nest can't do anything else
        return self.randomize()

    def execute(self, ai, loop):
        # Nest is immobile, just sits there
        # Spawning is handled by on_damage effect
        pass


def create_insect_nest_behaviors():
    """Insect Nest: immobile, spawns on damage."""
    return [NestDefenseBehavior()]


def create_hornet_behaviors():
    """Hornet: aggressive fast attacker."""
    return [
        CombatBehavior(tendency=(90, 5)),
        MoveBehavior(tendency=(60, 15)),
        WaitBehavior(),
    ]


# =============================================================================
# WATER MONSTER BEHAVIORS
# =============================================================================

def create_water_monster_behaviors():
    """Basic water monster: combat + movement."""
    return [
        CombatBehavior(tendency=(75, 10)),
        MoveBehavior(tendency=(50, 15)),
        WaitBehavior(),
    ]


# =============================================================================
# RAPTOR BEHAVIOR (fast aggressive hunter)
# =============================================================================

def create_raptor_behaviors():
    """Raptor: very aggressive, fast movement."""
    return [
        CombatBehavior(tendency=(90, 5)),
        MoveBehavior(tendency=(70, 15)),
        WaitBehavior(),
    ]


# =============================================================================
# GOLEM BEHAVIOR (very slow but tanky)
# =============================================================================

def create_golem_behaviors():
    """Golem: slow but relentless."""
    return [
        CombatBehavior(tendency=(80, 10)),
        MoveBehavior(tendency=(20, 5)),
        WaitBehavior(tendency=(30, 10)),
    ]
