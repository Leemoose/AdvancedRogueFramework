from interactable_implementation import *
from .spawn_params import InteractableSpawnParams

InteractableSpawns = []
InteractableSpawns.append(InteractableSpawnParams(HealthFountain(), minFloor=1, maxFloor=5, branch="all"))
InteractableSpawns.append(InteractableSpawnParams(Statue(), minFloor=1, maxFloor=5, branch="all"))

# NPCs - spawn in Hub and early dungeon floors
InteractableSpawns.append(InteractableSpawnParams(CraftingTable(), minFloor=1, maxFloor=10, branch="all"))
InteractableSpawns.append(InteractableSpawnParams(VillageElder(), minFloor=1, maxFloor=1, branch="Hub"))
InteractableSpawns.append(InteractableSpawnParams(ForestHermit(), minFloor=1, maxFloor=2, branch="Dungeon"))
InteractableSpawns.append(InteractableSpawnParams(WanderingTrader(), minFloor=2, maxFloor=4, branch="all"))
InteractableSpawns.append(InteractableSpawnParams(MysteriousStranger(), minFloor=3, maxFloor=5, branch="Dungeon"))

# Uncomment these for branch-specific content
# InteractableSpawns.append(InteractableSpawnParams(Campfire(), minFloor=1, maxFloor=5, branch="Forest"))
# InteractableSpawns.append(InteractableSpawnParams(ForestOrbPedastool(), minFloor=5, maxFloor=5, branch="Forest"))
InteractableSpawns.append(InteractableSpawnParams(YellowPlant(), minFloor=1, maxFloor=5, branch="Dungeon"))
# InteractableSpawns.append(InteractableSpawnParams(OceanOrbPedastool(), minFloor=5, maxFloor=5, branch="Ocean"))