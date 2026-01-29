from monsters.monster import Monster
from monster_implementation import MonsterAI, create_orc_behaviors

class Orc(Monster):
    def __init__(self, x=-1, y=-1, render_tag=2300, name="Orc", experience_given=20, health=20, min_damage=4, max_damage=8, rarity="Common"):  # TileID.ORC_KNIGHT from asset_registry.py
        super().__init__(x=x, y=y, render_tag=render_tag, name=name, experience_given=experience_given, health=health, min_damage=min_damage, max_damage=max_damage, rarity=rarity)
        self.brain = MonsterAI(self, create_orc_behaviors())
        self.character.skills = []
        self.description = "Hailing from the brutal and war-torn realms beyond the rifts, the Orc is a towering brute with muscles rippling beneath its coarse, green skin. Adorned in crude armor fashioned from bones and scavenged metal, its bloodshot eyes burn with a fierce determination for battle. The stench of blood and sweat follows this savage warrior, who wields a jagged, rusted blade with deadly proficiency. Covered in tribal tattoos and scars earned in countless skirmishes, the Rift Orc thrives in combat, reveling in the chaos of battle cries and the clash of weapons. Its growls and guttural shouts echo through the rifts, striking fear into the hearts of all who dare to oppose it. Beware its raw strength and relentless aggression, for the Orc knows no mercy on the battlefield.."
        self.strength = 3
        self.dexterity = 0
        self.endurance = 3
        self.intelligence = 0
        self.character.armor = 1
