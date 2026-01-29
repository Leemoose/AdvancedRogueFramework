from logging_config import get_logger
import random

logger = get_logger(__name__)

class School():
    def __init__(self):
        self.level = {}

    def random_spell(self):
        return self.level[random.randint(1,len(self.level))]

    def level_spell(self, num):
        if num in self.level:
            return self.level[num]
        else:
            logger.warning("You attempted to get a level %s spell but there are only %s levels in this spell school", num, len(self.level))
            return False
