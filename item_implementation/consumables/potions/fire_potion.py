from spell_system.status_effects import Burn
from .potion import Potion
from dungeon_generation.terrain.fire import Fire
from spell_system.status_effects.health_bump import HealthBump

class FirePotion(Potion):
    def __init__(self, render_tag=6020):
        super().__init__(render_tag, "Fire Potion")
        self.description = "A fire potion."
        self.action_description = "Heat flows through your body"

    def apply_to_entity(self, entity, loop):
        loop.add_message(f"The {self.name} splashes onto {entity.name}!", (200, 200, 200))
        entity.character.status.add_status_effect(Burn(5, 3, entity))

    def apply_to_tile(self, tile, loop):
        loop.add_message(f"The {self.name} shatters on the ground!", (200, 200, 200))
        tile.add_terrain(Fire(duration=10))

    def quaff(self, entity, loop):
        loop.add_message(f"You drink the {self.name}!", (200, 200, 200))
        entity.character.status.add_status_effect(HealthBump(10))

    def apply_to_equipment(self, equipment, loop):
        loop.add_message(f"You apply the {self.name} to your {equipment.name}!", (200, 200, 200))
        if equipment.has_trait("weapon"):
            equipment.add_on_damage_effect(Burn)
        elif equipment.has_trait("armor"):
            #add part here about equipment gaining on hit defense effect
            pass
        else:
            pass
