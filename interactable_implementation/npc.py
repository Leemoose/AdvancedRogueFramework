"""
NPC System.

Provides NPCs that can be talked to, give quests, and (in the future) trade items.
NPCs inherit from Interactable for clean integration with the existing system.

Dialogue System:
    Uses a node-based DialogueTree for cleaner, more maintainable conversations.
    Each node represents what the NPC says plus available player options.
    Options can trigger actions, set traits, and navigate to other nodes.

Classes:
    NPC: Base class for all NPCs
    QuestGiver: NPC that can give and track quests

Example NPCs:
    ForestHermit: Gives exploration quest
    VillageElder: Gives goblin slaying quest
"""

from logging_config import get_logger
from .interactables import Interactable
from .quest import Quest, GoblinSlayerQuest, DungeonDelverQuest
from .dialogue import DialogueTree, DialogueNode, DialogueOption, Option, END, STAY
from loop_workflow.looptype import LoopType

logger = get_logger(__name__)


class NPC(Interactable):
    """
    Base class for all NPCs.

    NPCs can be talked to and have dialogue trees with branching conversations.
    They integrate with the existing TradeState for dialogue display.

    Attributes:
        dialogue_tree: DialogueTree managing the conversation
        dialogue_memory: History of dialogue for UI display
        traits: Dict of flags that can be used for conditions
        options: List of interaction options (Talk, Quest, Trade)
        purpose: Current interaction mode
        talking: Whether currently in dialogue
    """

    def __init__(self, x=-1, y=-1, render_tag=0, name="NPC"):
        super().__init__(x=x, y=y, render_tag=render_tag, name=name)
        self.traits["npc"] = True

        # Dialogue system (new tree-based)
        self.dialogue_tree: DialogueTree = self.build_dialogue_tree()
        self.dialogue_memory = []

        # Legacy compatibility - these are used by the UI
        self.dialogue_queue = []  # Populated from tree for UI compatibility
        self.dialogue_dict = {}
        self.trait_dict = {}
        self.repeat_dict = {}

        # Interaction state
        self.options = ["Talk"]
        self.purpose = None
        self.talking = False
        self.has_stuff_to_say = True

        # Trading (future)
        self.items = []
        self.cost = 5

        # Quest (set by subclasses)
        self.quest = None
        self.gave_quest = False

        # Set description
        self.description = f"{self.name} - An NPC you can talk to."

    def build_dialogue_tree(self) -> DialogueTree:
        """
        Build and return the dialogue tree for this NPC.

        Override in subclasses to define conversation structure.
        Returns a DialogueTree with nodes and options.
        """
        tree = DialogueTree("start")
        tree.add_node("start", "...", [])
        return tree

    def start_dialogue(self, loop):
        """
        Start or restart the dialogue from the beginning.

        Called when player initiates conversation.
        """
        self.dialogue_tree.start(self, loop)
        self._sync_to_queue(loop)

    def _sync_to_queue(self, loop):
        """
        Sync the current dialogue tree state to the legacy queue format.

        This maintains compatibility with the existing DialogueInteraction UI.
        """
        self.dialogue_queue.clear()

        if self.dialogue_tree.has_ended():
            return

        # Get current NPC text
        npc_text = self.dialogue_tree.get_current_text()
        if npc_text:
            self.dialogue_queue.append([npc_text, False])

        # Get current options
        options = self.dialogue_tree.get_current_options(self, loop)
        if options:
            # Group all options together (same ID in old system)
            option_texts = [opt.text for opt in options]
            self.dialogue_queue.append(option_texts + [True])  # True = player options

    def advance_dialogue(self, choice_index: int, loop):
        """
        Advance dialogue by selecting an option.

        Args:
            choice_index: 0-based index of the selected option
            loop: Game loop instance
        """
        if self.dialogue_tree.has_ended():
            return

        options = self.dialogue_tree.get_current_options(self, loop)

        if choice_index < 0 or choice_index >= len(options):
            # No options or invalid - just check if we should end
            if not options:
                # NPC monologue - this shouldn't happen with tree system
                pass
            return

        # Select the option
        self.dialogue_tree.select_option(choice_index, self, loop)

        # Sync to legacy queue
        self._sync_to_queue(loop)

    def add_to_memory(self, text, left, choice, action, loop):
        """
        Add dialogue to memory and process trait changes.

        Args:
            text: The dialogue text
            left: Whether displayed on left (player) side
            choice: Whether this was a player choice being displayed
            action: The action string
            loop: The game loop instance
        """
        self.dialogue_memory.append((text, left, choice, action))

        # When a player choice is confirmed (not just displayed)
        if not choice and left:
            # Find and execute the matching option
            stripped_text = text.split(". ", 1)[-1] if text[0].isdigit() else text
            options = self.dialogue_tree.get_current_options(self, loop)
            for i, opt in enumerate(options):
                if opt.text == stripped_text:
                    self.dialogue_tree.select_option(i, self, loop)
                    # Sync the new state to the queue for the UI
                    self._sync_to_queue(loop)
                    break

    def _check_focus(self, loop):
        """
        Check and update the NPC's purpose based on current state.

        Override in subclasses for custom behavior.
        """
        pass

    def change_purpose(self, selection, loop):
        """
        Change the NPC's current interaction mode.

        Args:
            selection: Either an int (dialogue option) or string (mode name)
            loop: The game loop instance
        """
        if isinstance(selection, int):
            # Dialogue option selected - handled by tree system now
            pass
        elif isinstance(selection, str):
            if selection in self.options:
                self.purpose = selection.lower()
                if self.purpose == "quest":
                    self.give_quest(loop)

    def give_quest(self, loop):
        """
        Give the NPC's quest to the player.

        Override in subclasses for custom quest-giving behavior.
        """
        if self.quest is None:
            return

        if self.gave_quest:
            # Check for completion
            if self.quest.check_for_completion(loop):
                self.traits["quest_completed"] = True
                self.quest.give_reward(loop)
                self._check_focus(loop)
                loop.add_message(f"Quest '{self.quest.name}' completed!", (255, 215, 0))
        else:
            # Give quest
            loop.player.add_quest(self.quest)
            self.gave_quest = True
            self.traits["quest_given"] = True

            # Set start count for kill quests
            if hasattr(self.quest, 'set_start_count'):
                self.quest.set_start_count(loop)

            loop.add_message(f"New quest: {self.quest.name}", (255, 215, 0))

    def interact(self, loop):
        """
        Called when player interacts with this NPC.

        Enters dialogue mode via TradeState.
        """
        logger.debug("Player interacting with NPC: %s", self.name)
        loop.npc_focus = self
        self.talking = True

        # Always restart dialogue from beginning for fresh conversations
        # The tree will handle conditional starting points
        self.dialogue_memory.clear()
        self.start_dialogue(loop)

        loop.change_loop(LoopType.trade)

    # =========================================================================
    # Legacy compatibility methods (used by existing UI)
    # =========================================================================

    def get_dialogue_data(self):
        """Legacy method - returns empty list as we use tree now."""
        return []

    def insert_into_dialogue_queue(self, text, is_player):
        """Legacy method - no longer used with tree system."""
        pass

    def _check_dialogues_to_add(self):
        """Legacy method - tree handles this automatically."""
        pass


