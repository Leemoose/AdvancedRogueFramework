"""
Node-based Dialogue Tree System.

A cleaner, more maintainable dialogue system that uses a tree structure
instead of flat queues with trait-based conditionals.

Key concepts:
    DialogueNode: A point in conversation (NPC text + player options)
    DialogueOption: A player choice leading to another node or action
    DialogueTree: Container managing traversal and state

Benefits:
    - ~60% fewer lines of code for dialogue definitions
    - Visual clarity - tree structure shows flow at a glance
    - Native options - options are first-class, not tagged dialogue
    - Actions - options can trigger callbacks (give quest, trade, etc.)
    - Conditions - can gate options/nodes on any game state
    - Extensible - easy to add random responses, variables, etc.

Example usage:
    tree = DialogueTree("greeting")
    tree.add_node("greeting", "Hello traveler!", [
        Option("Who are you?", goto="introduce"),
        Option("Goodbye.", goto=END),
    ])
    tree.add_node("introduce", "I am the village elder.", [
        Option("I see.", goto="greeting"),
    ])
"""

from typing import Callable, Optional, Any
from logging_config import get_logger

logger = get_logger(__name__)

# Sentinel for ending dialogue
END = "__END__"
# Sentinel for staying on current node (show options again)
STAY = "__STAY__"


class DialogueOption:
    """
    A player dialogue choice.

    Attributes:
        text: What the player says
        goto: Node ID to go to (or END/STAY)
        action: Optional callback(npc, loop) when selected
        condition: Optional callable(npc, loop) -> bool to show this option
        sets: List of trait names to set when selected
    """

    def __init__(
        self,
        text: str,
        goto: str = END,
        action: Optional[Callable] = None,
        condition: Optional[Callable] = None,
        sets: Optional[list] = None,
    ):
        self.text = text
        self.goto = goto
        self.action = action
        self.condition = condition
        self.sets = sets or []

    def is_available(self, npc, loop) -> bool:
        """Check if this option should be shown."""
        if self.condition is None:
            return True
        try:
            return self.condition(npc, loop)
        except Exception as e:
            logger.warning("Option condition failed: %s", e)
            return False

    def select(self, npc, loop) -> str:
        """
        Called when player selects this option.

        Sets traits, runs action callback, returns next node ID.
        """
        # Set traits
        for trait in self.sets:
            npc.traits[trait] = True
            logger.debug("Set trait: %s", trait)

        # Run action callback
        if self.action:
            try:
                result = self.action(npc, loop)
                # Action can override goto by returning a node ID
                if isinstance(result, str):
                    return result
            except Exception as e:
                logger.error("Option action failed: %s", e)

        return self.goto


class DialogueNode:
    """
    A single point in the dialogue tree.

    Represents what the NPC says and what options the player has.

    Attributes:
        node_id: Unique identifier for this node
        text: What the NPC says (can be str or list for random selection)
        options: List of DialogueOption for player choices
        on_enter: Optional callback(npc, loop) when entering this node
        condition: Optional callable(npc, loop) -> bool to allow entering
    """

    def __init__(
        self,
        node_id: str,
        text: str | list[str],
        options: Optional[list[DialogueOption]] = None,
        on_enter: Optional[Callable] = None,
        condition: Optional[Callable] = None,
    ):
        self.node_id = node_id
        self.text = text
        self.options = options or []
        self.on_enter = on_enter
        self.condition = condition

    def get_text(self) -> str:
        """Get NPC text (handles random selection if list)."""
        if isinstance(self.text, list):
            import random
            return random.choice(self.text)
        return self.text

    def get_available_options(self, npc, loop) -> list[DialogueOption]:
        """Get options that pass their conditions."""
        return [opt for opt in self.options if opt.is_available(npc, loop)]

    def enter(self, npc, loop):
        """Called when dialogue enters this node."""
        if self.on_enter:
            try:
                self.on_enter(npc, loop)
            except Exception as e:
                logger.error("Node on_enter failed: %s", e)

    def can_enter(self, npc, loop) -> bool:
        """Check if this node can be entered."""
        if self.condition is None:
            return True
        try:
            return self.condition(npc, loop)
        except Exception as e:
            logger.warning("Node condition failed: %s", e)
            return False


