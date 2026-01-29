# class CrushingHammer(Hammer):
#     def __init__(self, render_tag):
#         super().__init__(render_tag)
#         self.melee = True
#         self.name = "Crushing Hammer"
#         self.description = "Player smash. "
#         self.can_be_levelled = True
#
#         self.on_hit = (lambda inflictor: ArmorShredding(5))
#         self.on_hit_description = f"Shreds the targets armor."
#
#         self.wearer = None  # item_implementation with stat buffs or skills need to keep track of owner for level ups
#         self.rarity = "Rare"
#
#     def attack(self):
#         return (super().attack(), self.on_hit)
