"""
Static Configurations - Asset Loading
=====================================

This file loads all game assets (sprites, tiles, icons) into a dictionary
keyed by tile IDs. The IDs follow the numbering scheme defined in
src/core/asset_registry.py.

See asset_registry.py for the complete ID reference and guidelines for
adding new assets.

ID RANGE QUICK REFERENCE:
-------------------------
0-999       Environment (floors, walls, doors, stairs, effects, traps, interactables)
1000-1999   Characters (player, NPCs, gold)
2000-2999   Monsters
3000-3999   Weapons
4000-4999   Armor
5000-5999   Accessories
6000-6999   Consumables
7000-7999   Special Items
8000-8999   UI - Equipment Slots
9000-9999   UI - Skills and Misc
"""

from pygame import image
import pygame

from src.core.constants import TILE_SIZE


class TileDict():
    """
    Loads and stores all game tile assets.

    Each tile is stored with its ID as the key. Fog-of-war shading is applied
    programmatically via pygame blending in display.py, so no shaded tile
    assets are needed.
    """

    def __init__(self, textSize):
        tiles = {}

        # ======================================================================
        # ENVIRONMENT (0-999)
        # ======================================================================

        # ----------------------------------------------------------------------
        # System/Placeholder (0-99)
        # ----------------------------------------------------------------------
        tiles[0] = image.load("assets/placeholder.png")

        # ----------------------------------------------------------------------
        # Floors (100-199)
        # 100-103=grass variants, 104-107=path variants,
        # 110=dirty, 120=carpet, 130=wood, 140=stone,
        # 150=forest, 160=sand, 170=ocean, 180=blood, 190=rounded
        # ----------------------------------------------------------------------
        tiles[100] = pygame.transform.scale(image.load("assets/tiles/tile_grass_1.png"), (TILE_SIZE, TILE_SIZE))
        tiles[101] = pygame.transform.scale(image.load("assets/tiles/tile_grass_2.png"), (TILE_SIZE, TILE_SIZE))
        tiles[102] = pygame.transform.scale(image.load("assets/tiles/tile_grass_3.png"), (TILE_SIZE, TILE_SIZE))
        tiles[103] = pygame.transform.scale(image.load("assets/tiles/tile_grass_4.png"), (TILE_SIZE, TILE_SIZE))
        tiles[104] = pygame.transform.scale(image.load("assets/tiles/tile_path_1.png"), (TILE_SIZE, TILE_SIZE))
        tiles[105] = pygame.transform.scale(image.load("assets/tiles/tile_path_2.png"), (TILE_SIZE, TILE_SIZE))
        tiles[106] = pygame.transform.scale(image.load("assets/tiles/tile_path_3.png"), (TILE_SIZE, TILE_SIZE))
        tiles[107] = pygame.transform.scale(image.load("assets/tiles/tile_path_4.png"), (TILE_SIZE, TILE_SIZE))
        tiles[110] = pygame.transform.scale(image.load("assets/tiles/floor_dirty.png"), (TILE_SIZE, TILE_SIZE))
        tiles[111] = pygame.transform.scale(image.load("assets/tiles/floor_dirty1.png"), (TILE_SIZE, TILE_SIZE))
        tiles[120] = image.load("assets/tiles/red_carpet.png")
        tiles[130] = image.load("assets/tiles/wooden_floor.png")
        tiles[140] = image.load("assets/tiles/stone_floor.png")
        tiles[150] = image.load("assets/tiles/forest_floor.png")
        tiles[151] = pygame.transform.scale(image.load("assets/tiles/dense_forest_floor.png"), (TILE_SIZE, TILE_SIZE))
        tiles[160] = image.load("assets/tiles/sand_floor.png")
        tiles[170] = image.load("assets/tiles/ocean_floor.png")
        tiles[171] = image.load("assets/tiles/deep_ocean_floor.png")
        tiles[180] = image.load('assets/crawl-tiles/dc-dngn/floor/cobble_blood1.png')
        tiles[190] = pygame.transform.scale(image.load("assets/tiles/floor_rounded.png"), (TILE_SIZE, TILE_SIZE))
        tiles[195] = pygame.transform.scale(image.load("assets/tiles/new_floor.png"), (TILE_SIZE, TILE_SIZE))

        # ----------------------------------------------------------------------
        # Walls (200-299)
        # 200=colorful, 210=rounded, 220=forest, 230=ocean, 240=stone
        # ----------------------------------------------------------------------
        tiles[200] = pygame.transform.scale(image.load("assets/tiles/tile_wall_modular.png"), (TILE_SIZE, TILE_SIZE))
        tiles[210] = pygame.transform.scale(image.load("assets/tiles/wall_extra_rounded.png"), (TILE_SIZE, TILE_SIZE))
        tiles[220] = image.load("assets/tiles/forest_wall.png")
        tiles[221] = pygame.transform.scale(image.load("assets/tiles/dense_forest_wall.png"), (TILE_SIZE, TILE_SIZE))
        tiles[230] = image.load("assets/tiles/ocean_wall.png")
        tiles[240] = image.load('assets/crawl-tiles/dc-dngn/wall/stone_dark1.png')
        tiles[250] = pygame.transform.scale(image.load("assets/tiles/new_wall.png"), (TILE_SIZE, TILE_SIZE))

        # ----------------------------------------------------------------------
        # Doors (300-399)
        # 300=closed, 301=open
        # ----------------------------------------------------------------------
        tiles[300] = pygame.transform.scale(image.load("assets/tiles/tile_door_closed.png"), (TILE_SIZE, TILE_SIZE))
        tiles[301] = pygame.transform.scale(image.load("assets/tiles/tile_door_open.png"), (TILE_SIZE, TILE_SIZE))
        tiles[320] = pygame.transform.scale(image.load("assets/tiles/new_door_closed.png"), (TILE_SIZE, TILE_SIZE))
        tiles[321] = pygame.transform.scale(image.load("assets/tiles/new_door_open.png"), (TILE_SIZE, TILE_SIZE))
        tiles[322] = pygame.transform.scale(image.load("assets/tiles/dense_forest_door_closed.png"), (TILE_SIZE, TILE_SIZE))
        tiles[323] = pygame.transform.scale(image.load("assets/tiles/dense_forest_door_open.png"), (TILE_SIZE, TILE_SIZE))

        # ----------------------------------------------------------------------
        # Stairs and Transitions (400-499)
        # 400=up, 410=down, 420=gateway
        # ----------------------------------------------------------------------
        tiles[400] = pygame.transform.scale(image.load("assets/tiles/tile_ladder_up.png"), (TILE_SIZE, TILE_SIZE))
        tiles[410] = pygame.transform.scale(image.load("assets/tiles/tile_ladder_down.png"), (TILE_SIZE, TILE_SIZE))
        tiles[420] = pygame.transform.scale(image.load("assets/tiles/tile_portal_transparent.png"), (TILE_SIZE, TILE_SIZE))
        tiles[430] = pygame.transform.scale(image.load("assets/tiles/new_stairs_up.png"), (TILE_SIZE, TILE_SIZE))
        tiles[431] = pygame.transform.scale(image.load("assets/tiles/new_stairs_down.png"), (TILE_SIZE, TILE_SIZE))
        tiles[432] = pygame.transform.scale(image.load("assets/tiles/new_portal.png"), (TILE_SIZE, TILE_SIZE))
        tiles[433] = pygame.transform.scale(image.load("assets/tiles/dense_forest_stairs_up.png"), (TILE_SIZE, TILE_SIZE))
        tiles[434] = pygame.transform.scale(image.load("assets/tiles/dense_forest_stairs_down.png"), (TILE_SIZE, TILE_SIZE))
        tiles[435] = pygame.transform.scale(image.load("assets/tiles/dense_forest_portal.png"), (TILE_SIZE, TILE_SIZE))

        # ----------------------------------------------------------------------
        # Effects (500-599)
        # 500=fire
        # ----------------------------------------------------------------------
        tiles[500] = pygame.transform.scale(image.load("assets/fire.png"), (TILE_SIZE, TILE_SIZE))

        # ----------------------------------------------------------------------
        # Traps (600-699)
        # 600=zot_trap
        # ----------------------------------------------------------------------
        tiles[600] = image.load('assets/crawl-tiles/dc-dngn/dngn_trap_zot.png')

        # ----------------------------------------------------------------------
        # Interactables (700-799)
        # 700=fountains, 710=idols, 720=campfires, 730=plants, 740=orb_pedestals
        # ----------------------------------------------------------------------
        tiles[700] = image.load('assets/crawl-tiles/dc-dngn/dngn_blood_fountain2.png')
        tiles[701] = image.load('assets/crawl-tiles/dc-dngn/dngn_dry_fountain.png')
        tiles[710] = image.load('assets/crawl-tiles/dc-dngn/dngn_orcish_idol.png')
        # Campfires - using fire effect as placeholder until proper campfire assets exist
        tiles[720] = pygame.transform.scale(image.load("assets/fire.png"), (TILE_SIZE, TILE_SIZE))  # CAMPFIRE
        tiles[721] = pygame.transform.scale(image.load("assets/fire.png"), (TILE_SIZE, TILE_SIZE))  # CAMPFIRE_BURNT (placeholder)
        # Plants
        tiles[730] = image.load("assets/items/consumeables/yello_flower_petal.png")  # YELLOW_PLANT (placeholder)
        # Orb pedestals - using orb icons as placeholders until proper pedestal assets exist
        tiles[740] = image.load("assets/items/orbs/forest_orb.png")  # FOREST_ORB_PEDESTAL (placeholder)
        tiles[741] = tiles[0]  # FOREST_ORB_PEDESTAL_EMPTY (placeholder)
        tiles[742] = image.load("assets/items/orbs/ocean_orb.png")  # OCEAN_ORB_PEDESTAL (placeholder)
        tiles[743] = tiles[0]  # OCEAN_ORB_PEDESTAL_EMPTY (placeholder)

        # ----------------------------------------------------------------------
        # Crafting (800-899)
        # ----------------------------------------------------------------------
        tiles[800] = image.load("assets/interactables/crafting_table.png") 

        # ======================================================================
        # CHARACTERS (1000-1999)
        # ======================================================================

        # ----------------------------------------------------------------------
        # Player Assets (1000-1099)
        # 1000=main, 1001=legacy, 1020+=overlays, 1030+=crawl overlays
        # ----------------------------------------------------------------------
        tiles[1000] = image.load('assets/crawl-tiles/player/base/human_m.png')
        tiles[1001] = image.load("assets/player/Player.png")
        tiles[-1000] = image.load("assets/player/player_under_armor.png")
        tiles[1020] = image.load("assets/player/player_boots.png")
        tiles[1021] = image.load("assets/player/player_gloves.png")
        tiles[1022] = image.load("assets/player/player_helmet.png")
        tiles[1023] = image.load("assets/player/player_armor.png")
        # Crawl-style player overlays
        tiles[1030] = image.load('assets/crawl-tiles/player/gloves/glove_black.png')
        tiles[1031] = image.load('assets/crawl-tiles/player/boots/middle_brown.png')
        tiles[1032] = image.load('assets/crawl-tiles/player/head/cap_black1.png')
        tiles[1033] = image.load('assets/crawl-tiles/player/body/aragorn.png')
        tiles[1034] = image.load('assets/crawl-tiles/player/legs/pants_blue.png')

        # ----------------------------------------------------------------------
        # NPCs (1100-1199)
        # ----------------------------------------------------------------------
        tiles[1100] = image.load("assets/npc/shopkeeper.png")
        tiles[1110] = image.load("assets/npc/king.png")
        tiles[1111] = image.load("assets/npc/guard.png")
        tiles[1120] = image.load("assets/npc/sensei.png")
        tiles[1121] = image.load("assets/npc/archmage.png")
        tiles[1122] = image.load("assets/npc/forest_hermit.png")
        tiles[1130] = image.load("assets/npc/training_dummy.png")
        tiles[1131] = image.load("assets/npc/destroyed_dummy.png")

        # ----------------------------------------------------------------------
        # Gold/Currency (1200-1299)
        # ----------------------------------------------------------------------
        tiles[1200] = image.load("assets/items/gold.png")

        # ======================================================================
        # MONSTERS (2000-2999)
        # ======================================================================

        # ----------------------------------------------------------------------
        # Oozes/Slimes (2000-2099)
        # ----------------------------------------------------------------------
        tiles[2000] = image.load('assets/crawl-tiles/dc-mon/brown_ooze.png')

        # ----------------------------------------------------------------------
        # Goblins (2100-2199)
        # ----------------------------------------------------------------------
        tiles[2100] = image.load('assets/crawl-tiles/dc-mon/goblin.png')

        # ----------------------------------------------------------------------
        # Kobolds (2200-2299)
        # ----------------------------------------------------------------------
        tiles[2200] = image.load('assets/crawl-tiles/dc-mon/kobold.png')

        # ----------------------------------------------------------------------
        # Orcs (2300-2399)
        # ----------------------------------------------------------------------
        tiles[2300] = image.load('assets/crawl-tiles/dc-mon/orc_knight.png')

        # ----------------------------------------------------------------------
        # Spiders (2400-2499)
        # ----------------------------------------------------------------------
        tiles[2400] = image.load('assets/crawl-tiles/dc-mon/animals/jumping_spider.png')

        # ----------------------------------------------------------------------
        # Undead (2500-2599)
        # ----------------------------------------------------------------------
        tiles[2500] = image.load('assets/crawl-tiles/dc-mon/undead/skeletons/skeleton_humanoid_large.png')
        tiles[2501] = image.load('assets/crawl-tiles/dc-mon/undead/skeletons/skeleton_centaur.png')

        # ======================================================================
        # WEAPONS (3000-3999)
        # ======================================================================

        # ----------------------------------------------------------------------
        # Swords (3000-3099)
        # ----------------------------------------------------------------------
        tiles[3000] = image.load("assets/items/weapons/sword.png")
        tiles[3001] = image.load("assets/items/weapons/sleeping_sword.png")
        tiles[3002] = image.load("assets/items/weapons/burning_sword.png")
        tiles[3010] = image.load('assets/crawl-tiles/item/weapon/long_sword1.png')

        # ----------------------------------------------------------------------
        # Axes (3100-3199)
        # ----------------------------------------------------------------------
        tiles[3100] = image.load("assets/items/weapons/basic_ax.png")
        tiles[3101] = image.load("assets/items/weapons/bleeding_ax.png")
        tiles[3110] = image.load('assets/crawl-tiles/item/weapon/war_axe1.png')

        # ----------------------------------------------------------------------
        # Hammers (3200-3299)
        # ----------------------------------------------------------------------
        tiles[3200] = image.load("assets/items/weapons/hammer.png")
        tiles[3201] = image.load("assets/items/weapons/crushing_hammer.png")
        tiles[3210] = image.load('assets/crawl-tiles/item/weapon/hammer1.png')

        # ----------------------------------------------------------------------
        # Daggers (3300-3399)
        # ----------------------------------------------------------------------
        tiles[3300] = image.load("assets/items/weapons/dagger.png")
        tiles[3301] = image.load("assets/items/weapons/screaming_dagger.png")
        tiles[3310] = image.load('assets/crawl-tiles/item/weapon/dagger.png')

        # ----------------------------------------------------------------------
        # Bows/Ranged (3400-3499)
        # ----------------------------------------------------------------------
        tiles[3400] = image.load("assets/items/weapons/bow.png")
        tiles[3401] = image.load('assets/items/weapons/bow.png')  # CRAWL_BOW uses same asset
        tiles[3410] = image.load('assets/crawl-tiles/item/weapon/spear2.png')

        # ----------------------------------------------------------------------
        # Wands/Staves (3500-3599)
        # ----------------------------------------------------------------------
        tiles[3500] = image.load("assets/items/weapons/magic_wand.png")
        tiles[3501] = image.load("assets/items/armor/magic_focus.png")

        # ----------------------------------------------------------------------
        # Shields (3600-3699)
        # ----------------------------------------------------------------------
        tiles[3600] = image.load("assets/items/armor/shield.png")
        tiles[3601] = image.load("assets/items/armor/aegis.png")
        tiles[3602] = image.load("assets/items/armor/tower_shield.png")
        tiles[3610] = image.load('assets/crawl-tiles/item/armour/shields/buckler1.png')

        # ======================================================================
        # ARMOR (4000-4999)
        # ======================================================================

        # ----------------------------------------------------------------------
        # Body Armor (4000-4099)
        # ----------------------------------------------------------------------
        tiles[4000] = image.load("assets/items/armor/armor.png")
        tiles[4001] = image.load("assets/items/armor/leather_armor.png")
        tiles[4002] = image.load("assets/items/armor/golden_armor.png")
        tiles[4003] = image.load("assets/items/armor/warmonger_armor.png")
        tiles[4004] = image.load("assets/items/armor/wizard_robe.png")
        tiles[4005] = image.load("assets/items/armor/karate_gi.png")
        tiles[4006] = image.load("assets/items/armor/bloodstained_armor.png")
        tiles[4010] = image.load('assets/crawl-tiles/item/armour/leather_armour1.png')

        # ----------------------------------------------------------------------
        # Helmets (4100-4199)
        # ----------------------------------------------------------------------
        tiles[4100] = image.load("assets/items/armor/helmet.png")
        tiles[4101] = image.load("assets/items/armor/viking_helmet.png")
        tiles[4102] = image.load("assets/items/armor/spartan_helmet.png")
        tiles[4103] = image.load("assets/items/armor/great_helm.png")
        tiles[4104] = image.load("assets/items/armor/thief_hood.png")
        tiles[4105] = image.load("assets/items/armor/wizard_hat.png")
        tiles[4110] = image.load('assets/crawl-tiles/item/armour/headgear/helmet3.png')

        # ----------------------------------------------------------------------
        # Gloves (4200-4299)
        # ----------------------------------------------------------------------
        tiles[4200] = image.load("assets/items/armor/gloves.png")
        tiles[4201] = image.load("assets/items/armor/gauntlets.png")
        tiles[4202] = image.load("assets/items/armor/boxing_gloves.png")
        tiles[4203] = image.load("assets/items/armor/healer_gloves.png")
        tiles[4204] = image.load("assets/items/armor/lich_hand.png")
        tiles[4210] = image.load('assets/crawl-tiles/item/armour/glove1.png')

        # ----------------------------------------------------------------------
        # Boots (4300-4399)
        # ----------------------------------------------------------------------
        tiles[4300] = image.load("assets/items/armor/boots.png")
        tiles[4301] = image.load("assets/items/armor/boots_of_escape.png")
        tiles[4302] = image.load("assets/items/armor/blackened_boots.png")
        tiles[4303] = image.load("assets/items/armor/assassin_boots.png")

        # ----------------------------------------------------------------------
        # Pants (4400-4499)
        # ----------------------------------------------------------------------
        tiles[4400] = image.load("assets/items/armor/pants.png")
        tiles[4401] = image.load('assets/items/armor/pants.png')  # CRAWL_PANTS uses same asset

        # ======================================================================
        # ACCESSORIES (5000-5999)
        # ======================================================================

        # ----------------------------------------------------------------------
        # Rings (5000-5099)
        # ----------------------------------------------------------------------
        tiles[5000] = image.load("assets/items/jewelry/green_ring_gold.png")
        tiles[5001] = image.load("assets/items/jewelry/blood_ring.png")
        tiles[5002] = image.load("assets/items/jewelry/blue_ring.png")
        tiles[5003] = image.load("assets/items/jewelry/red_ring.png")
        tiles[5004] = image.load("assets/items/jewelry/bone_ring.png")
        tiles[5005] = image.load("assets/items/jewelry/ring_of_teleport.png")
        tiles[5010] = image.load('assets/crawl-tiles/item/ring/gold_red.png')

        # ----------------------------------------------------------------------
        # Amulets (5100-5199)
        # ----------------------------------------------------------------------
        tiles[5100] = image.load("assets/items/jewelry/amulet.png")
        tiles[5110] = image.load('assets/crawl-tiles/item/amulet/bone_gray.png')

        # ======================================================================
        # CONSUMABLES (6000-6999)
        # ======================================================================

        # ----------------------------------------------------------------------
        # Potions/Orbs (6000-6099)
        # ----------------------------------------------------------------------
        tiles[6000] = image.load("assets/items/consumeables/health_orb_bigger.png")
        tiles[6001] = image.load("assets/items/consumeables/mana_orb_bigger.png")
        tiles[6002] = image.load("assets/items/consumeables/curing_orb_bigger.png")
        tiles[6003] = image.load("assets/items/consumeables/might_orb_bigger.png")
        tiles[6004] = image.load("assets/items/consumeables/haste_orb_bigger.png")
        tiles[6010] = image.load('assets/crawl-tiles/item/potion/ruby.png')

        # ----------------------------------------------------------------------
        # Scrolls (6100-6199)
        # ----------------------------------------------------------------------
        tiles[6100] = image.load("assets/items/consumeables/scroll.png")
        tiles[6110] = image.load('assets/crawl-tiles/item/scroll/scroll.png')

        # ----------------------------------------------------------------------
        # Books (6200-6299)
        # ----------------------------------------------------------------------
        tiles[6200] = image.load("assets/items/consumeables/book.png")

        # ----------------------------------------------------------------------
        # Special Consumables (6400-6499)
        # ----------------------------------------------------------------------
        tiles[6400] = image.load("assets/items/consumeables/yello_flower_petal.png")

        # ----------------------------------------------------------------------
        # Ingredients (6500-6599)
        # ----------------------------------------------------------------------
        tiles[6500] = image.load("assets/items/consumeables/Ingredients/fire_lily.png")
        tiles[6501] = image.load("assets/items/consumeables/Ingredients/rockvine.png")

        # ======================================================================
        # SPECIAL ITEMS (7000-7999)
        # ======================================================================

        # ----------------------------------------------------------------------
        # Key Orbs (7000-7099)
        # ----------------------------------------------------------------------
        tiles[7000] = image.load("assets/items/orbs/forest_orb.png")
        tiles[7001] = image.load("assets/items/orbs/ocean_orb.png")

        # ======================================================================
        # UI - EQUIPMENT SLOTS (8000-8999)
        # ======================================================================

        # ----------------------------------------------------------------------
        # Empty Slot Icons - Closed (8000-8099)
        # ----------------------------------------------------------------------
        tiles[8000] = image.load("assets/items/icons/empty_armor.png")
        tiles[8001] = image.load("assets/items/icons/empty_boots.png")
        tiles[8002] = image.load("assets/items/icons/empty_gloves.png")
        tiles[8003] = image.load("assets/items/icons/empty_helmet.png")
        tiles[8004] = image.load("assets/items/icons/empty_weapon.png")
        tiles[8005] = image.load("assets/items/icons/empty_shield.png")
        tiles[8006] = image.load("assets/items/icons/empty_ring.png")
        tiles[8007] = image.load("assets/items/icons/empty_pants.png")
        tiles[8008] = image.load("assets/items/icons/empty_amulet.png")

        # ----------------------------------------------------------------------
        # Empty Slot Icons - Open/Selected (8100-8199)
        # ----------------------------------------------------------------------
        tiles[8100] = image.load("assets/items/icons/empty_armor_open.png")
        tiles[8101] = image.load("assets/items/icons/empty_boots_open.png")
        tiles[8102] = image.load("assets/items/icons/empty_gloves_open.png")
        tiles[8103] = image.load("assets/items/icons/empty_helmet_open.png")
        tiles[8104] = image.load("assets/items/icons/empty_weapon_open.png")
        tiles[8105] = image.load("assets/items/icons/empty_shield_open.png")
        tiles[8106] = image.load("assets/items/icons/empty_ring_open.png")
        tiles[8107] = image.load("assets/items/icons/empty_pants_open.png")
        tiles[8108] = image.load("assets/items/icons/empty_amulet_open.png")

        # ======================================================================
        # UI - SKILLS AND MISC (9000-9999)
        # ======================================================================

        # ----------------------------------------------------------------------
        # System UI (9000-9099)
        # ----------------------------------------------------------------------
        tiles[9000] = image.load("assets/UI/target.png")
        tiles[9001] = image.load("assets/UI/stat_up.png")
        tiles[-9001] = image.load("assets/UI/stat_up_dark.png")
        tiles[9002] = image.load("assets/UI/stat_down.png")
        tiles[-9002] = image.load("assets/UI/stat_down_dark.png")

        # ----------------------------------------------------------------------
        # Attack Skills (9100-9199)
        # ----------------------------------------------------------------------
        tiles[9100] = image.load("assets/skills/placeholder_skill_icon.png")
        tiles[-9100] = image.load("assets/skills/placeholder_skill_icon.png")
        tiles[9101] = image.load("assets/skills/gun_skill_icon.png")
        tiles[-9101] = image.load("assets/skills/gun_skill_icon.png")
        tiles[9102] = image.load("assets/skills/BurningAttack_skill_icon.png")
        tiles[-9102] = image.load("assets/skills/BurningAttack_skill_icon_dark.png")
        tiles[9103] = image.load("assets/skills/MagicMissile_skill_icon.png")
        tiles[-9103] = image.load("assets/skills/MagicMissile_skill_icon_dark.png")

        # ----------------------------------------------------------------------
        # Defense Skills (9200-9299)
        # ----------------------------------------------------------------------
        tiles[9200] = image.load("assets/skills/ShrugOff_skill_icon.png")
        tiles[-9200] = image.load("assets/skills/ShrugOff_skill_icon_dark.png")
        tiles[9201] = image.load("assets/skills/invincible_skill_icon.png")
        tiles[-9201] = image.load("assets/skills/invincible_skill_icon_dark.png")

        # ----------------------------------------------------------------------
        # Buff Skills (9300-9399)
        # ----------------------------------------------------------------------
        tiles[9300] = image.load("assets/skills/Berserk_skill_icon.png")
        tiles[-9300] = image.load("assets/skills/Berserk_skill_icon_dark.png")
        tiles[9301] = image.load("assets/skills/BloodPact_skill_icon.png")
        tiles[-9301] = image.load("assets/skills/BloodPact_skill_icon_dark.png")

        # ----------------------------------------------------------------------
        # Utility Skills (9400-9499)
        # ----------------------------------------------------------------------
        tiles[9400] = image.load("assets/skills/Escape_skill_icon.png")
        tiles[-9400] = image.load("assets/skills/Escape_skill_icon_dark.png")
        tiles[9401] = image.load("assets/skills/teleport_skill_icon.png")
        tiles[-9401] = image.load("assets/skills/teleport_skill_icon_dark.png")

        # ----------------------------------------------------------------------
        # Heal Skills (9500-9599)
        # ----------------------------------------------------------------------
        tiles[9500] = image.load("assets/skills/heal_skill_icon.png")
        tiles[-9500] = image.load("assets/skills/heal_skill_icon_dark.png")

        # ----------------------------------------------------------------------
        # Debuff Skills (9600-9699)
        # ----------------------------------------------------------------------
        tiles[9600] = image.load("assets/skills/Petrify_skill_icon.png")
        tiles[-9600] = image.load("assets/skills/Petrify_skill_icon_dark.png")
        tiles[9601] = image.load("assets/skills/Terrify_skill_icon.png")
        tiles[-9601] = image.load("assets/skills/Terrify_skill_icon_dark.png")
        tiles[9602] = image.load("assets/skills/Torment_skill_icon.png")
        tiles[-9602] = image.load("assets/skills/Torment_skill_icon_dark.png")

        # ----------------------------------------------------------------------
        # Misc UI (9900-9999)
        # ----------------------------------------------------------------------
        tiles[9900] = image.load('assets/UI/buttonStock1d.png')
        tiles[9901] = image.load("assets/npc/speech_bubble.png")

        self.tiles = tiles

    def tile_string(self, key):
        return self.tiles[key]