class QuestGiver(NPC):
    """
    NPC that primarily exists to give and track a quest.

    Adds "Quest" to options and provides helper methods for
    quest-related dialogue.
    """

    def __init__(self, x=-1, y=-1, render_tag=0, name="Quest Giver"):
        super().__init__(x=x, y=y, render_tag=render_tag, name=name)
        self.options = ["Talk", "Quest"]

    def _check_focus(self, loop):
        """Auto-switch to quest mode if quest was given."""
        if self.has_trait("quest_given") and not self.has_trait("quest_completed"):
            self.purpose = "quest"

    def _give_quest_action(self, npc, loop):
        """Action callback to give quest from dialogue option."""
        npc.give_quest(loop)
        return None  # Don't override goto

    def start_dialogue(self, loop):
        """
        Start dialogue, checking for quest completion first.

        If quest is complete, starts at completion node.
        """
        # Check if quest is complete before starting dialogue
        if self.quest and self.gave_quest and not self.has_trait("quest_completed"):
            if self.quest.check_for_completion(loop):
                self.traits["quest_completed"] = True
                self.quest.give_reward(loop)
                loop.add_message(f"Quest '{self.quest.name}' completed!", (255, 215, 0))

        # Now start dialogue - tree conditions will check quest_completed trait
        if self.has_trait("quest_completed") and "quest_complete" in self.dialogue_tree.nodes:
            # Go directly to completion dialogue
            self.dialogue_tree._ended = False
            self.dialogue_tree.history = []
            self.dialogue_tree.goto("quest_complete", self, loop)
        else:
            self.dialogue_tree.start(self, loop)

        self._sync_to_queue(loop)


# =============================================================================
# EXAMPLE NPCs - Now using the cleaner tree-based dialogue system
# =============================================================================

