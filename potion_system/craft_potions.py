from potion_system.tag_manager import PotionTag, potionManager
from item_implementation.consumables.potions import Potion

def get_tag_name(tag):
    return tag.name

def craft_potion(ingredient_list):
    print("Crafting!!")
    tags = []
    for ingredient in ingredient_list:
        new_tags = ingredient.GetTagAtActivate()
        for new_tag in new_tags:
            tags.append(new_tag)

    print("Tags before combo: " + str(tags))
    potionManager.ApplyCombos(tags)
    print("Tags after combo: " + str(tags))

    name = "Potion of "

    if (len(tags) > 0):
        #Sort for name consistency, then cat to get the names!
        tags.sort()
        tag_names = [x.name for x in tags]
        name += " + ".join(tag_names)
    else:
        name += "Nothing"

    new_potion = Potion(6010, name)
    new_potion.tags = tags
    return new_potion
