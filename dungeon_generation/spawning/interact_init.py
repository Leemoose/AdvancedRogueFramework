from interactable_implementation import *
from .spawn_params import InteractableSpawnParams

InteractableSpawns = []
InteractableSpawns.append(InteractableSpawnParams(HealthFountain(), minFloor=1, maxFloor=5,branch = "all"))
InteractableSpawns.append(InteractableSpawnParams(Statue(), minFloor=1, maxFloor=5,branch = "all"))
# InteractableSpawns.append(InteractableSpawnParams(Campfire(), minFloor=1, maxFloor=5,branch = "Forest"))
# InteractableSpawns.append(InteractableSpawnParams(ForestOrbPedastool(), minFloor=5, maxFloor=5,branch = "Forest"))
#
# InteractableSpawns.append(InteractableSpawnParams(ForestHermit(), minFloor=1, maxFloor=1,branch = "Forest"))
# InteractableSpawns.append(InteractableSpawnParams(YellowPlant(), minFloor=1, maxFloor=5,branch = "Forest"))
#
#
# InteractableSpawns.append(InteractableSpawnParams(OceanOrbPedastool(), minFloor=5, maxFloor=5,branch = "Ocean"))