from enum import Enum, auto
import bisect #Used to do sorted list inserts!  #Base values for enums! Add here to create more types

class PotionTag(Enum):
    Nothing = auto()

    #Base types!
    Fire = auto()
    Water = auto()
    Stone = auto()
    Air = auto()
    Vigor = auto()

    #Double stacks
    Inferno = auto() #Double Fire
    Flood = auto() #Double Water
    Mantle = auto() #Double Stone 
    Whirlwind = auto() #Double Air
    Heal = auto() #Double Vigor

    #True combos - Buff variants
    Rage = auto() #Vigor + Fire
    Regeneration = auto() #Vigor + Water 
    Strength = auto() #Vigor + Stone
    Haste = auto() #Vigor + Air

    #True combos - Non-buff
    Steam = auto() #Fire + Water
    Magma = auto() #Fire + Stone 
    Storm = auto() #Air + Water
    
    #Advanced combos (3 or more components)
    Lightning = auto() #Storm + Fire
    Scorch = auto() #Haste + Fire
    Teleport = auto() #Haste + Air

    def __str__(self):
        return self.name

    def __lt__(self, other):
        return self.value < other.value


class PotionCombo():
    def __init__(self, leftTag, rightTag, priority, outputs):
        self.m_leftTag = leftTag
        self.m_rightTag = rightTag
        self.m_priority = priority
        self.m_outputs = outputs

    #Match function that handles cases where a match is duplicates!
    def Matches(self, tagOne, tagTwo):
        oneLeft  = (tagOne == self.m_leftTag)
        oneRight = (tagOne == self.m_rightTag)
        twoLeft  = (tagTwo == self.m_leftTag)
        twoRight = (tagTwo == self.m_rightTag)
        return (oneLeft and twoRight) or (oneRight and twoLeft)

class PotionManager():
    combos = []
    
    def AddCombo(self, potionCombo):
        bisect.insort(self.combos, potionCombo, key=lambda x: -x.m_priority)

    def ApplyCombos(self, tags):
        anyMatches = True
        while (anyMatches):
            anyMatches = False
            for combo in self.combos:
                for i in range(len(tags)):
                    for j in range(i + 1, len(tags)):
                        tagOne = tags[i]
                        tagTwo = tags[j]

                        if (combo.Matches(tagOne, tagTwo)):
                            print("Combo found between " + str(tagOne) + " and " + str(tagTwo))
                            tags.pop(j)
                            tags.pop(i)
                            tags += combo.m_outputs
                            anyMatches = True
                            break
                    if (anyMatches):
                        break
                if (anyMatches):
                    break

potionManager = PotionManager()

def InitPotionTags():
	
    #Base combos - All low prio! Prefer more interesting combos
    potionManager.AddCombo(PotionCombo(PotionTag.Fire, PotionTag.Fire, -100.0, [PotionTag.Inferno]))
    potionManager.AddCombo(PotionCombo(PotionTag.Water, PotionTag.Water, -100.0, [PotionTag.Flood]))
    potionManager.AddCombo(PotionCombo(PotionTag.Stone, PotionTag.Stone, -100.0, [PotionTag.Mantle]))
    potionManager.AddCombo(PotionCombo(PotionTag.Air, PotionTag.Air, -100.0, [PotionTag.Whirlwind]))
    potionManager.AddCombo(PotionCombo(PotionTag.Vigor, PotionTag.Vigor, -100.0, [PotionTag.Heal]))

    #Buff potions - Vigor combos
    potionManager.AddCombo(PotionCombo(PotionTag.Fire, PotionTag.Vigor, 10.0, [PotionTag.Rage]))
    potionManager.AddCombo(PotionCombo(PotionTag.Water, PotionTag.Vigor, 10.0, [PotionTag.Regeneration]))
    potionManager.AddCombo(PotionCombo(PotionTag.Stone, PotionTag.Vigor, 10.0, [PotionTag.Strength]))
    potionManager.AddCombo(PotionCombo(PotionTag.Air, PotionTag.Vigor, 10.0, [PotionTag.Haste]))

    #Normal combo types
    potionManager.AddCombo(PotionCombo(PotionTag.Fire, PotionTag.Water, 10.0, [PotionTag.Steam]))
    potionManager.AddCombo(PotionCombo(PotionTag.Fire, PotionTag.Stone, 5.0, [PotionTag.Magma]))
    potionManager.AddCombo(PotionCombo(PotionTag.Water, PotionTag.Air, 8.0, [PotionTag.Storm]))

    #Advanced combos - 3 ingredients
    potionManager.AddCombo(PotionCombo(PotionTag.Fire, PotionTag.Storm, 8.0, [PotionTag.Lightning]))
    potionManager.AddCombo(PotionCombo(PotionTag.Haste, PotionTag.Fire, 9.0, [PotionTag.Scorch]))
    potionManager.AddCombo(PotionCombo(PotionTag.Haste, PotionTag.Air, 9.0, [PotionTag.Teleport]))


    #Ultra combos - 4 ingredients (Please save me from naming things)
    


# this will test tag manager if we call python tag_manager.py but not run it 
if __name__ == "__main__":
    print(str(PotionTag.Fire).split(".")[-1])
