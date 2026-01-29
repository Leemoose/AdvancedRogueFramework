from .bodyarmor import BodyArmor
from item_implementation.statupgrade import statUpgrades
class LeatherArmor(BodyArmor):
    def __init__(self, render_tag = 3000):
        super().__init__(render_tag, "Leather Armor")
        self.description = "A comfortable piece of armor, that helps you feel lighter on your feet. "
        self.wearer = None  # item_implementation with stat buffs need to keep track of owner for level ups
        self.stats = statUpgrades(base_arm=1, max_arm=1)

    def level_up(self):
        self.enchant()
        if self.level == 2:
            self.description += " It's been enchanted to make you more nimble."
        if self.level == 6:
            self.description = "Comfortable armor that makes you feel incredibly fast on your feet while offering decent protection. It's been enchanted as much as possible."
