from .potion import Potion
class HealthPotion(Potion):
    def __init__(self, render_tag = 3700):
        super().__init__(render_tag = render_tag,name = "Health Potion")
        self.description = "A potiorb that heals you."
        self.action_description = "Heal by 20 + 10% max health."
        self.rarity = "Common"

    def activate_once(self, entity):
        entity.character.change_health(20 + (entity.character.get_max_health() // 10))
#