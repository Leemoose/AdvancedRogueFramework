# Rogue Game Ideas

## Tile Effects & Schools

### Terrain Modification School
- Ice - if you move onto it, keep moving in that direction
- Pit - moves to floor below (Halfway done)

### Necromancer School
- Corpse explosion
- Raise skeleton
- Resurrect enemy
- Bone armor
- Cheat death
- Army of arms (mass slow)

### Additional Tile Effects
- Foggy, Poison mist, Snow, On fire, Flooded, Shattered
- Lightened, Darkened, Slowed, Blinded
- Pathway (can go faster), Webs, Rainy, Tar

---

## Combat & Mechanics

### Combat Modifiers
- Magic penetration <=> MR
- Mental power <=> Will power
- Attribute (susceptible or resistant)
- True damage
- Critical hits

### Resistance System
- **Attributes:** Fire, cold, poison, electric, acidic, physical
- **Types:** Slashing, stabbing, bashing, magical, psychic

### Status Effects
- Flying, Confusion, Berserk

### Miscellaneous Mechanics
- Swap with monster spell
- Flint and steel (start fire on tile)
- Skill tree system
- Portal to first floor
- Combining potions with equipment for status effects
- Corpses disappear after a while
- Randomize weapons on rarity and power

---

## Items & Crafting

### Potions
- Poison, flame, fog, levitation, speed
- Attraction/marking, divinity, bottled roots
- **Crafting:** Plant + empty bottle + flammable material = potion (unlocked after ocean branch)

### Scrolls & Books
- A way to make scrolls
- Combine scrolls to make book

### Weapons
- Cleaver, scythe, mace, spear, whip, ball and chain
- Ax can chop trees for logs
- **Butcher's blade:** Can't run from monsters, gain temp buff for each kill

### Brewing
- Fungus, kelp, plants can be brewed (fire moss)

---

## UI & Quality of Life

### UI Improvements
- Mini-icons on tiles for active status effects
- Ctrl+F for items (like DCSS)
- Show stat changes on item compare (vs currently equipped)
- Way to choose what to pick up on tiles with multiple items

### Code
- Add more comments

### Testing
- Add testing powers: see full map, never die, insta-kill monsters

---

## NPCs & Quests

### NPC Types
| NPC | Description | Role |
|-----|-------------|------|
| Forest Hermit | Old recluse who knows forest secrets | Provides history, hints, quests |
| Traveling Merchant | Wandering trader | Sells rare items/potions |
| Lost Explorer | Young enthusiast searching for relics | Side quests, rewards, location info |
| Wounded Knight | Injured in battle | Quests for herbs/monsters, weapon rewards |
| Mystic Druid | Deep forest connection | Magical items, monster insights |
| Forest Child | Grew up in forest | Guides through terrain, shortcuts |
| Cursed Ranger | Skilled but cursed | Archery training, cure quests |
| Enchanted Smith | Forges with forest materials | Upgraded weapons/armor |
| Ghostly Guardian | Ancient spirit protector | Lore quests, artifact rewards |
| Timid Herbalist | Shy potion maker | Potions, herb quests |
| NPC Doppleganger | Monster disguised as quest NPC | Attacks when approached |

### Quest Ideas
- Lifting siege of castle
- Clearing river of toxins
- Get piece of ore
- Underwater city exploration

### NPC Affinity System
- NPCs can like, dislike, or be neutral to player
- Affected by quests/actions
- Affects trade prices

---

## Monsters

### Cave
| Monster | Characteristics | Abilities |
|---------|-----------------|-----------|
| Vampiric Bat | Swarm | Dashes back after damage, drains health |
| Thing (hand) | Difficult to hit | Constricts limb for several turns |

### Dungeon
| Monster | Characteristics | Abilities |
|---------|-----------------|-----------|
| NPC Doppleganger | Looks human with quest | Camo, attacks when close |
| Blaarg the Ooze | Indestructible, very slow | Consumes people/items, spits out |
| Large Rodent | Stronger with nearby rats | Breeds by eating corpse |

### Ocean
| Monster | Characteristics | Abilities |
|---------|-----------------|-----------|
| King Crab | Double attack, meaty | Free attack on block |
| Waterwind | Flying whirlpool | Rotates player around it |

### Mountain
| Monster | Characteristics | Abilities |
|---------|-----------------|-----------|
| Scout Hawk | Only attacks in flock | Awakens other hawks |
| Pika | Runs, alerts others | Alert radius |

---

## Interactables

### Traps
- Arrows, Pit, Flame, Door shutting
- Geyser, Monsters, Quicksand, Turrets

### Generic Objects
- Chests (store items)
- Doors (open/close)
- Armor shelf (drops armor)
- Statues (decorative)
- Shrines (pray for star attention)

