from pygame import image
import pygame


class TileDict():
    def __init__(self, textSize):
        tiles = {}
        # 1-99 are tile
        tiles[0] = image.load("assets/placeholder.png")
        tiles[1] = pygame.transform.scale(image.load("assets/tiles/colorful_wall.png"), (32, 32))
        tiles[-1] = pygame.transform.scale(image.load("assets/tiles/colorful_wall_shaded.png"), (32, 32))
        tiles[2] = pygame.transform.scale(image.load("assets/tiles/colorful_floor.png"), (32, 32))
        tiles[-2] = pygame.transform.scale(image.load("assets/tiles/colorful_floor_shaded.png"), (32, 32))
        tiles[3] = pygame.transform.scale(image.load("assets/tiles/floor_dirty.png"), (32, 32))
        tiles[-3] = pygame.transform.scale(image.load("assets/tiles/floor_dirty_shaded.png"), (32, 32))
        tiles[4] = pygame.transform.scale(image.load("assets/tiles/floor_dirty1.png"), (32, 32))
        tiles[-4] = pygame.transform.scale(image.load("assets/tiles/floor_dirty1_shaded.png"), (32, 32))
        tiles[5] = image.load("assets/tiles/red_carpet.png")
        tiles[-5] = image.load("assets/tiles/red_carpet_shaded.png")
        tiles[6] = image.load("assets/tiles/wooden_floor.png")
        tiles[-6] = image.load("assets/tiles/wooden_floor_shaded.png")
        tiles[7] = image.load("assets/tiles/forest_wall.png")
        tiles[-7] = image.load("assets/tiles/forest_wall_shaded.png")
        tiles[8] = image.load("assets/tiles/ocean_floor.png")
        tiles[-8] = image.load("assets/tiles/ocean_floor_shaded.png")
        tiles[9] = image.load("assets/tiles/sand_floor.png")
        tiles[-9] = image.load("assets/tiles/sand_floor_shaded.png")
        tiles[10] = image.load("assets/tiles/deep_ocean_floor.png")
        tiles[-10] = image.load("assets/tiles/deep_ocean_floor_shaded.png")


        tiles[11] = pygame.transform.scale(image.load("assets/tiles/wall_extra_rounded.png"), (32, 32))
        tiles[-11] = pygame.transform.scale(image.load("assets/tiles/wall_extra_rounded_shaded.png"), (32, 32))
        tiles[12] = pygame.transform.scale(image.load("assets/tiles/floor_rounded.png"), (32, 32))
        tiles[-12] = pygame.transform.scale(image.load("assets/tiles/floor_rounded_shaded.png"), (32, 32))
        tiles[13] = image.load("assets/tiles/forest_floor.png")
        tiles[-13] = image.load("assets/tiles/forest_floor_shaded.png")
        tiles[14] = image.load("assets/tiles/ocean_wall.png")
        tiles[-14] = image.load("assets/tiles/ocean_wall_shaded.png")
        tiles[15] = image.load("assets/tiles/stone_floor.png")
        tiles[-15] = image.load("assets/tiles/stone_floor_shaded.png")

        tiles[20] = pygame.transform.scale(image.load("assets/fire.png"), (32, 32))

        tiles[30] = image.load("assets/tiles/door.png")
        tiles[-30] = image.load("assets/tiles/door_shaded.png")
        tiles[31] = image.load("assets/tiles/open_door.png")
        tiles[-31] = image.load("assets/tiles/open_door_shaded.png")

        # ui assets
        tiles[50] = image.load("assets/ui/stat_up.png")
        tiles[51] = image.load("assets/ui/stat_down.png")
        tiles[-50] = image.load("assets/ui/stat_up_dark.png")
        tiles[-51] = image.load("assets/ui/stat_down_dark.png")

        # basic assets
        tiles[90] = image.load("assets/tiles/stairs_up.png")
        tiles[-90] = image.load("assets/tiles/stairs_up_shaded.png")
        tiles[91] = image.load("assets/tiles/stairs_down.png")
        tiles[-91] = image.load("assets/tiles/stairs_down_shaded.png")
        tiles[92] = image.load("assets/tiles/gateway.png")
        tiles[-92] = image.load("assets/tiles/gateway_shaded.png")

        # pants
        tiles[100] = image.load("assets/items/armor/pants.png")

        # npc assets
        tiles[110] = image.load("assets/npc/shopkeeper.png")
        tiles[120] = image.load("assets/npc/king.png")
        tiles[121] = image.load("assets/npc/guard.png")
        tiles[122] = image.load("assets/npc/speech_bubble.png")
        tiles[123] = image.load("assets/npc/sensei.png")
        tiles[124] = image.load("assets/npc/training_dummy.png")
        tiles[125] = image.load("assets/npc/destroyed_dummy.png")
        tiles[126] = image.load("assets/npc/archmage.png")

        # 200-299 player assets
        tiles[200] = image.load("assets/player/Player.png")
        tiles[-200] = image.load("assets/player/player_under_armor.png")
        tiles[201] = image.load("assets/player/player_boots.png")
        tiles[202] = image.load("assets/player/player_gloves.png")
        tiles[203] = image.load("assets/player/player_helmet.png")
        tiles[204] = image.load("assets/player/player_armor.png")
        tiles[210] = image.load("assets/items/gold.png")

        # 300-399 weapon assets
        tiles[300] = image.load("assets/items/weapons/basic_ax.png")
        tiles[303] = image.load("assets/items/weapons/bleeding_ax.png")
        tiles[301] = image.load("assets/items/weapons/hammer.png")
        tiles[302] = image.load("assets/items/weapons/crushing_hammer.png")
        tiles[321] = image.load("assets/items/weapons/dagger.png")
        tiles[322] = image.load("assets/items/weapons/screaming_dagger.png")
        tiles[331] = image.load("assets/items/weapons/burning_sword.png")
        tiles[332] = image.load("assets/items/weapons/magic_wand.png")
        tiles[340] = image.load("assets/items/weapons/sword.png")
        tiles[341] = image.load("assets/items/weapons/sleeping_sword.png")
        tiles[351] = image.load("assets/items/weapons/bow.png")

        # shield assets
        # list of shields: basic, aegis, tower, magic focus
        tiles[311] = image.load("assets/items/armor/shield.png")
        tiles[312] = image.load("assets/items/armor/aegis.png")
        tiles[313] = image.load("assets/items/armor/tower_shield.png")
        tiles[314] = image.load("assets/items/armor/magic_focus.png")

        # 400-499 consumeables assets
        tiles[401] = image.load("assets/items/consumeables/health_orb_bigger.png")
        tiles[402] = image.load("assets/items/consumeables/mana_orb_bigger.png")
        tiles[403] = image.load("assets/items/consumeables/curing_orb_bigger.png")
        tiles[404] = image.load("assets/items/consumeables/might_orb_bigger.png")
        tiles[405] = image.load("assets/items/consumeables/haste_orb_bigger.png")

        # scroll assets
        tiles[450] = image.load("assets/items/consumeables/scroll.png")

        tiles[480] = image.load("assets/items/consumeables/book.png")

        # ring assets
        tiles[500] = image.load("assets/items/jewelry/green_ring_gold.png")
        tiles[501] = image.load("assets/items/jewelry/blood_ring.png")
        tiles[502] = image.load("assets/items/jewelry/blue_ring.png")
        tiles[503] = image.load("assets/items/jewelry/red_ring.png")
        tiles[504] = image.load("assets/items/jewelry/bone_ring.png")
        tiles[505] = image.load("assets/items/jewelry/ring_of_teleport.png")

        # amulet
        tiles[550] = image.load("assets/items/jewelry/amulet.png")

        # armor assets
        # list of armor: basic, leather, golden, warmonger, wizard robe
        tiles[600] = image.load("assets/items/armor/armor.png")
        tiles[601] = image.load("assets/items/armor/leather_armor.png")
        tiles[602] = image.load("assets/items/armor/golden_armor.png")
        tiles[603] = image.load("assets/items/armor/warmonger_armor.png")
        tiles[604] = image.load("assets/items/armor/wizard_robe.png")
        tiles[605] = image.load("assets/items/armor/karate_gi.png")
        tiles[606] = image.load("assets/items/armor/bloodstained_armor.png")


        # boots assets
        # list of boots: basic, escape
        tiles[700] = image.load("assets/items/armor/boots.png")
        tiles[701] = image.load("assets/items/armor/boots_of_escape.png")
        tiles[702] = image.load("assets/items/armor/blackened_boots.png")
        tiles[703] = image.load("assets/items/armor/assassin_boots.png")
 
        # gloves assets
        # list of gloves: basic, gauntlets
        tiles[750] = image.load("assets/items/armor/gloves.png")
        tiles[751] = image.load("assets/items/armor/gauntlets.png")
        tiles[752] = image.load("assets/items/armor/boxing_gloves.png")
        tiles[753] = image.load("assets/items/armor/healer_gloves.png")
        tiles[754] = image.load("assets/items/armor/lich_hand.png")

        # helmet assets
        tiles[770] = image.load("assets/items/armor/helmet.png")
        tiles[771] = image.load("assets/items/armor/viking_helmet.png")
        tiles[772] = image.load("assets/items/armor/spartan_helmet.png")
        tiles[773] = image.load("assets/items/armor/great_helm.png")
        tiles[774] = image.load("assets/items/armor/thief_hood.png")
        tiles[775] = image.load("assets/items/armor/wizard_hat.png")

        # empty equipment assets
        tiles[801] = image.load("assets/items/icons/empty_armor.png")
        tiles[802] = image.load("assets/items/icons/empty_boots.png")
        tiles[803] = image.load("assets/items/icons/empty_gloves.png")
        tiles[804] = image.load("assets/items/icons/empty_helmet.png")
        tiles[805] = image.load("assets/items/icons/empty_weapon.png")
        tiles[806] = image.load("assets/items/icons/empty_shield.png")
        tiles[807] = image.load("assets/items/icons/empty_ring.png")
        tiles[811] = image.load("assets/items/icons/empty_armor_open.png")
        tiles[812] = image.load("assets/items/icons/empty_boots_open.png")
        tiles[813] = image.load("assets/items/icons/empty_gloves_open.png")
        tiles[814] = image.load("assets/items/icons/empty_helmet_open.png")
        tiles[815] = image.load("assets/items/icons/empty_weapon_open.png")
        tiles[816] = image.load("assets/items/icons/empty_shield_open.png")
        tiles[817] = image.load("assets/items/icons/empty_ring_open.png")
        tiles[818] = image.load("assets/items/icons/empty_pants_open.png")
        tiles[819] = image.load("assets/items/icons/empty_pants.png")
        tiles[820] = image.load("assets/items/icons/empty_amulet_open.png")
        tiles[821] = image.load("assets/items/icons/empty_amulet.png")

        # skill assets
        tiles[901] = image.load("assets/ui/target.png")
        tiles[902] = image.load("assets/skills/placeholder_skill_icon.png")
        tiles[-902] = image.load("assets/skills/placeholder_skill_icon.png")
        tiles[903] = image.load("assets/skills/gun_skill_icon.png")
        tiles[-903] = image.load("assets/skills/gun_skill_icon.png")
        tiles[904] = image.load("assets/skills/BurningAttack_skill_icon.png")
        tiles[-904] = image.load("assets/skills/BurningAttack_skill_icon_dark.png")
        tiles[905] = image.load("assets/skills/MagicMissile_skill_icon.png")
        tiles[-905] = image.load("assets/skills/MagicMissile_skill_icon_dark.png")
        tiles[906] = image.load("assets/skills/Petrify_skill_icon.png")
        tiles[-906] = image.load("assets/skills/Petrify_skill_icon_dark.png")
        tiles[907] = image.load("assets/skills/ShrugOff_skill_icon.png")
        tiles[-907] = image.load("assets/skills/ShrugOff_skill_icon_dark.png")
        tiles[908] = image.load("assets/skills/Berserk_skill_icon.png")
        tiles[-908] = image.load("assets/skills/Berserk_skill_icon_dark.png")
        tiles[909] = image.load("assets/skills/BloodPact_skill_icon.png")
        tiles[-909] = image.load("assets/skills/BloodPact_skill_icon_dark.png")
        tiles[910] = image.load("assets/skills/Terrify_skill_icon.png")
        tiles[-910] = image.load("assets/skills/Terrify_skill_icon_dark.png")
        tiles[911] = image.load("assets/skills/Escape_skill_icon.png")
        tiles[-911] = image.load("assets/skills/Escape_skill_icon_dark.png")
        tiles[912] = image.load("assets/skills/Heal_skill_icon.png")
        tiles[-912] = image.load("assets/skills/Heal_skill_icon_dark.png")
        tiles[913] = image.load("assets/skills/Torment_skill_icon.png")
        tiles[-913] = image.load("assets/skills/Torment_skill_icon_dark.png")
        tiles[914] = image.load("assets/skills/teleport_skill_icon.png")
        tiles[-914] = image.load("assets/skills/teleport_skill_icon_dark.png")
        tiles[915] = image.load("assets/skills/invincible_skill_icon.png")
        tiles[-915] = image.load("assets/skills/invincible_skill_icon_dark.png")

        # monster assets 
        # dungeon monsters (10xx)
        # 1000-1999 monster assets

        tiles[1000] = image.load('assets/crawl-tiles/dc-mon/brown_ooze.png')
        tiles[1010] = image.load('assets/crawl-tiles/dc-mon/goblin.png')
        tiles[1020] = image.load('assets/crawl-tiles/dc-mon/kobold.png')
        tiles[1030] = image.load('assets/crawl-tiles/dc-mon/orc_knight.png')
        tiles[1040] = image.load('assets/crawl-tiles/dc-mon/animals/jumping_spider.png')

        tiles[1050] = image.load('assets/crawl-tiles/dc-mon/undead/skeletons/skeleton_humanoid_large.png')
        tiles[1051] = image.load('assets/crawl-tiles/dc-mon/undead/skeletons/skeleton_centaur.png')


        #2000-2999 all tiles assets
        tiles[2000] = image.load('assets/crawl-tiles/dc-dngn/floor/cobble_blood1.png')

        tiles[2100] = image.load('assets/crawl-tiles/dc-dngn/wall/stone_dark1.png')

        tiles[2200] = image.load('assets/crawl-tiles/dc-dngn/dngn_trap_zot.png')

        #3000 -4999 all items assets
        tiles[3000] = image.load('assets/crawl-tiles/item/armour/leather_armour1.png')

        tiles[3100] = image.load('assets/crawl-tiles/item/armour/glove1.png')

        tiles[3200] = image.load('assets/crawl-tiles/item/armour/headgear/helmet3.png')

        tiles[3300] = image.load('assets/items/armor/pants.png')

        tiles[3400] = image.load('assets/crawl-tiles/item/armour/shields/buckler1.png')

        tiles[3500] = image.load('assets/crawl-tiles/item/ring/gold_red.png')

        tiles[3600] = image.load('assets/crawl-tiles/item/amulet/bone_gray.png')

        tiles[3700] = image.load('assets/crawl-tiles/item/potion/ruby.png')




        #Items 4000+
        tiles[4000] = image.load("assets/items/orbs/forest_orb.png")
        tiles[4010] = image.load("assets/items/orbs/ocean_orb.png")

        tiles[4200] = image.load("assets/items/consumeables/yello_flower_petal.png")

        tiles[4300] = image.load('assets/crawl-tiles/item/scroll/scroll.png')

        tiles[4400] = image.load('assets/items/weapons/bow.png')

        tiles[4500] = image.load('assets/crawl-tiles/item/weapon/spear2.png')

        tiles[4600] = image.load('assets/crawl-tiles/item/weapon/war_axe1.png')

        tiles[4700] = image.load('assets/crawl-tiles/item/weapon/hammer1.png')

        tiles[4800] = image.load('assets/crawl-tiles/item/weapon/long_sword1.png')

        tiles[4900] = image.load('assets/crawl-tiles/item/weapon/dagger.png')


        #Player assets 5000
        tiles[5000] = image.load('assets/crawl-tiles/player/base/human_m.png')
        tiles[5100] = image.load('assets/crawl-tiles/player/gloves/glove_black.png')
        tiles[5200] = image.load('assets/crawl-tiles/player/boots/middle_brown.png')
        tiles[5300] = image.load('assets/crawl-tiles/player/head/cap_black1.png')
        tiles[5400] = image.load('assets/crawl-tiles/player/body/aragorn.png')
        tiles[5500] = image.load('assets/crawl-tiles/player/legs/pants_blue.png')

        #Interactables 6000
        tiles[6000] = image.load('assets/crawl-tiles/dc-dngn/dngn_blood_fountain2.png')
        tiles[6010] = image.load('assets/crawl-tiles/dc-dngn/dngn_dry_fountain.png')
        tiles[6100] = image.load('assets/crawl-tiles/dc-dngn/dngn_orcish_idol.png')


        #UI
        tiles[9000] = image.load('assets/UI/buttonStock1d.png')

        self.tiles = tiles

    def tile_string(self, key):
        return self.tiles[key]

