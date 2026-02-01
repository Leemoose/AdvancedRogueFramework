"""
Spatial query utilities for finding entities in the game world.

These functions were moved from loop_workflow/loop_utility.py to break
circular imports between display_generation and loop_workflow packages.
"""


def get_closest_monster(loop):
    """
    Find the closest visible monster to the player.

    Args:
        loop: The game loop object containing player and map data.

    Returns:
        The closest visible monster, or the player if no monsters are visible.
    """
    player = loop.player
    monster_map = loop.generator.monster_map.dict
    tile_map = loop.generator.tile_map
    closest_dist = 100000
    closest_monster = player

    for monster_key in monster_map.subjects:
        monster = monster_map.get_subject(monster_key)
        dist = player.get_distance(monster.x, monster.y)

        if dist < closest_dist and tile_map.get_entity(monster.x, monster.y).get_visible():
            closest_dist = dist
            closest_monster = monster

    return closest_monster
