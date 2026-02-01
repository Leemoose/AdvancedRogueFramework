"""
Key handlers for each game screen.

Each function handles keyboard input for a specific game screen/mode.
Uses input_actions module for key mappings to reduce repetition.
"""

from logging_config import get_logger
from src.core.enums import LoopType
from .input_actions import (
    is_direction_key,
    get_direction,
    get_equipment_slot,
    get_inventory_filter,
    is_quick_cast_key,
    get_skill_index,
    is_quest_number_key,
    key_to_index,
    get_action_screen_change,
    get_item_action,
    get_main_screen_action,
    get_paused_action,
)

logger = get_logger(__name__)


# =============================================================================
# TARGETING / EXAMINE SCREENS
# =============================================================================

def key_targeting_screen(loop, key):
    """Handle input on the targeting screen (selecting a target for an action)."""
    loop.update_screen = True
    targets = loop.targets

    direction = get_direction(key)
    if direction:
        targets.adjust(*direction)
        return

    if key == "esc":
        targets.void_skill()
        loop.player.inventory.ready_scroll = None
        loop.change_loop(LoopType.action)
    elif key == "return":
        if targets.get_has_queued_action() is not None:
            targets.use_queued_action(loop)
        targets.void_skill()
        loop.change_loop(LoopType.action)


def key_examine_screen(loop, key):
    """Handle input on the examine screen (looking around the map)."""
    loop.update_screen = True
    targets = loop.targets

    direction = get_direction(key)
    if direction:
        targets.adjust(*direction)
        return

    if key == "esc":
        targets.void_skill()
        loop.change_loop(LoopType.action)
    elif key == "return":
        loop.change_loop(LoopType.specific_examine)


def key_specific_examine(loop, key):
    """Handle input when examining a specific tile/entity."""
    if key == "esc":
        loop.change_loop(LoopType.examine)


# =============================================================================
# SIMPLE MODAL SCREENS
# =============================================================================

def key_help(loop, key):
    """Handle input on the help screen."""
    if key == "esc":
        loop.change_loop(LoopType.main)


def key_quest(loop, key):
    """Handle input on the quest log screen."""
    logger.debug("Key that you are inputting for quest is: %s", key)

    if key == "esc":
        loop.change_loop(LoopType.action)
    elif is_quest_number_key(key):
        loop.display.quest_number = int(key)
        logger.debug("The new quest number is %s", int(key))
        loop.change_loop(LoopType.quest)


def key_death(loop, key):
    """Handle input on the death screen."""
    if key == "esc":
        loop.clear_data()
        loop.init_game()


def key_victory(loop, key):
    """Handle input on the victory screen."""
    loop.change_loop(LoopType.main)
    loop.clear_data()
    loop.init_game()


def key_rest(loop, key):
    """Handle input during rest (any key interrupts rest)."""
    loop.add_message("Input detected. Ending rest early.")
    loop.change_loop(LoopType.action)


def key_explore(loop, key):
    """Handle input during auto-explore (any key interrupts exploration)."""
    loop.add_message("Input detected. Ending exploration early.")
    loop.player.path = []
    loop.change_loop(LoopType.action)


# =============================================================================
# MAIN ACTION SCREEN
# =============================================================================

def key_action(loop, key):
    """
    Handle input on the main action/gameplay screen.
    This is the primary game state where the player moves and acts.
    """
    player = loop.player

    # Movement and attack
    direction = get_direction(key)
    if direction:
        player.attack_move(*direction, loop)
        return

    # Screen changes (inventory, equipment, spells, etc.)
    screen_change = get_action_screen_change(key)
    if screen_change:
        loop_type, inventory_filter = screen_change
        if inventory_filter:
            if inventory_filter == "main":
                player.inventory.change_active_inventory("main")
            else:
                player.inventory.change_limit_inventory(inventory_filter)
        loop.change_loop(loop_type)
        return

    # Quick cast spells (1-8)
    if is_quick_cast_key(key):
        _handle_quick_cast(loop, player, key)
        return

    # Other actions
    if key == "g":
        _handle_grab(loop, player)
    elif key == "f":
        _start_attack_targeting(loop, player)
    elif key == "l":
        if player.stat_points > 0:
            loop.change_loop(LoopType.level_up)
    elif key == "s":
        _handle_find_stairs(loop, player)
    elif key == ">":
        player.down_stairs(loop)
    elif key == "<":
        player.up_stairs(loop)
    elif key == ".":
        player.character.wait()
        loop.add_message("The player waits.")
    elif key == "x":
        _start_examine_mode(loop, player)
    elif key == "o":
        _handle_autoexplore(loop, player)
    elif key == "t":
        player.do_interact(loop)
    elif key == "z":
        loop.after_rest = LoopType.action
        loop.change_loop(LoopType.resting)
    elif key == "tab":
        player.smart_attack(loop)


