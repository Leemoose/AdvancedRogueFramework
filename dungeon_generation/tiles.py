from objects import Objects 

class Tile(Objects):
    def __init__(self, x, y, render_tag=0, passable=False, blocks_vision=True, id_tag=0, walkable=False):
        super().__init__(x, y, id_tag, render_tag, "Tile")
        self.passable = passable
        self.blocks_vision = blocks_vision
        self.walkable = walkable
        self.seen = False
        self.visible = False
        self.terrain = []
        self.elevation = 0

    def get_visible(self):
        return self.visible

    def set_seen(self, seen):
        self.seen = seen

    def get_seen(self):
        return self.seen

    def get_terrain(self):
        return self.terrain

    def get_terrain_message(self):
        message = []
        if len(self.terrain) > 0:
            for terrain in self.terrain:
                message.append(terrain.get_terrain_message())
        return message

    def get_elevation(self):
        return self.elevation

    def is_passable(self, entity=None):
        """Check if tile is passable, including deep water check."""
        if not self.passable:
            return False
        # Check if deep water terrain blocks passage
        for terrain in self.get_terrain():
            if not terrain.is_passable(entity):
                return False
        return True

    def is_blocking_vision(self, origin = None):
        for terrain in self.terrain:
            if terrain.is_blocking_vision(origin):
                return True
        return self.blocks_vision

    def add_terrain(self, terrain):
        terrain.set_location(self.get_x(), self.get_y())
        self.terrain.append(terrain)

    def has_terrain(self):
        return len(self.terrain) > 0

    def apply_terrain_effects(self, entity):
        for terrain_mod in self.terrain:
            terrain_mod.apply_effects(entity)

    def remove_terrain(self, trait):
        """Remove all of a specific terrain from this tile."""
        self.terrain = [t for t in self.terrain if not t.traits.get(trait, False)]

    def __str__(self):
        if self.passable:
            return (".")
        else:
            return ("#")


class Floor(Tile):
    def __init__(self, x, y, render_tag = 100, passable = True, blocks_vision = False, id_tag = 0):  # 195 = NEW_FANTASY_FLOOR (see asset_registry.py)
        super().__init__(x, y,  render_tag = render_tag, passable = passable, id_tag = id_tag, blocks_vision=blocks_vision)
        self.traits["floor"] = True

class Door(Floor):
    def __init__(self, x, y, render_tag = 320, passable = True, blocks_vision = True, id_tag = 0):  # 320 = NEW_FANTASY_DOOR_CLOSED (see asset_registry.py)
        super().__init__(x, y,  render_tag = render_tag, passable = passable, id_tag = id_tag, blocks_vision=blocks_vision)

    def open(self):
        self.render_tag = 321  # 321 = NEW_FANTASY_DOOR_OPEN (see asset_registry.py)
        self.blocks_vision = False

class Wall(Tile):
    def __init__(self, x, y, render_tag = 200, passable = False, blocks_vision = True, id_tag = 0):  # 250 = NEW_FANTASY_WALL (see asset_registry.py)
        super().__init__(x, y,  render_tag = render_tag, passable = passable, blocks_vision = blocks_vision, id_tag = id_tag)
        self.traits["wall"] = True

class Stairs(Tile):
    def __init__(self, x, y, render_tag = 0, passable = True, id_tag = 0):
        super().__init__(x, y, render_tag, passable, id_tag)
        self.stairs = True
        self.pair = None
        self.level_change = 0
        self.traits["stairs"] = True

    def pair_stairs(self, other_stairs):
        self.pair = other_stairs
        other_stairs.pair = self

    def get_paired_stairs(self):
        return self.pair

    def get_has_paired_stairs(self):
        return self.pair is not None

    def get_level_change(self):
        return self.level_change


class DownStairs(Stairs):
    def __init__(self, x, y, render_tag = 410, passable = True, id_tag = 0):  # 431 = NEW_FANTASY_STAIRS_DOWN (see asset_registry.py)
        super().__init__(x, y, render_tag = render_tag, passable = passable, id_tag = id_tag)
        self.level_change = 1

class UpStairs(Stairs):
    def __init__(self, x, y, render_tag = 400, passable = True, id_tag = 0):  # 430 = NEW_FANTASY_STAIRS_UP (see asset_registry.py)
        super().__init__(x, y, render_tag = render_tag, passable = passable, id_tag = id_tag)
        self.level_change = -1

class Gateway(Tile):
    #Bug: for some reason this tile is blocking vision
    def __init__(self, x, y, level = 1, branch = "Dungeon", render_tag = 420, passable = True, blocks_vision = False, id_tag = 0):  # 432 = NEW_FANTASY_PORTAL (see asset_registry.py)
        super().__init__(x, y, render_tag = render_tag, passable = passable, id_tag = id_tag)
        self.branch = branch
        self.level = level
        self.outgoing = None
        self.incoming = None
        self.traits["gateway"] = True

    def relocate(self, branch, level):
        self.branch = branch
        self.level = level
    def get_branch(self):
        return self.branch

    def get_depth(self):
        return self.level

    def pair_gateway(self, other_gateway):
        self.outgoing = other_gateway
        other_gateway.incoming = self

    def has_outgoing(self):
        return self.outgoing is not None

    def has_incoming(self):
        return self.incoming is not None
