from .potion import Potion
from spell_system.status_effects import Might

class MightPotion(Potion):
    def __init__(self, render_tag=6003):
        super().__init__(render_tag, "Might Potion")
        self.description = "A potion that makes you stronger for a few turns."
        self.rarity = "Rare"
        self.action_description = "Gain 5 strength temporarily."

    def activate_once(self, entity):
        effect = Might(5, 5)
        entity.character.status.add_status_effect(effect)