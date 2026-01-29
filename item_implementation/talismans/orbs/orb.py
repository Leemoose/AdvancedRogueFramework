from item_implementation.items import Item

class OrbOfYendorb(Item):
    def __init__(self):
        super().__init__(-1, -1, 0, 161, "Orb of Yendorb")
        self.equipable = False
        self.equipment_type = "Orb of Yendorb"
        self.description = "Its the all-powerful orb of yendorb. The magic animating it has deactivated"
        self.stackable = False
        self.level = 1
        self.can_be_levelled = False
        self.ped = False
        self.wearer = None
        self.rarity = "YENDORB"
        self.required_strength = 0
        self.attached_skill_exists = False
        self.yendorb = True

class Orb(Item):
    def __init__(self, x = -1, y=-1, id_tag = 0, render_tag = 0, name = "Orb"):
        super().__init__(x,y, id_tag, render_tag, name)
        self.equipable = False
        self.rarity = "Mythic"
        self.traits['orb'] = True

class ForestOrb(Orb):
    def __init__(self, x = -1, y=-1, id_tag = 4000, render_tag = 0, name = "Forest Orb"):
        super().__init__(x,y, id_tag, render_tag, name)
        self.traits["forest_orb"] = True

class OceanOrb(Orb):
    def __init__(self, x = -1, y=-1, id_tag = 4010, render_tag = 0, name = "Ocean Orb"):
        super().__init__(x,y, id_tag, render_tag, name)
        self.traits["ocean_orb"] = True