def _handle_grab(loop, player):
    """Try to grab an item at the player's location."""
    for item in loop.generator.item_map.get_all_entities():
        if item.x == player.x and item.y == player.y:
            player.do_grab(item, loop)
            break


def _start_attack_targeting(loop, player):
    """Enter targeting mode for a ranged attack."""
    loop.targets.set_target_range(player.get_location(), player.fighter.get_range())
    loop.targets.set_queued_action(player.attack)
    loop.start_targetting()


def _handle_find_stairs(loop, player):
    """Auto-path to stairs if found."""
    player.find_stairs(loop)
    if player.path:
        loop.change_loop(LoopType.pathing)


def _start_examine_mode(loop, player):
    """Enter examine mode centered on the player."""
    loop.change_loop(LoopType.examine)
    loop.targets.set_target(player.get_location())
    loop.set_target(player.get_location())
    loop.update_screen = True


def _handle_autoexplore(loop, player):
    """Start auto-exploration if a path is found."""
    player.autoexplore(loop)
    if player.path:
        loop.change_loop(LoopType.pathing)


def _handle_quick_cast(loop, player, key):
    """Handle quick-casting a spell from the hotbar."""
    skill_num = get_skill_index(key)
    if skill_num >= len(player.mage.quick_cast_spells):
        return
    if player.mage.quick_cast_spells[skill_num] is None:
        return

    loop.targets.set_target_range(player.get_location(), player.fighter.get_range())
    loop.targets.set_queued_action(player.mage.known_spells[skill_num].activate)
    loop.start_targetting()


# =============================================================================
# INVENTORY SCREEN
# =============================================================================

def key_inventory(loop, key):
    """Handle input on the inventory screen."""
    player = loop.player

    if key == "esc":
        _exit_inventory(loop, player)
        return

    # Number keys filter inventory by type
    inventory_filter = get_inventory_filter(key)
    if inventory_filter:
        player.inventory.change_active_inventory("main")
        player.inventory.change_limit_inventory(inventory_filter)
        loop.change_loop(LoopType.inventory)
        return

    # Key "6" switches to orb inventory
    if key == "6":
        player.inventory.change_active_inventory("orb")
        loop.change_loop(LoopType.inventory)
        return

    # Letter keys select items
    index = key_to_index(key)
    if index is not None:
        items = player.inventory.get_limit_inventory()
        if index < len(items):
            loop.targets.set_entity_target(items[index])
            loop.change_loop(LoopType.items)


def _exit_inventory(loop, player):
    """Handle exiting the inventory screen."""
    if player.inventory.limit_inventory == "item":
        loop.change_loop(LoopType.action)
    else:
        loop.change_loop(LoopType.equipment)
    player.inventory.change_limit_inventory("item")


# =============================================================================
# EQUIPMENT SCREEN
# =============================================================================

def key_equipment(loop, key):
    """Handle input on the equipment screen."""
    player = loop.player

    if key == "esc":
        player.inventory.change_limit_inventory("item")
        loop.change_loop(LoopType.action)
        return

    slot = get_equipment_slot(key)
    if slot:
        player.inventory.change_limit_inventory(slot)
        loop.change_loop(LoopType.inventory)


# =============================================================================
# ITEM DETAIL SCREEN
# =============================================================================

