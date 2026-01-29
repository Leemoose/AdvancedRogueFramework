class statUpgrades():
    def __init__(self, base_str=0, max_str=0, base_dex=0, max_dex=0, base_int=0, max_int=0, base_end=0, max_end=0,
                 base_arm=0, max_arm=0):
        self.base_str = base_str
        self.max_str = max_str
        self.base_dex = base_dex
        self.max_dex = max_dex
        self.base_int = base_int
        self.max_int = max_int
        self.base_end = base_end
        self.max_end = max_end
        self.base_arm = base_arm
        self.max_arm = max_arm

    def intLerp(self, a, b, level):
        return (((b - a) * (level - 1)) // 5) + a

    def GetStatsForLevel(self, level):
        return (self.intLerp(self.base_str, self.max_str, level),
                self.intLerp(self.base_dex, self.max_dex, level),
                self.intLerp(self.base_int, self.max_int, level),
                self.intLerp(self.base_end, self.max_end, level),
                self.intLerp(self.base_arm, self.max_arm, level))

    def GetStatsForLevelUp(self, level):
        prev_level = self.GetStatsForLevel(level - 1)

        this_level = self.GetStatsForLevel(level)

        return tuple(map(lambda i, j: i - j, this_level, prev_level))

