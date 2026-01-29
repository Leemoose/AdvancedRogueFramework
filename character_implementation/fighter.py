import random

class Fighter():
    def __init__(self, parent):
        self.parent = parent
        self.base_damage = 0

        #Should make an unarmed damage object

    def get_base_damage(self):
        return self.base_damage

    def get_damage_min(self):
        return self.parent.body.get_weapon().get_damage_min() + self.get_base_damage()

    def get_damage_max(self):
        return self.parent.body.get_weapon().get_damage_max() + self.get_base_damage()

    def get_range(self):
        return self.parent.body.get_weapon().get_range()

    def do_defend(self):
        defense = self.parent.character.attributes.get_armor()
        return defense

    def change_base_damage(self, change):
        self.base_damage += change

    """
    1. Damage: Calculate how much damage opponent you would deal
    2. Chance to hit: dexterity vs dexterity affected by how heavy the armor is for both sides (% shave off damage?)
    2. On hit effects
    3. Armor: Armor flat damage decrease vs armor piercing 
    4. Take damage

    Armor piercing <=> Armor
    Magic penetration <=> MR
    Mental power <=> Will power
    Attribute (either suceptible or resistent)
    Accuracy <=> Dodge
    True damage
    On hit modifiers
    
    """

    def do_attack(self, defender, loop):
        dodge_percentage = defender.fighter.get_dodge_chance() - self.get_physical_hit_chance()
        damage_shave = 1 - (max(min(dodge_percentage,100), 0) / 100)
        if damage_shave == 0: #Missed the attack
            return 0

        defender.fighter.do_on_hit_effect(self.parent.body.get_weapon(), loop)
        damage = self.get_damage() * self.parent.character.attributes.get_physical_damage_multiplier()
        defense = defender.do_defend(self.parent, loop) - self.get_armor_piercing()
        finalDamage = max(0, int(damage * damage_shave) - defense)
        if finalDamage > 0:
            defender.fighter.do_on_damage_effect(self.parent.body.get_weapon(), loop)
        defender.character.take_damage(self.parent, finalDamage)
        return finalDamage

    def get_physical_hit_chance(self):
        strike_chance = random.randint(1,100) + self.parent.character.attributes.get_accuracy()
        return strike_chance

    def get_dodge_chance(self):
        dodge_chance = random.randint(1, 100) + self.parent.character.attributes.get_evasion()
        return dodge_chance

    def get_damage(self):
        weapon = self.parent.body.get_weapon()
        return weapon.get_damage() + self.base_damage

    def do_on_hit_effect(self, weapon, loop):
        for effect in weapon.get_on_hit_effect():
            self.parent.character.status.add_status_effect(effect(self.parent))

    def do_on_damage_effect(self, weapon, loop):
        for effect in weapon.get_on_damage_effect():
            self.parent.character.status.add_status_effect(effect(self.parent))


    def get_armor_piercing(self):
        weapon = self.parent.body.get_weapon()
        return weapon.get_armor_piercing()


