from .interactables import Interactable
from logging_config import get_logger
from src.core.enums import LoopType

logger = get_logger(__name__)

class CraftingTable(Interactable):
    def __init__(self, render_tag = 800, x=-1, y = -1, name="Crafting"):  # should be closed door
        super().__init__(x, y,render_tag, name=name)
        self.description = "Make Potions"

    def interact(self, loop):
        logger.debug("Player interacting with crafting table")
        print("Table!")
        loop.change_loop(LoopType.crafting)