from spell_implementation.school import School
from .sap_vitality import SapVitality

class NecromancySchool(School):
    def __init__(self):
        super().__init__()

        self.level = {1: SapVitality}
