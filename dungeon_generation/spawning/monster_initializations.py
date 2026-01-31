"""
Monster spawn configurations for dungeon generation.

Defines which monsters appear on which floors and in which branches.
"""

from monsters import (
    # Core monsters
    Ooze, Goblin, Kobold, Orc, Spider, Skeleton, SkeletonArcher,
    # New monsters
    Slime, GoblinShaman, Hobgoblin, Looter,
    Gargoyle, Minotaur, Golem, Raptor, Tormentorb, Dummy,
    Stumpy, Treant, MetallicBear, InsectNest, Hornet,
    # Water monsters (not spawned yet - water branch not implemented)
    # Squid, Leviathan, ChasmCrawler,
)

from .spawn_params import MonsterSpawnParams

MonsterSpawns = []

# =============================================================================
# EARLY FLOORS (1-4)
# =============================================================================

# Slimes and Oozes - floor 1-4
MonsterSpawns.append(MonsterSpawnParams(Slime(), group="slime", minFloor=1, maxFloor=4))
MonsterSpawns.append(MonsterSpawnParams(Ooze(), minFloor=1, maxFloor=5))

# Goblins and variants - floor 2-6
MonsterSpawns.append(MonsterSpawnParams(Goblin(), group="goblins", minFloor=2, maxFloor=6))
MonsterSpawns.append(MonsterSpawnParams(Looter(), group="goblins", minFloor=2, maxFloor=5, rarity="Rare"))

# =============================================================================
# MID FLOORS (4-7)
# =============================================================================

# Kobolds with fire magic - floor 3-7
MonsterSpawns.append(MonsterSpawnParams(Kobold(), minFloor=3, maxFloor=7))

# Orcs - floor 4-8
MonsterSpawns.append(MonsterSpawnParams(Orc(), minFloor=4, maxFloor=8))

# Goblin elites - floor 4-7
MonsterSpawns.append(MonsterSpawnParams(Hobgoblin(), group="goblins", minFloor=4, maxFloor=7, rarity="Uncommon"))
MonsterSpawns.append(MonsterSpawnParams(GoblinShaman(), group="goblins", minFloor=5, maxFloor=8, rarity="Rare"))

# Stone creatures - floor 5-8
MonsterSpawns.append(MonsterSpawnParams(Gargoyle(), group="gargoyle", minFloor=5, maxFloor=8))
MonsterSpawns.append(MonsterSpawnParams(Minotaur(), minFloor=5, maxFloor=8))

# =============================================================================
# LATE FLOORS (6-10)
# =============================================================================

# Undead - floor 5-10
MonsterSpawns.append(MonsterSpawnParams(Skeleton(), group='skeleton', minFloor=5, maxFloor=10))
MonsterSpawns.append(MonsterSpawnParams(SkeletonArcher(), group='skeleton', minFloor=5, maxFloor=10))

# Spiders - floor 6-10
MonsterSpawns.append(MonsterSpawnParams(Spider(), minFloor=6, maxFloor=10))

# Powerful late-game monsters - floor 8-10
MonsterSpawns.append(MonsterSpawnParams(Raptor(), group="dinosaur", minFloor=8, maxFloor=10))
MonsterSpawns.append(MonsterSpawnParams(Tormentorb(), minFloor=8, maxFloor=10, rarity="Rare"))
MonsterSpawns.append(MonsterSpawnParams(Golem(), minFloor=8, maxFloor=10))

# =============================================================================
# FOREST BRANCH (when implemented)
# =============================================================================

MonsterSpawns.append(MonsterSpawnParams(Stumpy(), minFloor=1, maxFloor=4, branch="Forest"))
MonsterSpawns.append(MonsterSpawnParams(Treant(), minFloor=3, maxFloor=6, branch="Forest"))
MonsterSpawns.append(MonsterSpawnParams(MetallicBear(), minFloor=4, maxFloor=7, branch="Forest", rarity="Rare"))
MonsterSpawns.append(MonsterSpawnParams(InsectNest(), minFloor=2, maxFloor=5, branch="Forest"))

# =============================================================================
# WATER BRANCH (not yet implemented)
# Water monsters have the water attribute but are not spawned until
# the water/ocean branch is implemented.
# =============================================================================

# MonsterSpawns.append(MonsterSpawnParams(Squid(), minFloor=1, maxFloor=3, branch="Ocean"))
# MonsterSpawns.append(MonsterSpawnParams(ChasmCrawler(), minFloor=2, maxFloor=5, branch="Ocean"))
# MonsterSpawns.append(MonsterSpawnParams(Leviathan(), minFloor=4, maxFloor=7, branch="Ocean", rarity="Rare"))

# =============================================================================
# SPECIAL / TESTING
# =============================================================================

# Training dummy - not spawned naturally, placed manually
# MonsterSpawns.append(MonsterSpawnParams(Dummy(), minFloor=1, maxFloor=1))