def key_item_screen(loop, key):
    """Handle input when viewing/interacting with a specific item."""
    player = loop.player
    item = loop.targets.get_target()
    item_map = loop.generator.item_map
    item_dict = None  # Not used but kept for API compatibility

    if key == "esc":
        _exit_item_screen(loop, item)
        return

    action = get_item_action(key)
    if action == "drop":
        if player.do_drop(item, item_map):
            loop.change_loop(LoopType.inventory)
    elif action == "equip":
        player.do_equip(item)
    elif action == "unequip":
        player.do_unequip(item)
    elif action == "quaff":
        if player.character.quaff(item, item_dict, item_map):
            loop.change_loop(LoopType.inventory)
    elif action == "read":
        player.character.read(item, loop, item_dict, item_map)
    elif action == "activate":
        if player.character.activate(item, loop):
            loop.change_loop(LoopType.inventory)

    loop.change_loop(LoopType.items)


def _exit_item_screen(loop, item):
    """Handle exiting the item detail screen."""
    if loop.player.inventory.limit_inventory == "item":
        loop.change_loop(LoopType.inventory)
    elif item.equipable and item.equipped:
        loop.change_loop(LoopType.equipment)
    else:
        loop.change_loop(LoopType.inventory)


# =============================================================================
# ENCHANT SCREEN
# =============================================================================

def key_enchant(loop, key):
    """Handle input on the enchantment screen."""
    player = loop.player

    if key == "esc":
        loop.change_loop(LoopType.action)
        player.inventory.change_limit_inventory("item")
        player.inventory.ready_scroll = None
        return

    enchantable = player.inventory.get_enchantable()
    index = key_to_index(key)
    if index is not None:
        inventory = player.get_inventory()
        if index < len(inventory) and inventory[index] in enchantable:
            item = inventory[index]
            player.inventory.ready_scroll.consume_scroll(player)
            item.level_up()
            loop.change_loop(LoopType.action)
            player.inventory.change_limit_inventory("item")
            loop.update_screen = True


# =============================================================================
# LEVEL UP SCREEN
# =============================================================================

def key_level_up(loop, key):
    """Handle input on the level up screen."""
    player = loop.player

    if key == "esc":
        loop.change_loop(LoopType.action)
        loop.current_stat = 0
        player.stat_decisions = [0, 0, 0, 0]
        return

    if key == "return":
        player.apply_level_up()
        loop.current_stat = 0
        loop.change_loop(LoopType.action)
        return

    # Navigation within stat selection
    if key == "up" and loop.current_stat > 0:
        loop.current_stat -= 1
    elif key == "down" and loop.current_stat < 3:
        loop.current_stat += 1
    elif key == "left":
        player.modify_stat_decisions(loop.current_stat, increase=False)
    elif key == "right":
        player.modify_stat_decisions(loop.current_stat, increase=True)


# =============================================================================
# TRADE / NPC DIALOG SCREEN
# =============================================================================

def key_trade(loop, key):
    """Handle input during NPC trading/dialog."""
    player = loop.player

    if key == "esc":
        loop.change_loop(LoopType.action)
        loop.next_dialogue = False
        loop.dialogue_options = 0
        loop.player_choice = -1
        return

    # Advance dialogue with no options
    if key == "return" and loop.dialogue_options == 0:
        loop.next_dialogue = True
        return

    # Select a dialogue option
    if loop.dialogue_options > 0 and key in "123456789":
        if int(key) <= loop.dialogue_options:
            loop.npc_focus.change_purpose(int(key), loop)
            loop.player_choice = int(key)
            loop.next_dialogue = False
        return

    # Trade mode: select items with letter keys
    if loop.npc_focus.purpose == "trade":
        index = key_to_index(key)
        if index is not None and index < len(loop.npc_focus.items):
            loop.npc_focus.take_gold(index, loop)
        return

    # Continue talking if no options
    if loop.npc_focus.talking and loop.dialogue_options == 0:
        loop.next_dialogue = True


# =============================================================================
# MAIN MENU SCREEN
# =============================================================================

