# Crafting Mechanics

## Raw Ingredients

Have percentages associated with each tag. Coding wise, we do a dict mapping tag names to percentages. Raw ingredient tags are primary effects. When combined, there is a chance for primary effects to convert to secondary ones.

### Basic Ingredients - High Chance of One Element

| Ingredient | Primary | Secondary | Tertiary | Nothing |
|---|---|---|---|---|
| Blaze Pepper | 70% fire | 20% smoke | 9% lightning | 1% |
| Frost Fern | 70% ice | 20% water | 9% acid | 1% |
| Stormcap Shroom | 70% lightning | 20% wind | 9% ice | 1% |
| Windweed | 70% wind | 20% ice | 9% earth | 1% |
| Caustic Caper | 70% acid | 20% poison | 9% fire | 1% |
| Rancid Root | 70% poison | 20% earth | 9% water | 1% |
| Stonebud Petal | 70% earth | 20% fire | 9% lightning | 1% |
| Aqua Algae | 70% water | 20% poison | 9% ice | 1% |

### Complex Ingredients - Less Certainty, Chance of Multiple Tags

| Ingredient | Tag A | Tag B | Combo | Nothing |
|---|---|---|---|---|
| Burn Bamboo | 25% fire | 25% acid | 45% fire + acid | 5% |
| Vortex Vine | 25% wind | 25% water | 45% wind + water | 5% |
| Obscura Root | 25% smoke | 25% darkness | 45% smoke + darkness | 5% |
| Frostfire Fruit | 25% fire | 25% ice | 45% fire + ice | 5% |

### Rare Ingredients - Custom Percentages, Weird Tags

| Ingredient | Distribution |
|---|---|
| Elemental Chaos Bulb | 5% of 20 different tags |
| Distortion Tuber | 30% spatial, 30% darkness, 10% spatial + darkness, 30% nothing |
| Gamblers Berry | 50% death, 50% nothing |

---

## Combining into Potions

When crafting a potion, choose up to 3 ingredients. Sum up and normalize percentages of each tag present across the 3 ingredients. Then, randomly select the first primary tag amongst the new percentages. After, select another tag with the following procedure:

- Keep selecting tags until nothing is selected (if nothing selected first, considered a "dud" result, maybe makes a default potion with very basic effects)
- After each selection, the chance of nothing goes up by 5, then 10, then 20, 30 etc. The chance of the selected tag goes down by the same value nothing has increased to ensure we still sum to 100%.
  - *Reasoning: gambling on potion results a little bit and ensuring it's very hard to get potions with like 50 different tags*
- For each tag after the first, there is a 25% chance the tag effect is converted to a secondary effect (we'll have a map of primary to secondary effects). This percentage increases by 25% for every primary effect selected so far.
  - *Reasoning: makes it less likely to have fire+ice+lightning+every element potions, but more likely to have fire+ice+AOE+damage over time etc.*

---

## Primary vs Secondary Tags

Each primary tag has a secondary equivalent that it has a chance to map to:

| Primary | Secondary |
|---|---|
| Fire | Circle AOE |
| Lightning | Line AOE |
| Acid | Extra Duration |
| Poison | Damage Over Time |
| Ice | Slow |
| Water | Knockback |

*Etc, maybe scrap this and just have secondary tags on normal ingredients too.*

*Reasoning: avoid typeless AOE potions*

---

## Processed Ingredients

Different ways to process ingredients that affect these percentages.

### Boil - Increase Highest Percentage (to Max of 90), Remove Chance of Weaker Percentages

**Boiling Blaze Pepper:**
70 fire / 20 acid / 9 lightning / 1 nothing → 90 fire / 10 nothing

**Boiling Vortex Vine:**
25 wind / 25 water / 45 wind+water / 5 nothing → 90 wind+water / 10 nothing

### Bake - Increase Lowest Non-Nothing Percentage to Be the Highest (Randomly Chosen if Tied). Decrease Others by 40%.

**Baking Blaze Pepper:**
70 fire / 20 acid / 9 lightning / 1 nothing → 42 fire / 12 acid / 45 lightning / 1 nothing

**Baking Vortex Vine:**
25 wind / 25 water / 45 wind+water / 5 nothing → 53 wind / 15 water / 27 wind+water / 5 nothing *or* 15 wind / 53 water / 27 wind+water / 5 nothing

### Distill - Convert Primary Properties into Secondary Properties. Guarantees That Secondary Property in the Potion but Increases Chance of Nothing by 5%.

**Distilling Blaze Pepper:**
70 fire / 20 acid / 9 lightning / 1 nothing → 65 circle AOE / 20 extra duration / 9 line AOE / 6 nothing
