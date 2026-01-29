# from .scroll import Scroll
#
# class TeleportScroll(Scroll):
#     def __init__(self, render_tag):
#         super().__init__(render_tag, "Teleport Scrorb")
#         self.description = "Let's go for a ride."
#         self.rarity = "Common"
#         self.skill = Teleport(None, None, None)
#
#     def activate_once(self, entity, loop):
#         self.skill.parent = entity
#         self.skill.activate(entity, loop.generator, bypass = True)
#         self.consume_scroll(entity)
#         loop.change_loop("inventory")