def key_main_screen(loop, key):
    """Handle input on the main menu screen."""
    if key == "esc":
        return False

    action = get_main_screen_action(key)
    if action == "load":
        loop.load_game()
    elif action == "help":
        loop.change_loop(LoopType.help)
    elif action == "story":
        loop.change_loop(LoopType.story)
    else:
        loop.change_loop(LoopType.action)

    return True


# =============================================================================
# PAUSED SCREEN
# =============================================================================

def key_paused(loop, key):
    """Handle input on the pause menu."""
    if key == "esc":
        loop.change_loop(LoopType.action)
        return True

    action = get_paused_action(key)
    if action == "main_menu":
        loop.change_loop(LoopType.main)
        loop.clear_data()
        loop.init_game()
    elif action == "save":
        loop.memory.update_memory(loop.get_depth(), loop.get_branch())
        loop.memory.save_objects()
    elif action == "quit":
        return False
    elif action == "binding":
        loop.change_loop(LoopType.binding)
        loop.add_message("Please enter the key you want to map from (click return when done):")

    return True


# =============================================================================
# SPELL SCREENS
# =============================================================================

def key_spell(loop, key):
    """Handle input on the spell list screen."""
    player = loop.player

    if key == "esc":
        loop.change_loop(LoopType.action)
        loop.current_spell = None
        return

    index = key_to_index(key)
    if index is not None and 0 <= index < len(player.mage.known_spells):
        loop.current_spell = index
        loop.change_loop(LoopType.spell_individual)


def key_spell_individual(loop, key):
    """Handle input when viewing a specific spell."""
    player = loop.player
    skill_num = loop.current_spell

    if key == "esc":
        loop.change_loop(LoopType.spell)
        loop.current_spell = None
        return

    if key == "q":
        loop.change_loop(LoopType.quickcast)
        return

    if key == "c":
        _cast_spell(loop, player, skill_num)


def _cast_spell(loop, player, skill_num):
    """Attempt to cast a spell, entering targeting mode if needed."""
    spell = player.mage.known_spells[skill_num]

    if not spell.targetted:
        # Non-targeted spell: cast immediately if possible
        if spell.castable(player):
            logger.debug("Casted a spell.")
            player.cast_spell(skill_num, player, loop)
        else:
            loop.add_message(f"You can't cast {spell.name} right now.")
        loop.current_spell = None
    else:
        # Targeted spell: enter targeting mode
        loop.start_targetting(start_on_player=(not spell.targets_monster))
        loop.targets.store_skill(skill_num, spell, player.character)
        loop.current_spell = None


def key_quickselect(loop, key):
    """Handle input on the quick-cast assignment screen."""
    player = loop.player
    spell = player.mage.known_spells[loop.current_spell]

    if key == "esc":
        loop.change_loop(LoopType.spell_individual)
        return

    if key == "p":
        loop.change_loop(LoopType.spell)
        return

    if is_quick_cast_key(key):
        skill_num = get_skill_index(key)
        if skill_num < len(player.mage.quick_cast_spells):
            player.mage.set_quick_cast(spell, skill_num)
            loop.change_loop(LoopType.action)


# =============================================================================
# KEY BINDING SCREEN
# =============================================================================

def key_binding(loop, key):
    """Handle input on the key binding configuration screen."""
    if key == "esc":
        loop.change_loop(LoopType.action)
        loop.clear_message()
        return True

    bindings = loop.keyboard.key_bindings

    if not bindings.accepting_binding:
        # Phase 1: Selecting the source key
        if key == "return":
            bindings.accepting_binding = True
            loop.clear_message()
            loop.add_message("Please enter the keys you want to map to (click return when done): ")
        else:
            bindings.temp_binding = key
            loop.clear_message()
            loop.add_message(f"The key you have chosen is: {key}")
    else:
        # Phase 2: Selecting the target key(s)
        if key == "return":
            bindings.save_key_binding()
            loop.change_loop(LoopType.action)
            loop.clear_message()
        else:
            bindings.temp_binding_map.append(key)
            loop.clear_message()
            keys_str = " ".join(bindings.temp_binding_map)
            loop.add_message(f"The keys you have chosen are: {keys_str}")

    return True
