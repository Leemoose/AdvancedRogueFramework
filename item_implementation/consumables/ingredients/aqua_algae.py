from .ingredient import Ingredient
from potion_system import PotionTag

class AquaAlgae(Ingredient):
    def __init__(self, render_tag=6003):
        tagNames = [PotionTag.Water, PotionTag.Heal]
        tagProbs = [0.66, 0.33]
        tagDict = {k: v for k, v in zip(tagNames, tagProbs)}
        super().__init__(render_tag, "Aqua Algae", tagDict)
        self.description = "A strain of seaweed that contains the powers of the sea. One bite can quench all your thirst."
        self.rarity = "Common"
        self.action_description = "High chance of water based effects, with a small chance of heal based effects"

    def activate_once(self, entity):
        tag = self.GetTagAtActivate()
        
        # TODO: apply whatever tag we pull