# Core monsters
from .spiders import Spider
from .oozes import Ooze
from .kobolds import Kobold
from .orcs import Orc
from .undead import Skeleton, SkeletonArcher

# Goblin family
from .goblins import Goblin, GoblinShaman, Hobgoblin, Looter

# Slimes (different from oozes - picks up items instead of destroying)
from .slimes import Slime

# Stone/mythical creatures
from .gargoyles import Gargoyle
from .minotaurs import Minotaur
from .golems import Golem

# Fast predators
from .raptors import Raptor

# Magical creatures
from .orbs import Tormentorb

# Training/utility
from .dummies import Dummy

# Forest branch monsters
from .forest import Stumpy, Treant
from .bears import MetallicBear
from .insects import InsectNest, Hornet

# Water branch monsters (not yet in spawner - water branch not implemented)
from .water import Squid, Leviathan, ChasmCrawler
