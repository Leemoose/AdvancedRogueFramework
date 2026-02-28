"""
Spell class - represents a spell instance bound to a caster.

Spells are created from SpellData (loaded from YAML) and bound to a specific caster.
The spell handles cooldown tracking and delegates effect execution to the effect system.
"""

from logging_config import get_logger

logger = get_logger(__name__)


class Spell:
    """A spell instance bound to a specific caster."""

    def __init__(self, caster, spell_data):
        """
        Create a spell instance.

        Args:
            caster: The entity that owns this spell
            spell_data: SpellData object containing the spell definition
        """
        self.caster = caster
        self.data = spell_data
        self.ready = 0  # Cooldown tracker, 0 = ready to cast

    # ---- Properties (delegate to spell_data) ----

    @property
    def name(self):
        return self.data.name

    @property
    def id(self):
        return self.data.id

    @property
    def cost(self):
        return self.data.cost

    @property
    def cooldown(self):
        return self.data.cooldown

    @property
    def range(self):
        return self.data.range

    @property
    def action_cost(self):
        return self.data.action_cost

    @property
    def targetted(self):
        return self.data.targeting != "self"

    @property
    def targets_monster(self):
        return self.data.targeting == "enemy"

    @property
    def render_tag(self):
        return self.data.icon

    @property
    def school(self):
        return self.data.school

    # ---- Cooldown management ----

    def tick_cooldown(self):
        """Reduce cooldown by 1 turn."""
        if self.ready > 0:
            self.ready -= 1

    def reset_cooldown(self):
        """Reset cooldown to 0 (e.g., on rest)."""
        self.ready = 0

    def is_ready(self):
        """Check if spell is off cooldown."""
        return self.ready == 0

    # ---- Casting ----

    def castable(self, target=None):
        """
        Check if the spell can be cast.

        Returns True if:
        - Spell is off cooldown
        - Caster has enough mana
        - Target is in range (if targeted spell)
        """
        if not self.is_ready():
            return False

        if self.caster.character.get_mana() < self.cost:
            return False

        if target is not None and self.targetted:
            if not self.in_range(target):
                return False

        return True

    def in_range(self, target):
        """Check if target is within spell range."""
        if self.range == -1:  # Unlimited range
            return True

        if isinstance(target, tuple):
            target_x, target_y = target
        else:
            target_x, target_y = target.get_location()

        distance = self.caster.get_distance(target_x, target_y)
        return distance <= self.range

    def try_to_activate(self, target, loop):
        """
        Attempt to cast the spell.

        Returns True if cast succeeded, False otherwise.
        """
        if not self.castable(target):
            loop.add_message("You were unable to cast the spell.")
            return False

        self.ready = self.cooldown
        logger.info("Spell %s is activated by %s", self.name, self.caster.name)
        return self.activate(target, loop)

    def activate(self, target, loop):
        """
        Execute the spell effects.

        This is where the magic happens - we iterate through all effects
        defined in the spell data and execute them.
        """
        # Deduct mana cost
        self.caster.character.change_mana(-self.cost)

        # Build context for effects
        context = SpellContext(
            caster=self.caster,
            target=target,
            spell=self,
            loop=loop
        )

        # Execute all effects
        from .effects import EffectFactory
        for effect_data in self.data.effects:
            effect = EffectFactory.create(effect_data, context)
            if effect:
                effect.execute(context)

        return True

    # ---- Display ----

    def description(self):
        """Short description for spell list."""
        return f"{self.name} ({self.cost} mana, {self.cooldown} turn cd)"

    def full_description(self):
        """Full description for spell details screen."""
        return self.data.description

    def __str__(self):
        return self.name


class SpellContext:
    """
    Context object passed to spell effects during execution.

    Contains all the information an effect might need to do its job.
    """

    def __init__(self, caster, target, spell, loop):
        self.caster = caster
        self.target = target
        self.spell = spell
        self.loop = loop

    @property
    def caster_stats(self):
        """Get caster's character stats."""
        return self.caster.character

    def get_skill_damage_bonus(self):
        """Get damage bonus from caster's intelligence."""
        return self.caster_stats.skill_damage_increase()

    def get_skill_duration_bonus(self):
        """Get duration bonus from caster's intelligence."""
        return self.caster_stats.skill_duration_increase()

    def add_message(self, msg):
        """Add a message to the game log."""
        self.loop.add_message(msg)
