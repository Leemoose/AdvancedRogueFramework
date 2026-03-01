from .ingredient import Ingredient
from potion_system import PotionTag

class ThunderShroom(Ingredient):
    def __init__(self, render_tag=6003):
        tagNames = [PotionTag.Lightning, PotionTag.Water]
        tagProbs = [0.66, 0.33]
        tagDict = {k: v for k, v in zip(tagNames, tagProbs)}
        super().__init__(render_tag, "Thunder Shroom", tagDict)
        self.description = "A small mushroom that crackles with static electricity. It has a tingly taste."
        self.rarity = "Common"
        self.action_description = "High chance of lightning based effects, with a small chance of water based effects"

    def activate_once(self, entity):
        tag = self.GetTagAtActivate()
        
        # TODO: apply whatever tag we pull