### Branch-Specific

**Cave:**
- Lantern - needs flammable items to not die
- Torches - light as you go

**Dungeon:**
- Fountain - empty bottle for buff
- Bookshelf - drops magic book

**Ocean:**
- Boat - cross deep water

### Other
- Hot air balloon
- Riding creature

---

## Rift Branches

### Orb Mechanics
- Different orbs for each location
- Grabbing orb eventually closes the rift
- Place all orbs in secret room to summon final monster
- Carrying orbs grants power but death drops a portal there

### Cave
- Completely dark, monsters afraid of light
- Lantern needs continuous feeding
- Massive damage in darkness
- **Reward:** Keep the lantern

### Desert
- Sun exposure/radiation
- Stepping off path calls large monsters
- Sandworms

### Ocean
- High/low tide system
- Some monsters water-only, some land-only
- Can drown if trapped in deep water
- **Reward:** Potion crafting

### Forest
- Day/night cycle (lantern useful)
- Rest camps scattered throughout
- Night monsters very strong
- Seeds grow on dirt
- **Reward:** Grow plants/moss/kelp

### Mountain
- Hunger and cold build over time
- Blizzards reduce visibility, change map, cause cold
- Small fires throughout
- Animals can be butchered
- **Reward:** Larger/organized inventory

### Dungeon
- Trap-focused
- **Reward:** Personal room with storage and bed

### Tower
- Floors go up
- Puzzles and floor guardians instead of monsters

### Carnival
- Mirrors, clowns, elephants

### Stone Quarry
- Gargoyle, golem, dancing stones
- **Reward:** Craft armor

### Butcher's Den
- Butcher boss at end
- Only meaty animals
- **Reward:** Corpse processing, corpse inventory

---

## Stars (Deity System)

### Mechanics
- Rework interest to threshold-based system
- Different actions increase interest
- "Star quest" at high interest - highest rewards, one per run
- NPC who explains stars and gives starter quest

### Star Ideas

| Star | Encourages | Rewards |
|------|------------|---------|
| Green Buck | Finding money | Extra gold drops, shop discounts |
| Northern Fist | Unarmed combat | TBD |
| Crystal Eye | Exploration | Increased LOS |
| Great Forge | Using rare equipment | Enchantment scrolls |
| Unbreakable | High endurance | Damage reduction |
| Peace Wish | Exploration without killing | XP without kills |
| Undying Light | Being at low health | Increased stats when low |
| Star of Darkness | Not exploring, not fighting, not equipping | Reduced vision tiles, dodge chance, path to stairs shown |
| Star of Battle | Defeating powerful enemies | Roll advantage, attack speed | Can't flee, wider alert radius |
| Star of Intimacy | Being near monsters, not killing | Lots of armor, monster affinity | Forced to remove armor |
| Star of Friends | Summons, friendly monsters | Buff friendlies, enemy discord |
| Star of Movement | Not standing still | Speed, wings, moving attacks |
| Star of Forest | Being in forest branch | Poison, slow, heal |
| Star of Blood | Low health | Attack speed, dodge, regen, enemy explosions |
| Star of Roundness | Levels 3,6,8,0; balanced stats | TBD |
| Star of Simplicity | One of each item type | Replenish potions/scrolls, fill gaps |
| Star of Chaos | Varied actions | Blink enemies, transform items |

---

## Races
- Halfling
- Dwarf
- Hag Witch
- Sylvan

---

## Other Ideas
- Music system
- Ocean: boats, flying
- Change monster alertness system
- Potentially change NPC conversations (in progress)
- Portals have 5% chance of sputtering out
- Adding a village

### Tutorial
- Throne room shows basic movement and stairs
- Extra hub room for mechanics tutorial:
  - Pick up items
  - Equip
  - Use spells/skills
  - Attack
  - Quaff
  - Read

### Spawning
- More monsters for rarity/groups scheme
- Deep water monsters need special pathfinding brains

---

## [AI] Additional Ideas

*Note: Ideas below this line were AI-generated and should be reviewed for fit with the game's vision.*

### [AI] Magic Schools

**Chronomancer School**
- Rewind - undo last 3 turns (high cooldown)
- Haste - extra action this turn
- Slow field - area that reduces enemy speed
- Echo strike - repeat your last attack
- Temporal anchor - mark position, teleport back later

**Illusionist School**
- Mirror image - decoys that draw attacks
- Phantasmal terrain - fake walls/pits that fool monsters
- Invisibility - breaks on attack
- Misdirection - swap places with a decoy
- Mass confusion - enemies attack each other

**Geomancer School**
- Stone skin - temporary armor boost
- Tremor - damages and staggers in a line
- Wall of stone - create impassable terrain
- Burrow - move through walls for 1 turn
- Magnetic pull - yank metallic enemies/items toward you

