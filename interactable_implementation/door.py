from .interactables import Interactable

#Need to fix tile id
class Door(Interactable):
    def __init__(self, render_tag = 700, x=-1, y = -1, name="Door"):  # should be closed door
        super().__init__(x, y,render_tag, name=name)
        self.description = "It is a door"
        self.blocks_vision = True

    def interact(self, loop):
        if self.active:
            self.blocks_vision = False
            self.active = False
            self.set_render_tag(701)  # Tshould be open door
