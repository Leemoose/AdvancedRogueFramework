from potion_system.tag_manager import PotionTag, potionManager
from item_implementation.consumables.potions import Potion


def craft_potion(ingredient_list):
    print("Crafting!!")
    new_potion = Potion(6010, "Crafted Potion")
    tags = []
    for ingredient in ingredient_list:
        tag = ingredient.GetTagAtActivate()
        tags.append(tag)
    potionManager.ApplyCombos(tags)
    new_potion.tags = tags
    return new_potion
