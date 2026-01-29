from loop_workflow import *

def get_closest_monster(loop):
    player = loop.player
    monsterID = loop.generator.monster_map.dict
    tile_map = loop.generator.tile_map
    closest_dist = 100000
    closest_monster = player
    for monster_key in monsterID.subjects:
        monster = monsterID.get_subject(monster_key)
        dist = player.get_distance(monster.x, monster.y)

        if dist < closest_dist and tile_map.get_entity(monster.x, monster.y).get_visible():
            closest_dist = dist
            closest_monster = monster
    return closest_monster
