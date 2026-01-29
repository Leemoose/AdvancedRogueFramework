from .skeleton import Skeleton
from monster_implementation import MonsterAI, create_skeleton_behaviors
from item_implementation.weapons import Bow

class SkeletonArcher(Skeleton):
    def __init__(self, x=-1, y=-1, render_tag=1051, name="Skeleton Archer", experience_given=15):
        super().__init__(x=x, y=y, render_tag=render_tag, name=name, experience_given=experience_given)
        self.brain = MonsterAI(self, create_skeleton_behaviors())  # Same AI as skeleton
        self.description = ""
        self.traits["archer"] = True
        self.inventory.get_item(Bow())
        self.body.equip(Bow(), self.character.get_attribute("Strength"))

