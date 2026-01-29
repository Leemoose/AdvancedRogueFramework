from monsters.monster import Monster
from monster_implementation import MonsterAI, create_skeleton_behaviors

class Skeleton(Monster):
    def __init__(self, x=-1, y=-1, render_tag=2500, name="Skeleton", experience_given=10):  # TileID.SKELETON from asset_registry.py
        super().__init__(x=x, y=y, render_tag=render_tag, name=name, experience_given=experience_given)
        self.brain = MonsterAI(self, create_skeleton_behaviors())
        self.description = ""
        self.traits["skeleton"] = True