### [AI] New Rift Branches

**Library**
- Endless bookshelves, maze-like
- Animated books and ink monsters
- Reading books grants temp abilities but takes time (danger)
- Paper golems, bookmark mimics
- **Reward:** Spell copying - duplicate one scroll per run

**Clocktower**
- Gears and mechanisms as terrain
- Time moves differently on different floors (fast/slow zones)
- Mechanical enemies: clockwork soldiers, spring traps
- Boss: The Watchmaker
- **Reward:** Pocket watch - one free turn rewind per floor

**Fungal Depths**
- Spore clouds cause various status effects
- Symbiotic mushrooms: step on them for buffs/debuffs
- Mushroom zombies (infected corpses rise)
- Bioluminescent areas vs pitch dark
- **Reward:** Spore sack - throwable status bombs

### [AI] Monster Ideas

**Library Monsters**
| Monster | Characteristics | Abilities |
|---------|-----------------|-----------|
| Ink Wraith | Phases through shelves | Blinds with ink splash |
| Bookmark Mimic | Looks like item | Latches on, drains mana |
| Tome Guardian | Heavy, slow | Slams closed for massive damage |
| Paper Swarm | Many weak units | Reforms after "death" unless burned |

**Clocktower Monsters**
| Monster | Characteristics | Abilities |
|---------|-----------------|-----------|
| Gear Golem | Armored front only | Must flank to damage |
| Pendulum Knight | Predictable movement | Hits hard on swing path |
| Spring Jack | Erratic | Bounces unpredictably, knockback |
| Time Beetle | Tiny, fast | Steals turns (you skip a turn) |

### [AI] Items

**New Weapons**
- **Boomerang:** Returns after throw, hits twice
- **Chain hook:** Pull enemies to you or pull yourself to walls
- **Mirror shield:** Chance to reflect projectiles
- **Hourglass staff:** Spells cost turns instead of mana

**New Consumables**
- **Amnesia dust:** Makes monsters forget you exist (resets aggro)
- **Bottled echo:** Repeats your last action
- **Shrinking potion:** Fit through small gaps, reduced damage
- **Petrification flask:** Throw to freeze enemy as statue (blocks path)

**Cursed Items** (powerful but with drawbacks)
- **Ring of Hunger:** +3 all stats, but hunger drains 2x fast
- **Bloodthirst blade:** Lifesteal, but you can't heal any other way
- **Paranoid helm:** See invisible, but also see "phantom" enemies that aren't real
- **Gambler's coin:** 50% chance for double effect, 50% for nothing

### [AI] Stars

| Star | Encourages | Rewards | Drawback |
|------|------------|---------|----------|
| Star of Secrets | Finding hidden rooms/traps | X-ray vision pulses, trap immunity | Doors lock behind you |
| Star of Gluttony | Eating everything | Gain stats from food, never full | Constant hunger |
| Star of Echoes | Revisiting cleared floors | Monsters drop better loot on return | Floors repopulate stronger |
| Star of Mercy | Letting enemies flee | Pacified enemies become neutral | Can't kill fleeing enemies |
| Star of Mirrors | Using reflective items | Clone yourself briefly | Clones can hurt you too |

### [AI] Mechanics

**Reputation System**
- Different factions (undead, beasts, constructs, etc.)
- Killing one faction improves standing with rivals
- High reputation: faction ignores you or helps
- Low reputation: faction hunts you specifically
- Some shops only serve certain reputations

**Weather System** (beyond just branch-specific)
- Rain: extinguishes fire, slippery floors, reduced vision
- Wind: projectiles curve, light enemies pushed
- Fog: severely reduced LOS for everyone
- Heat wave: faster hunger/thirst, fire spreads faster

**Combo System**
- Certain actions in sequence trigger bonuses
- Kill 3 enemies without moving = "Stand your ground" (temp armor)
- Move 10 tiles without stopping = "Momentum" (next attack bonus)
- Use 3 different damage types in a row = "Versatile" (crit chance)

### [AI] Quality of Life

- **Auto-explore** with danger interrupt
- **Item favorites** - mark items to never drop/sell
- **Run log** - see stats from previous runs (kills, floors, cause of death)
- **Ghost mode** - after death, watch your ghost replay the run
- **Loadouts** - save equipment configurations at storage

### [AI] Races

| Race | Passive | Starting Bonus | Drawback |
|------|---------|----------------|----------|
| Golem | Immune to poison/bleed | +2 armor | Can't eat food, must repair |
| Shade | Invisible in darkness | Start with cloak | Light damages you |
| Beastkin | Smell nearby enemies | Unarmed bonus | Shops charge more (distrust) |
| Fungoid | Regenerate in spore clouds | Immune to fungal effects | Fire does 2x damage |
