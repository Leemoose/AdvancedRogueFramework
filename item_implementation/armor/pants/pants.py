from item_implementation.armor.armor import Armor
from item_implementation.statupgrade import statUpgrades

class Pants(Armor):
    def __init__(self, render_tag = 3300, name = "Pants"):
        super().__init__(-1,-1, 0, render_tag, name = name)
        self.equipment_type = "Pants"
        self.name = "Pants"
        self.description = "A pair of pants. Why would you ever take them off?"

        self.stats = statUpgrades(base_str = 0, max_str = 2,
                                  base_end = 1, max_end = 1,
                                  base_arm = 1, max_arm = 3)
        self.slot = "pants_slot"
        self.traits["pants"] = True

    def level_up(self):
        self.enchant()
        if self.level == 2:
            self.description += " It's been enchanted to be more protective."
        if self.level == 6:
            self.description = "A round pair of pants that protects your head from nearly anything. It's been enchanted as much as possible."
