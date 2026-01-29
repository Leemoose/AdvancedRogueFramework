from .interactables import Interactable
class Statue(Interactable):
    def __init__(self, render_tag = 710, x=-1, y = -1, name="Statue"):  # TileID.ORCISH_IDOL
        super().__init__(x, y, render_tag, name=name)
        self.description = "It is a statue of a monster"

    def interact(self, loop):
        pass
