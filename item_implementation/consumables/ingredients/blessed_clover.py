from .ingredient import Ingredient
from potion_system import PotionTag

class BlessedClover(Ingredient):
    def __init__(self, render_tag=6003):
        tagNames = [PotionTag.Heal]
        tagProbs = [1.0]
        tagDict = {k: v for k, v in zip(tagNames, tagProbs)}
        super().__init__(render_tag, "Blessed Clover", tagDict)
        self.description = "A small clover that heals you when eating, a commmon ingredient in healing potions"
        self.rarity = "Common"
        self.action_description = "Guaranteed chance of healing"

    def activate_once(self, entity):
        tag = self.GetTagAtActivate()
        
        # TODO: apply whatever tag we pull