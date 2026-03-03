from potion_system.tag_manager import PotionTag
from item_implementation.consumables.potions import Potion

def craft_potion(ingredient_list):
    new_potion = Potion()
    tags = []
    for ingredient in ingredient_list:
        tag = ingredient.GetTagAtActivate()
        tags.append(tag)
    new_potion.tags = tags