from dungeon_generation.configuration_data import *
from display_generation import *
from loop_workflow import keyboard as K
import loops as L
import static_configs
from spell_system import initialize_spell_system
from tag_system import tag_manager as tags

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module = "PIL.PNGImagePlugin")

#..random.seed(420)
pygame.init()
pygame.font.init()

# Initialize the spell system (loads all spell data from YAML files)
initialize_spell_system()

# Initialize Tag system - adds default tag combos to test
tags.InitPotionTags()

# Quick test of the tag updates! Adding Fire, Water, and Stone - Fire + Water is higher prio so it should result in Steam, Stone
tagTest = [tags.PotionTag.Fire, tags.PotionTag.Water, tags.PotionTag.Stone]
tags.potionManager.ApplyCombos(tagTest);
print(tagTest)


#Size of tiles
textSize = 32
infoObject = pygame.display.Info()
width = infoObject.current_w #1920 * 4/5
height = infoObject.current_h #1080 * 4/5
textWidth = int(width / textSize)

textHeight = int(height / textSize)
#dictionary mapping renderID to the image
tileDict = static_configs.TileDict(textSize)
dungeonData = DungeonData()
#Responsible for game loops

display = Display(width, height, textSize, textWidth, textHeight)
keyboard = K.Keyboard()
loop = L.Loops(tileDict, display, keyboard, dungeonData)

player_turn = True
loop.init_game()
loop.change_loop(L.LoopType.main)

while player_turn:
    loop.render_screen(display)
    player_turn = loop.action_loop(keyboard, display)
