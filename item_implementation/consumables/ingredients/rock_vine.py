from .ingredient import Ingredient
from potion_system import PotionTag

class RockVine(Ingredient):
    def __init__(self, render_tag=6501):
        tagNames = [PotionTag.Stone, PotionTag.Fire]    
        tagProbs = [0.66, 0.33]
        tagDict = {k: v for k, v in zip(tagNames, tagProbs)}
        super().__init__(render_tag, "Rock Vine", tagDict)
        self.description = "A rough looking vine with a tough stone-like exterior"
        self.rarity = "Common"
        self.action_description = "High chance of stone based effects, with a small chance of fire based effects"

    def activate_once(self, entity):
        tag = self.GetTagAtActivate()
        
        # TODO: apply whatever tag we pull