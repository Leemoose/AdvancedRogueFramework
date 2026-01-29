from item_implementation.equipment import Equipment


"""
RINGS
"""

class Ring(Equipment):
    def __init__(self, render_tag = 3500, name = "Ring"):
        super().__init__(-1, -1, 0, render_tag, name = name)
        self.equipment_type = "Ring"
        self.description = "A ring that does something."
        self.can_be_levelled = False
        self.required_strength = 0
        self.action_description = "Power courses through your hands"
        self.traits["ring"] = True
        self.slot = "ring_slot"
#
# class RingOfSwiftness(Ring):
#     def __init__(self, render_tag):
#         super().__init__(render_tag, "Ring of Swiftness")
#         self.description = "The most circular thing you own, it makes you feel spry on your feet"
#         self.rarity = "Rare"
#         self.action_description = "You move a fifth faster"
#
#     def activate(self, entity):
#         entity.character.change_attribute("Dexterity", 5)
#
#     def deactivate(self, entity):
#         entity.character.change_attribute("Dexterity", -5)
#
#
# class BloodRing(Ring):
#     def __init__(self, render_tag):
#         super().__init__(render_tag, "Blood Ring")
#         self.description = "Pricking your finger on the spikes of this ring makes you feel alive."
#         self.action_description = "Gain the Blood Pact skill."
#
#         # skill doesn't have an owner until equipped to an entity, so need a lambda expression here
#         self.rarity = "Rare"
#         self.attached_skill_exists = True
#
#     def attached_skill(self, owner):
#         self.attached_skill_exists = True
#         return S.BloodPact(owner, cooldown=10, cost=25, strength_increase=5, duration=5, action_cost=100)
#
#
# class RingOfMight(Ring):
#     def __init__(self, render_tag = 503):
#         super().__init__(render_tag, "Ring of Might")
#         self.equipment_type = "Ring"
#         self.name = "Ring of Might"
#         self.description = "A ring that makes you feel stronger."
#         self.action_description = "Gain 4 strength"
#         self.rarity = "Rare"
#
#     def activate(self, entity):
#         entity.character.change_attribute("Strength", 5)
#
#     def deactivate(self, entity):
#         entity.character.change_attribute("Strength", -5)
#
#
# class RingOfMana(Ring):
#     def __init__(self, render_tag):
#         super().__init__(render_tag, "Ring of Mana")
#         self.description = "A ring that every spellcaster is given on their 10th birthday"
#         self.action_description = "Gain 20 mana, 3 intelligence and extra mana regen."
#         self.rarity = "Rare"
#
#     def activate(self, entity):
#         entity.mana += 20
#         entity.character.max_mana += 20
#         entity.character.mana_regen += 4
#         entity.intelligence += 3
#
#     def deactivate(self, entity):
#         entity.mana -= 20
#         entity.character.max_mana -= 20
#         entity.character.mana_regen -= 4
#         entity.intelligence -= 3
#
#
# class BoneRing(Ring):
#     def __init__(self, render_tag):
#         super().__init__(render_tag, "Bone Ring")
#         self.description = "An eerie ring that makes you much stronger and faster while wearing it but rapidly drains your health and mana"
#         self.action_description = "Gain 8 strength and 8 dexterity but lose health and mana over time."
#         self.rarity = "Legendary"
#
#     def activate(self, entity):
#         entity.safe_rest = False
#         entity.character.change_attribute("Strength", 8)
#         entity.character.change_attribute("Dexterity", 8)
#         entity.character.mana_regen -= 10
#         entity.health_regen -= 10  # intended to kill you if you don't take it off after a few turns
#
#     def deactivate(self, entity):
#         entity.safe_rest = True
#         entity.character.change_attribute("Strength", -8)
#         entity.character.change_attribute("Dexterity", -8)
#         entity.character.mana_regen += 10
#         entity.health_regen += 10
#
#
# class RingOfTeleportation(Ring):
#     def __init__(self, render_tag):
#         super().__init__(render_tag, "Ring of Teleportation")
#         self.description = "The most circular thing you own, it makes you feel spry on your feet"
#         self.rarity = "Rare"
#         self.name = "Ring of Teleportation"
#         self.action_description = "Gain the teleport skill."
#
#         self.wearer = None  # item_implementation with stat buffs need to keep track of owner for level ups
#
#         self.skill_cooldown = 40
#         self.skill_cost = 30
#
#         self.attached_skill_exists = True
#
#         self.rarity = "Legendary"
#
#     def attached_skill(self, owner):
#         self.attached_skill_exists = True
#         return Teleport(parent = owner,cooldown = self.skill_cooldown, cost = self.skill_cost)
#
#     def activate(self, entity):
#         # entity.add_skill(self.attached_skill(entity.parent))
#         self.wearer = entity
#         return super().activate(entity)
#
#     def deactivate(self, entity):
#         #if entity.ring_1 != None and entity.ring_1.name == "Ring of Teleportation":
#         #    return  # don't remove skill if other ring was a teleportation ring
#         # entity.remove_skill(self.attached_skill(entity.parent).name)
#         self.wearer = None
#         return super().deactivate(entity)
#
#
# """
#     def level_up(self):
#         self.enchant()
#         if self.level == 2:
#             self.description += " It seems to be growing stronger?"
#         if self.level == 6:
#             self.skill_cooldown = 0
#             self.description = "Unlimited power."
#             """