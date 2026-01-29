"""
All detailed item_implementation are initialized here.
"""
from .items import Item
from .statupgrade import statUpgrades
class Equipment(Item):
    def __init__(self, x, y, id_tag, render_tag, name):
        super().__init__(x,y, id_tag, render_tag, name)
        self.equipable = True
        self.equipped = False
        self.wearer = None
        self.cursed = False
        self.rarity = "Common"
        self.required_strength = 0
        self.stats = statUpgrades()
        self.traits["equipment"] = True
        self.slot = "hand_slot"
        self.slots_taken = 1

    def get_slot(self):
        return self.slot

    def activate(self, entity):
        self.wearer = entity
        self.add_stats(entity)

    def deactivate(self, entity):
        self.wearer = None
        self.remove_stats(entity)

    def enchant(self):
        self.level += 1
        if (self.wearer):
            self.update_stats_level_up(self.wearer)

    def add_stats(self, entity):
        (str, dex, intl, end, arm) = self.stats.GetStatsForLevel(self.level)
        entity.change_attribute("Strength", str)
        entity.change_attribute("Intelligence", intl)
        entity.change_attribute("Endurance", end)
        entity.change_attribute("Dexterity", dex)
        entity.change_attribute("Armor", arm)

    #Called after level up has completed to get stats to match!
    def update_stats_level_up(self, entity):
        (str, dex, intl, end, arm) = self.stats.GetStatsForLevelUp(self.level)
        entity.change_attribute("Strength", str)
        entity.change_attribute("Intelligence", intl)
        entity.change_attribute("Endurance", end)
        entity.change_attribute("Dexterity", dex)
        entity.change_attribute("Armor", arm)

    def remove_stats(self, entity):
        (str, dex, intl, end, arm) = self.stats.GetStatsForLevel(self.level)
        entity.change_attribute("Strength", str)
        entity.change_attribute("Intelligence", intl)
        entity.change_attribute("Endurance", end)
        entity.change_attribute("Dexterity", dex)
        entity.change_attribute("Armor", arm)

    def can_be_equipped(self, entity):
        return self.equipable and entity.get_attribute("Strength") >= self.required_strength

    def can_be_unequipped(self, entity):
        return (self.equipped and not self.cursed)

    def get_attached_skill_description(self):
        if self.attached_skill_exists:
            return self.attached_skill(None).description() # temporarily attach skill to nothing to get name
        else:
            return None

    def level_up(self):
        pass