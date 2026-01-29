from .interactables import Interactable
class HealthFountain(Interactable):
    def __init__(self, render_tag = 6000,x=-1, y = -1, name="Health Fountain"):
        super().__init__(x, y,render_tag, name=name)
        self.description = "It is a fountain of healing"

    def interact(self, loop):
        if self.active:
            loop.player.character.change_health(loop.player.character.get_max_health()-loop.player.character.get_health())
            self.active = False
            self.set_render_tag(6010)
