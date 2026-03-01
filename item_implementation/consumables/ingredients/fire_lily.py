from .ingredient import Ingredient
from tag_manager import PotionTag

class FireLily(Ingredient):
    def __init__(self, render_tag=6003):
        tagNames = [PotionTag.Fire, PotionTag.Lightning]
        tagProbs = [0.66, 0.33]
        tagDict = {k: v for k, v in zip(tagNames, tagProbs)}
        super().__init__(-1, -1, 0, render_tag, "Fire Lily", tagDict)
        self.description = "A lily with red petals that grow in hot environments. They are so spicy they are inedible."
        self.rarity = "Common"
        self.action_description = "High chance of fire based effects, with a small chance of lightning"

    def activate_once(self, entity):
        tag = self.GetTagAtActivate()
        
        # TODO: apply whatever tag we pull