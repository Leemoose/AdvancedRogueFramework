from interactable_implementation.environment.pickable import Pickable

class Plant(Pickable):
    def __init__(self, render_tag = 730, x=-1, y = -1, name="Plant"):  # TileID.YELLOW_PLANT
        super().__init__(render_tag=render_tag, x=x, y=y, name=name)
