from .ax import Axe

# class SlicingAxe(Axe):
#     def __init__(self, render_tag):
#         super().__init__(render_tag)
#         self.melee = True
#         self.name = "Slicing Axe"
#         self.description = "Like cutting paper "
#         self.can_be_levelled = True
#
#         self.on_hit = (lambda inflictor: Bleed(3, 4, inflictor))
#         self.on_hit_description = f"The target starts to bleed."
#
#         self.wearer = None  # item_implementation with stat buffs or skills need to keep track of owner for level ups
#         self.rarity = "Rare"
#
#     def attack(self):
#         return (super().attack(), self.on_hit)