class ForestHermit(QuestGiver):
    """A hermit in the forest who gives an exploration quest."""

    def __init__(self, x=-1, y=-1, render_tag=126, name="Forest Hermit"):
        self._custom_quest = DungeonDelverQuest(target_depth=3)
        super().__init__(x=x, y=y, render_tag=render_tag, name=name)
        self.quest = self._custom_quest

    def build_dialogue_tree(self) -> DialogueTree:
        tree = DialogueTree("greeting")

        # Greeting node
        tree.add_node("greeting", "Ah, a traveler! These woods hide many secrets.", [
            Option("Who are you?", goto="introduce"),
            Option("What secrets?", goto="secrets"),
        ])

        # Introduction branch
        tree.add_node("introduce", "I am but a humble hermit, living off the land.", [
            Option("Tell me about the secrets.", goto="secrets"),
            Option("Farewell.", goto=END),
        ])

        # Secrets branch - leads to quest
        tree.add_node("secrets", "The dungeon to the east... it goes deep. Very deep.", [
            Option("Can you help me explore?", goto="quest_offer", action=self._give_quest_action),
            Option("Interesting. Farewell.", goto=END),
        ])

        # Quest given
        tree.add_node("quest_offer", "Brave soul! Descend to depth 3 and return. I shall reward you.", [
            Option("I'll do it.", goto="quest_accepted"),
            Option("I'll think about it.", goto=END),
        ])

        tree.add_node("quest_accepted", "May the spirits guide you.", [
            Option("Farewell.", goto=END),
        ])

        # Quest completion (QuestGiver.start_dialogue handles routing here)
        tree.add_node("quest_complete",
            "You've done it! Here is your reward.",
            [Option("Thank you.", goto=END)]
        )

        return tree


class VillageElder(QuestGiver):
    """A village elder who gives a goblin slaying quest."""

    def __init__(self, x=-1, y=-1, render_tag=120, name="Village Elder"):
        self._custom_quest = GoblinSlayerQuest(target_count=5)
        super().__init__(x=x, y=y, render_tag=render_tag, name=name)
        self.quest = self._custom_quest

    def build_dialogue_tree(self) -> DialogueTree:
        tree = DialogueTree("greeting")

        # Greeting
        tree.add_node("greeting", "Welcome, adventurer. Our village is troubled.", [
            Option("What troubles you?", goto="explain_problem"),
            Option("I'm just passing through.", goto="passing_through"),
        ])

        # Passing through branch
        tree.add_node("passing_through", "Safe travels then, stranger.", [
            Option("Actually, tell me about your troubles.", goto="explain_problem"),
            Option("Farewell.", goto=END),
        ])

        # Problem explanation
        tree.add_node("explain_problem", "Goblins! They raid our farms and steal our livestock.", [
            Option("I can help with that.", goto="accept_quest", action=self._give_quest_action),
            Option("Not my problem.", goto="refuse_quest"),
        ])

        # Quest accepted
        tree.add_node("accept_quest", "Bless you! Slay 5 of those wretched creatures.", [
            Option("Consider it done.", goto=END),
        ])

        # Quest refused
        tree.add_node("refuse_quest", "I understand. Perhaps another hero will come.", [
            Option("Maybe I can help after all.", goto="accept_quest", action=self._give_quest_action),
            Option("Farewell.", goto=END),
        ])

        # Quest completion (QuestGiver.start_dialogue handles routing here)
        tree.add_node("quest_complete",
            "The goblin menace is ended! You have our eternal gratitude.",
            [Option("Happy to help.", goto=END)]
        )

        return tree


class WanderingTrader(NPC):
    """
    A trader NPC. Trading functionality placeholder for future implementation.
    """

    def __init__(self, x=-1, y=-1, render_tag=121, name="Wandering Trader"):
        super().__init__(x=x, y=y, render_tag=render_tag, name=name)
        self.options = ["Talk"]  # Trading disabled for now

    def build_dialogue_tree(self) -> DialogueTree:
        tree = DialogueTree("greeting")

        tree.add_node("greeting", "Wares for sale! ...Well, soon anyway.", [
            Option("What do you sell?", goto="no_wares"),
            Option("Nevermind.", goto=END),
        ])

        tree.add_node("no_wares", "Many things! But my cart broke down. Come back later.", [
            Option("I'll check back.", goto=END),
        ])

        return tree


class MysteriousStranger(NPC):
    """A mysterious NPC with cryptic dialogue."""

    def __init__(self, x=-1, y=-1, render_tag=122, name="Mysterious Stranger"):
        super().__init__(x=x, y=y, render_tag=render_tag, name=name)

    def build_dialogue_tree(self) -> DialogueTree:
        tree = DialogueTree("silent")

        tree.add_node("silent", "...", [
            Option("Hello?", goto="warning"),
            Option("(Leave them alone)", goto=END),
        ])

        tree.add_node("warning", "The shadows grow longer. Be wary.", [
            Option("What do you mean?", goto="cryptic"),
            Option("...Okay.", goto=END),
        ])

        tree.add_node("cryptic", "You will understand... in time.", [
            Option("(Nod slowly)", goto=END),
        ])

        return tree
