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
        from spell_implementation.effects.berserk import Berserk
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
