from enum import Enum
import bisect #Used to do sorted list inserts!

#Base values for enums! Add here to create more types
class PotionTag(Enum):
    Fire  = 0,
    Water = 1,
    Steam = 2,
    Stone = 3,
    Magma = 4

class PotionCombo():
    def __init__(self, leftTag, rightTag, priority, outputs):
        self.m_leftTag = leftTag
        self.m_rightTag = rightTag
        self.m_priority = priority
        self.m_outputs = outputs

    #Match function that handles cases where a match is duplicates!
    def Matches(self, tagOne, tagTwo):
        oneLeft = (tagOne == self.m_leftTag)
        oneRight = (tagOne == self.m_rightTag)
        twoLeft =  (tagTwo == self.m_leftTag)
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
                            tags.append(combo.m_outputs)
                            anyMatches = True
                            break
                    if (anyMatches):
                        break
                if (anyMatches):
                    break

potionManager = PotionManager()

def InitPotionTags():
    potionManager.AddCombo(PotionCombo(PotionTag.Fire, PotionTag.Water, 1.0, [PotionTag.Steam]))
    potionManager.AddCombo(PotionCombo(PotionTag.Fire, PotionTag.Stone, 0.5, [PotionTag.Magma]))
