"""
Burning Attack - A basic fire spell that damages and burns a single target.
"""

from ..base_spell import BaseSpell
from ..targeting import TargetType
from ..effects.damage import DamageEffect
from ..effects.apply_status import ApplyStatusEffect
from ..status_effects import Burn


class BurningAttack(BaseSpell):
    """
    Throw a small bolt of fire at a target that sets the target ablaze.

    Deals fire damage and applies a burn effect that deals damage over time.
    """

    name = "Burning Attack"
    school = "fire"

    cost = 5
    cooldown = 10
    range = 5
    action_cost = 50
    icon = 904

    target_type = TargetType.SINGLE_ENEMY

    effects = [
        DamageEffect(base=3, damage_type="fire", scales=True),
        ApplyStatusEffect(Burn, duration=5, damage=3, scales_duration=True, scales_damage=True),
    ]

    def full_description(self) -> str:
        damage_effect = self.effects[0]
        status_effect = self.effects[1]

        desc = "Throw a small bolt of fire at a target that sets the target ablaze.\n\n"
        desc += f"Deals {damage_effect.base} fire damage at range {self.range}\n"
        desc += f"Burns for {status_effect.kwargs.get('damage', 3)} damage/turn for {status_effect.duration} turns\n"
        desc += f"Costs {self.cost} mana on a {self.cooldown} turn cooldown"

        return desc
