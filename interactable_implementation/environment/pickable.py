from interactable_implementation.interactables import Interactable
from item_implementation.items import YellowFlowerPetal

class Pickable(Interactable):
    def __init__(self, render_tag = 730, x=-1, y = -1, name="Pickable"):  # TileID.YELLOW_PLANT
        super().__init__(x=x, y=y, render_tag=render_tag, name=name)
        self.used = False
        self.description = "Should not be in game production so this is a special treat"
        self.charges = 1
        self.item = YellowFlowerPetal

    def interact(self, loop):
        if self.charges > 0:
            loop.player.inventory.get_item(self.item(), loop)
            self.charges -= 1
        if self.charges <= 0:
            loop.generator.interact_map.remove_thing(self)