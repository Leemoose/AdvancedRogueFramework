# In progress
class Attributes():
    def __init__(self, parent, endurance=0, intelligence=0, dexterity=0, strength=0, health=100, mana=0, health_regen=0.2, mana_regen=0.2, experience_given=0):
        self.parent = parent

        self.base_endurance = endurance
        self.base_intelligence = intelligence
        self.base_dexterity = dexterity
        self.base_strength = strength
        self.endurance = endurance
        self.intelligence = intelligence
        self.dexterity = dexterity
        self.strength = strength

        self.health = health
        self.max_health = health
        self.mana = mana
        self.max_mana = mana
        self.health_regen = health_regen
        self.mana_regen = mana_regen

        self.accuracy = 0
        self.evasion = 0

        self.magical_resistance = 0
        self.magical_power = 0

        self.physical_damage_multiplier = 1
        self.armor = 0

        self.resistances = {"fire": 0, "cold": 0, "poison": 0, "will": 0}

        self.experience_given = experience_given  # monsters will overwrite this attribute, it just makes some class stuff easier if its stored in character
        self.experience = 0
        self.experience_to_next_level = 20

    def calculate_attributes(self):
        self.max_health = self.endurance * 3 + self.parent.parent.get_level() * 5
        self.max_mana = self.intelligence * 2 + self.parent.parent.get_level() * 3
        self.health_regen = self.endurance * 0.01 + 0.2
        self.mana_regen = self.intelligence * 0.01 + 0.2
        self.accuracy = self.dexterity
        self.evasion = self.dexterity
        self.magical_resistance = self.intelligence #chance of avoiding a spell
        self.magical_power = self.intelligence #chance of hitting a spell
        self.physical_damage_multiplier = 1 + self.strength * .01

    def get_health(self):
        return int(self.health)

    def get_max_health(self):
        return int(self.max_health)

    def get_health_regen(self):
        return self.health_regen

    def get_mana(self):
        return int(self.mana)

    def get_max_mana(self):
        return int(self.max_mana)

    def get_mana_regen(self):
        return self.mana_regen

    def get_strength(self):
        return self.strength

    def get_intelligence(self):
        return self.intelligence

    def get_endurance(self):
        return self.endurance

    def get_dexterity(self):
        return self.dexterity

    def get_experience_given(self):
        return self.experience_given

    def get_armor(self):
        return self.armor

    def change_strength(self, change):
        self.strength += change
        self.calculate_attributes()

    def change_intelligence(self, change):
        self.intelligence += change
        self.calculate_attributes()

    def change_endurance(self, change):
        self.endurance += change
        self.calculate_attributes()

    def change_dexterity(self, change):
        self.dexterity += change
        self.calculate_attributes()

    def change_health(self, change):
        self.health += change
        #self.health = int(self.health)
        if self.health > self.max_health:
            self.health = self.max_health

    def change_max_health(self, change):
        self.max_health += change
        self.change_health(change)

    def change_mana(self, change):
        self.mana += change
        if self.get_mana() > self.get_max_mana():
            self.mana = self.get_max_mana()

    def change_mana_override(self, new_mana):
        self.mana = new_mana
        if self.get_mana() > self.get_max_mana():
            self.mana = self.get_max_mana()

    def change_max_mana(self, change):
        self.max_mana += change
        self.change_mana(change)

    def change_experience(self, change):
        self.experience += change

    def change_armor(self, change):
        self.armor += change

    def can_level_up(self):
        return self.experience >= self.experience_to_next_level

    def level_up(self):
        self.change_max_mana(3)
        self.change_max_health(5)
        self.change_experience(-self.experience_to_next_level)
        self.experience_to_next_level += 20 + self.experience_to_next_level // 4

    def get_experience(self):
        return self.experience

    def get_experience_to_next_level(self):
        return self.experience_to_next_level

    def get_evasion(self):
        return self.evasion

    def get_accuracy(self):
        return self.accuracy

    def get_physical_damage_multiplier(self):
        return self.physical_damage_multiplier



