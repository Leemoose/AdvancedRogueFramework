"""
Concrete game state implementations.

States are organized into logical groups:
    - gameplay_states: Core gameplay (action, targeting, examine)
    - menu_states: Menus and navigation (main, paused, help)
    - inventory_states: Item management (inventory, equipment, items)
    - spell_states: Magic system (spell list, individual spell, quickcast)
    - modal_states: Simple overlays (death, victory, quest, trade)
    - automated_states: AI-driven states (resting, pathing)
"""

from .gameplay_states import ActionState, TargetingState, ExamineState, SpecificExamineState
from .menu_states import MainMenuState, PausedState, HelpState, StoryState
from .inventory_states import InventoryState, EquipmentState, ItemScreenState, EnchantState
from .spell_states import SpellListState, SpellIndividualState, QuickcastState
from .modal_states import DeathState, VictoryState, QuestState, TradeState, LevelUpState
from .automated_states import RestingState, PathingState
from .binding_state import BindingState
from .class_state import ClassState

__all__ = [
    # Gameplay
    'ActionState', 'TargetingState', 'ExamineState', 'SpecificExamineState',
    # Menus
    'MainMenuState', 'PausedState', 'HelpState', 'StoryState',
    # Inventory
    'InventoryState', 'EquipmentState', 'ItemScreenState', 'EnchantState',
    # Spells
    'SpellListState', 'SpellIndividualState', 'QuickcastState',
    # Modals
    'DeathState', 'VictoryState', 'QuestState', 'TradeState', 'LevelUpState',
    # Automated
    'RestingState', 'PathingState',
    # Other
    'BindingState', 'ClassState',
]


def create_all_states(loop):
    """
    Factory function to create all state instances.

    Args:
        loop: The Loops instance that coordinates game state

    Returns:
        list: All state instances ready to be registered
    """
    return [
        # Core gameplay
        ActionState(loop),
        TargetingState(loop),
        ExamineState(loop),
        SpecificExamineState(loop),

        # Menus
        MainMenuState(loop),
        PausedState(loop),
        HelpState(loop),
        StoryState(loop),

        # Inventory management
        InventoryState(loop),
        EquipmentState(loop),
        ItemScreenState(loop),
        EnchantState(loop),

        # Spell system
        SpellListState(loop),
        SpellIndividualState(loop),
        QuickcastState(loop),

        # Modal screens
        DeathState(loop),
        VictoryState(loop),
        QuestState(loop),
        TradeState(loop),
        LevelUpState(loop),

        # Automated states
        RestingState(loop),
        PathingState(loop),

        # Other
        BindingState(loop),
        ClassState(loop),
    ]
