"""
Fireball - A powerful AoE fire spell.
"""

from ..base_spell import BaseSpell
from ..targeting import (
    TargetType,
    get_enemies_in_radius,
    get_positions_in_radius,
)
from ..effects.damage import DamageEffect
from ..effects.apply_status import ApplyStatusEffect
from ..effects.terrain import ModifyTerrainEffect
from ..status_effects import Burn


class Fireball(BaseSpell):
    """
    Throw a giant ball of fire at a target location.

    Hits all enemies in a 3x3 area (radius 1) and sets the ground on fire.
    Enemies hit take fire damage and are set ablaze.
    """

    name = "Fireball"
    school = "fire"

    cost = 10
    cooldown = 20
    range = 10
    action_cost = 150
    required_intelligence = 5

    target_type = TargetType.GROUND

    effects = [
        DamageEffect(base=10, damage_type="fire", scales=True),
        ApplyStatusEffect(Burn, duration=2, damage=3, scales_duration=True, scales_damage=True),
    ]

    terrain_effects = [
        ModifyTerrainEffect(on_fire=True),
    ]

    # AoE radius
    radius = 1

    def get_targets(self, target, context):
        """Get all enemies within radius of target position."""
        return get_enemies_in_radius(target, self.radius, context, include_center=True)

    def get_terrain_targets(self, target, context):
        """Get all positions within radius to set on fire."""
        return get_positions_in_radius(
            target, self.radius, context,
            include_center=True, passable_only=True
        )

    def full_description(self) -> str:
        damage_effect = self.effects[0]
        status_effect = self.effects[1]

        desc = "Throw a giant ball of fire at a target that hits a 3x3 area "
        desc += "centered on the target, setting all enemies in range ablaze.\n\n"
        desc += f"Deals {damage_effect.base} fire damage at range {self.range}\n"
        desc += f"Burns targets for {status_effect.kwargs.get('damage', 3)} damage/turn "
        desc += f"for {status_effect.duration} turns\n"
        desc += f"Costs {self.cost} mana on a {self.cooldown} turn cooldown\n"
        desc += f"Requires {self.required_intelligence} Intelligence"

        return desc
