from interactable_implementation.environment.plants.plants import Plant

class YellowPlant(Plant):
    def __init__(self, render_tag = 730, x=-1, y = -1, name="Yellow Plant"):  # TileID.YELLOW_PLANT
        super().__init__(render_tag=render_tag, x=x, y=y, name=name)
        self.charges = 3
