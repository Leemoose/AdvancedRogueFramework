from .terrain import Terrain
from spell_implementation.effects import Slow
class Web(Terrain):
    def __init__(self, x=-1, y=-1, render_tag=2200):
        super().__init__(x=x, y=y, effect = Slow, duration = 1, render_tag = render_tag, name = "Web")
