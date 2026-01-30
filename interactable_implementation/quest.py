"""
Quest System.

Provides a multi-stage quest system with progress tracking and rewards.

Quest stages work by incrementing the `level` attribute. Each level can have
its own description in the `descriptions` dict. When level exceeds the number
of descriptions, the quest is considered complete.

Classes:
    Quest: Base class for all quests
    KillCountQuest: Quest that tracks monster kills
    ItemCollectionQuest: Quest that tracks item collection
    ExplorationQuest: Quest that tracks floor exploration
"""

from logging_config import get_logger

logger = get_logger(__name__)


class Quest:
    """
    Base class for all quests.

    Attributes:
        name: Display name of the quest
        level: Current stage/level of the quest (1-indexed)
        experience_given: XP reward on completion
        descriptions: Dict mapping level -> description text
        active: Whether the quest is still in progress
    """

    def __init__(self, name="Quest", experience_given=10):
        self.name = name
        self.level = 1
        self.experience_given = experience_given
        self.descriptions = {}
        self.active = True
        logger.debug("Created quest: %s", name)

    def get_description(self, loop=None):
        """Get the description for the current quest stage."""
        if self.level in self.descriptions:
            return self.descriptions[self.level]
        return "This quest has been completed."

    def check_for_progress(self, loop):
        """
        Check if the quest should advance to the next stage.

        Called each turn from the game loop. Override in subclasses
        to implement stage progression logic.

        Args:
            loop: The main game loop instance
        """
        pass

    def check_for_completion(self, loop):
        """
        Check if the quest is complete.

        Args:
            loop: The main game loop instance

        Returns:
            bool: True if quest is complete
        """
        return self.level > len(self.descriptions)

    def give_reward(self, loop):
        """
        Give the quest reward to the player.

        Override in subclasses for custom rewards.

        Args:
            loop: The main game loop instance
        """
        loop.player.gain_experience(self.experience_given)
        logger.info("Quest '%s' completed, gave %d XP", self.name, self.experience_given)

    def advance_stage(self, loop, message=None):
        """
        Advance to the next quest stage.

        Args:
            loop: The main game loop instance
            message: Optional message to display
        """
        self.level += 1
        if message:
            loop.add_message(message, (255, 215, 0))  # Gold color
        logger.debug("Quest '%s' advanced to stage %d", self.name, self.level)


class KillCountQuest(Quest):
    """
    Quest that requires killing a certain number of monsters.

    Tracks kills via the player's statistics system.

    Attributes:
        target_count: Number of kills required
        monster_type: Optional specific monster type to track (None = any)
        start_count: Kill count when quest was started
    """

    def __init__(self, name="Slay Quest", target_count=5, monster_type=None, experience_given=20):
        super().__init__(name=name, experience_given=experience_given)
        self.target_count = target_count
        self.monster_type = monster_type
        self.start_count = None  # Set when quest is given

        self.descriptions[1] = f"Kill {target_count} {'monsters' if monster_type is None else monster_type + 's'}."
        self.descriptions[2] = "Return to the quest giver to claim your reward."

    def set_start_count(self, loop):
        """Record the starting kill count when quest begins."""
        if self.monster_type:
            self.start_count = loop.player.statistics.get_monster_kills(self.monster_type)
        else:
            self.start_count = loop.player.statistics.total_monsters_killed()

    def get_current_kills(self, loop):
        """Get the number of kills since quest started."""
        if self.start_count is None:
            return 0
        if self.monster_type:
            current = loop.player.statistics.get_monster_kills(self.monster_type)
        else:
            current = loop.player.statistics.total_monsters_killed()
        return current - self.start_count

    def check_for_progress(self, loop):
        """Check if kill target has been reached."""
        if not self.active or self.level != 1:
            return

        if self.get_current_kills(loop) >= self.target_count:
            self.advance_stage(loop, f"Quest '{self.name}': Kill target reached! Return to claim reward.")

    def get_description(self, loop=None):
        """Get description with current progress."""
        if self.level == 1:
            base = self.descriptions[1]
            if self.start_count is not None and loop is not None:
                current = self.get_current_kills(loop)
                return f"{base} (Progress: {min(current, self.target_count)}/{self.target_count})"
            return base
        return super().get_description()


class ItemCollectionQuest(Quest):
    """
    Quest that requires collecting specific items.

    Attributes:
        item_trait: Trait to look for in items (e.g., "goblin_corpse")
        target_count: Number of items needed
    """

    def __init__(self, name="Collection Quest", item_trait="quest_item", target_count=1, experience_given=15):
        super().__init__(name=name, experience_given=experience_given)
        self.item_trait = item_trait
        self.target_count = target_count

        self.descriptions[1] = f"Collect {target_count} {item_trait.replace('_', ' ')}(s)."
        self.descriptions[2] = "Return to the quest giver with the items."

    def get_item_count(self, loop):
        """Count matching items in player inventory."""
        count = 0
        for item in loop.player.get_inventory():
            if item.has_trait(self.item_trait):
                count += 1
        return count

    def check_for_progress(self, loop):
        """Check if enough items have been collected."""
        if not self.active or self.level != 1:
            return

        if self.get_item_count(loop) >= self.target_count:
            self.advance_stage(loop, f"Quest '{self.name}': Items collected! Return to claim reward.")


class ExplorationQuest(Quest):
    """
    Quest that requires reaching a specific dungeon depth.

    Attributes:
        target_depth: Depth to reach
        target_branch: Optional specific branch (None = any)
    """

    def __init__(self, name="Exploration Quest", target_depth=5, target_branch=None, experience_given=25):
        super().__init__(name=name, experience_given=experience_given)
        self.target_depth = target_depth
        self.target_branch = target_branch

        branch_text = f" of the {target_branch}" if target_branch else ""
        self.descriptions[1] = f"Reach depth {target_depth}{branch_text}."
        self.descriptions[2] = "You have reached the target depth. Return to claim your reward."

    def check_for_progress(self, loop):
        """Check if target depth has been reached."""
        if not self.active or self.level != 1:
            return

        current_depth = loop.get_depth()
        current_branch = loop.get_branch()

        depth_reached = current_depth >= self.target_depth
        branch_matched = self.target_branch is None or current_branch == self.target_branch

        if depth_reached and branch_matched:
            self.advance_stage(loop, f"Quest '{self.name}': Destination reached!")


class GoblinSlayerQuest(KillCountQuest):
    """Pre-configured quest to kill goblins."""

    def __init__(self, target_count=5):
        super().__init__(
            name="Goblin Slayer",
            target_count=target_count,
            monster_type="Goblin",
            experience_given=30
        )
        self.descriptions[1] = f"The goblin menace grows. Slay {target_count} of them and bring proof."
        self.descriptions[2] = "You have slain enough goblins. Return to collect your reward."


class DungeonDelverQuest(ExplorationQuest):
    """Pre-configured quest to explore the dungeon."""

    def __init__(self, target_depth=3):
        super().__init__(
            name="Dungeon Delver",
            target_depth=target_depth,
            target_branch="Dungeon",
            experience_given=40
        )
        self.descriptions[1] = f"Prove your worth by descending to depth {target_depth} of the Dungeon."
        self.descriptions[2] = "You have proven yourself a capable explorer. Return for your reward."