class DialogueTree:
    """
    Container for a complete dialogue conversation.

    Manages nodes, traversal state, and provides the interface
    used by the dialogue UI system.

    Attributes:
        start_node: ID of the starting node
        nodes: Dict mapping node IDs to DialogueNode objects
        current_node: Currently active node (or None if ended)
        history: List of visited node IDs for this session
    """

    def __init__(self, start_node: str = "start"):
        self.start_node = start_node
        self.nodes: dict[str, DialogueNode] = {}
        self.current_node: Optional[DialogueNode] = None
        self.history: list[str] = []
        self._ended = False

    def add_node(
        self,
        node_id: str,
        text: str | list[str],
        options: Optional[list[DialogueOption]] = None,
        on_enter: Optional[Callable] = None,
        condition: Optional[Callable] = None,
    ) -> "DialogueTree":
        """
        Add a node to the tree. Returns self for chaining.

        Example:
            tree.add_node("greet", "Hello!", [
                Option("Hi!", goto="talk"),
                Option("Bye.", goto=END),
            ]).add_node("talk", "Nice weather.", [
                Option("Indeed.", goto=END),
            ])
        """
        self.nodes[node_id] = DialogueNode(
            node_id=node_id,
            text=text,
            options=options,
            on_enter=on_enter,
            condition=condition,
        )
        return self

    def start(self, npc, loop) -> Optional[DialogueNode]:
        """
        Start or restart the dialogue from the beginning.

        Returns the starting node, or None if it can't be entered.
        """
        self._ended = False
        self.history = []
        return self.goto(self.start_node, npc, loop)

    def goto(self, node_id: str, npc, loop) -> Optional[DialogueNode]:
        """
        Navigate to a specific node.

        Returns the node, or None if dialogue ended or node doesn't exist.
        """
        if node_id == END:
            self._ended = True
            self.current_node = None
            return None

        if node_id == STAY:
            return self.current_node

        if node_id not in self.nodes:
            logger.warning("Unknown dialogue node: %s", node_id)
            self._ended = True
            self.current_node = None
            return None

        node = self.nodes[node_id]

        # Check condition
        if not node.can_enter(npc, loop):
            logger.debug("Cannot enter node %s (condition failed)", node_id)
            return self.current_node  # Stay on current

        # Enter the node
        self.current_node = node
        self.history.append(node_id)
        node.enter(npc, loop)

        return node

    def select_option(self, index: int, npc, loop) -> Optional[DialogueNode]:
        """
        Select a dialogue option by index (0-based).

        Returns the next node, or None if dialogue ended.
        """
        if self.current_node is None:
            return None

        options = self.current_node.get_available_options(npc, loop)

        if index < 0 or index >= len(options):
            logger.warning("Invalid option index: %d", index)
            return self.current_node

        option = options[index]
        next_node_id = option.select(npc, loop)

        return self.goto(next_node_id, npc, loop)

    def has_ended(self) -> bool:
        """Check if dialogue has ended."""
        return self._ended

    def get_current_text(self) -> Optional[str]:
        """Get current NPC text, or None if dialogue ended."""
        if self.current_node is None:
            return None
        return self.current_node.get_text()

    def get_current_options(self, npc, loop) -> list[DialogueOption]:
        """Get available options for current node."""
        if self.current_node is None:
            return []
        return self.current_node.get_available_options(npc, loop)

    @property
    def is_active(self) -> bool:
        """Check if dialogue is in progress."""
        return self.current_node is not None and not self._ended


# Convenience alias
Option = DialogueOption


def build_simple_tree(dialogue_list: list[dict]) -> DialogueTree:
    """
    Build a DialogueTree from a simplified list format.

    This provides an even more concise way to define linear or
    simple branching dialogues.

    Format:
        [
            {"id": "start", "text": "Hello!", "options": [
                {"text": "Hi!", "goto": "greet"},
                {"text": "Bye.", "goto": END},
            ]},
            {"id": "greet", "text": "Nice to meet you.", "options": [
                {"text": "Likewise.", "goto": END},
            ]},
        ]

    Returns:
        Configured DialogueTree
    """
    if not dialogue_list:
        tree = DialogueTree()
        tree.add_node("start", "...", [])
        return tree

    tree = DialogueTree(start_node=dialogue_list[0].get("id", "start"))

    for entry in dialogue_list:
        node_id = entry.get("id", "node")
        text = entry.get("text", "...")
        raw_options = entry.get("options", [])
        on_enter = entry.get("on_enter")
        condition = entry.get("condition")

        options = []
        for opt in raw_options:
            if isinstance(opt, DialogueOption):
                options.append(opt)
            elif isinstance(opt, dict):
                options.append(DialogueOption(
                    text=opt.get("text", "..."),
                    goto=opt.get("goto", END),
                    action=opt.get("action"),
                    condition=opt.get("condition"),
                    sets=opt.get("sets", []),
                ))

        tree.add_node(
            node_id=node_id,
            text=text,
            options=options,
            on_enter=on_enter,
            condition=condition,
        )

    return tree
