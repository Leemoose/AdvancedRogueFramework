from monsters.monster import Monster
from monster_implementation import MonsterAI, create_skeleton_behaviors
from spell_system import give_spell

"""Lich - undead spellcaster king."""
class Lich(Monster):
    def __init__(self, x=-1, y=-1, render_tag=-1, name="Lich"):
        super().__init__(x=x, y=y, render_tag=render_tag, name=name, experience_given=10, health=10, mana=10, gold=20)
        self.brain = MonsterAI(self, create_skeleton_behaviors())
        self.skills = []
        give_spell(self, 'sap_vitality', cooldown=5, cost=3, range=5,
                   effects_overrides=[{'amount': 3}])
        self.endurance = 0
        self.strength = 0
        self.dexterity = 0
        self.intelligence = 10
        self.description = "The king of the dead"
        self.traits["lich"] = True
