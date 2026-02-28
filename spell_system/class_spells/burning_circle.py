"""
Burning Circle - Emit a ring of fire around the caster.
"""

from ..base_spell import BaseSpell
from ..targeting import TargetType, get_passable_adjacent_positions
from ..effects.terrain import ModifyTerrainEffect


class BurningCircle(BaseSpell):
    """
    Emit a ring of fire at all tiles around you, setting adjacent spaces ablaze.

    This spell targets the ground rather than enemies directly.
    Enemies standing on or walking through the fire will take burn damage.
    """

    name = "Burning Circle"
    school = "fire"

    cost = 5
    cooldown = 10
    range = 0  # Self-centered
    action_cost = 50

    target_type = TargetType.SELF

    # No direct entity effects
    effects = []

    # Set adjacent tiles on fire
    terrain_effects = [
        ModifyTerrainEffect(on_fire=True),
    ]

    def get_terrain_targets(self, target, context):
        """Get all passable tiles adjacent to the caster."""
        return get_passable_adjacent_positions(self.caster, context)

    def full_description(self) -> str:
        desc = "Emit a ring of fire at all targets around you, setting adjacent spaces ablaze.\n\n"
        desc += f"Costs {self.cost} mana on a {self.cooldown} turn cooldown"
        return desc
