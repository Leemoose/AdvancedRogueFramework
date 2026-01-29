from logging_config import get_logger, log_high_priority
from item_implementation.weapons.hands import Unarmed

logger = get_logger(__name__)


class Body():
    def __init__(self, parent, min_damage=2, max_damage = 3):
        self.equipment_slots = {"body_armor_slot": [None],
                                "helmet_slot": [None],
                                "gloves_slot": [None],
                                "boots_slot": [None],
                                "ring_slot": [None, None],
                                "pants_slot": [None],
                                "amulet_slot": [None],
                                "hand_slot": [None, None]
                                }
        self.parent = parent
        self.unarmed = Unarmed(self.parent, min_damage, max_damage)
        logger.debug(f"Body initialized for {parent.name} with equipment slots")


    def can_equip(self, item):
        return True

    def can_unequip(self, item):
        return True

    def num_total_equipment_slots(self, slot):
        return len(self.equipment_slots[slot])

    def get_num_free_equipment_slots(self, slot):
        if slot not in self.equipment_slots:
            log_high_priority(logger, "You are trying to find a %s in %s's equipment slot", slot, self.parent.name)
            return 0
        free_slots = 0
        for item in self.equipment_slots[slot]:
            if item is None:
                free_slots += 1
        return free_slots

    def add_item_to_equipment_slot(self, item, slot, num_slots):
        logger.debug(f"Adding item {item.name if hasattr(item, 'name') else item} to {slot}")
        i = 0
        for item_slot in range(len(self.equipment_slots[slot])):
            if self.equipment_slots[slot][item_slot] is None:
                self.equipment_slots[slot][item_slot] = item
                logger.debug(f"Item added successfully to slot index {item_slot}")
                return True
        log_high_priority(logger, "Failed to equip item %s to equipment slot %s", item.name if hasattr(item, 'name') else item, slot)
        return False

    def remove_item_from_equipment_slot(self, item, slot, num_slots):
        logger.debug(f"Removing item {item.name if hasattr(item, 'name') else item} from {slot}")
        i = 0
        for item_slot in range(len(self.equipment_slots[slot])):
            if self.equipment_slots[slot][item_slot] is item:
                self.equipment_slots[slot][item_slot] = None
                i += 1
            if i >= num_slots:
                break
        if i >= num_slots:
            logger.debug(f"Successfully removed {i} slot(s) for item")
            return True
        else:
            logger.warning(f"Something has probably gone wrong with unequipping - only removed {i} of {num_slots} slots")
            return False

    def remove_equipment_slot(self, slot):
        if slot not in self.equipment_slots:
            log_high_priority(logger, "You are trying to find a %s in %s's equipment slot", slot, self.parent.name)
            return False
        try:
            self.equipment_slots[slot].remove(None)
        except:
            log_high_priority(logger, "You tried to remove a %s in %s's equipment slot but there was nothing that could be removed", slot, self.parent.name)
        return False

    def add_equipment_slot(self, slot):
        if slot not in self.equipment_slots:
            log_high_priority(logger, "You are trying to find a %s in %s's equipment slot", slot, self.parent.name)
            return False
        self.equipment_slots[slot].append(None)
        return True

    def get_items_in_equipment_slot(self, slot):
        carried = []
        if slot not in self.equipment_slots:
            log_high_priority(logger, "You are trying to find a %s in %s's equipment slot", slot, self.parent.name)
            return carried
        else:
            for item in self.equipment_slots[slot]:
                if item is not None:
                    carried.append(item)
        return carried

    def get_nth_item_in_equipment_slot(self, slot, n):
        items = self.get_items_in_equipment_slot(slot)
        if len(items) > n:
            return items[n]


    def equip(self, item, strength):
        logger.debug(f"Attempting to equip {item.name if hasattr(item, 'name') else item} (required strength: {item.required_strength}, current: {strength})")
        slot = item.get_slot()
        if strength >= item.required_strength:
            self.unequip_current(item) # frees slots for current item
            self.add_item_to_equipment_slot(item, slot, item.slots_taken)
            item.equipped = True
            item.dropable = False
            if item.attached_skill_exists:
                self.parent.character.add_skill(item.attached_skill(self.parent))
            logger.info(f"Equipped {item.name if hasattr(item, 'name') else item} to {slot}")
            # item.activate(self.parent)
        else:
            logger.debug(f"Cannot equip {item.name if hasattr(item, 'name') else item} - insufficient strength")


    def unequip_current(self, item):
        logger.debug(f"Unequipping current items to make room for {item.name if hasattr(item, 'name') else item}")
        if item.has_trait("weapon"):
            self.unequip(self.get_weapon()) # if a weapon is already equipped, unequip it
            if item.slots_taken > 1: # two handed weapon
                self.unequip(self.get_shield()) # if a shield is equipped in offhand, unequip it
        elif item.has_trait("shield"):
            self.unequip(self.get_shield())
            weapon = self.get_weapon()
            if weapon and weapon.slots_taken > 1: # two handed weapon must be unequipped for a shield
                self.unequip(weapon)
        elif item.has_trait("ring"):
            if self.get_num_free_equipment_slots("ring_slot") == 0:
                self.unequip(self.get_items_in_equipment_slot("ring_slot")[0])
                for slot in range(self.num_total_equipment_slots("ring_slot") - 1):
                    self.equipment_slots["ring_slot"][slot] = self.equipment_slots["ring_slot"][slot + 1]
                self.equipment_slots["ring_slot"][-1] = None


    def unequip(self, item):
        if item is None: # lets us call unequip with get_weapon
            return False
        logger.debug(f"Unequipping {item.name if hasattr(item, 'name') else item}")
        slot = item.get_slot()
        self.remove_item_from_equipment_slot(item, slot, item.slots_taken)
        item.dropable = True
        item.equipped = False
        if item.attached_skill_exists:
            self.parent.character.remove_skill(item.attached_skill(self.parent))
        item.deactivate(self.parent)
        logger.info(f"Unequipped {item.name if hasattr(item, 'name') else item} from {slot}")

    def get_weapon(self):
        carried_items = self.equipment_slots["hand_slot"]
        for item in carried_items:
            if item is not None and item.has_trait("weapon"):
                return item
        return self.unarmed

    def get_shield(self):
        carried_items = self.equipment_slots["hand_slot"]
        for item in carried_items:
            if item is not None and item.has_trait("shield"):
                return item
        return None

    def get_in_slot(self, slot):
        carried_items = self.equipment_slots[slot]
        for item in carried_items:
            if item is not None:
                return item
        return None
