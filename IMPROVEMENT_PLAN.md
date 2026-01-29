# RogueGame Improvement Plan

**Goal:** Tighten code, improve structure, fix UI cross-platform issues, and create distributable builds for PC/Mac.

**Context:** Python roguelike using pygame + pygame_gui. ~209 Python files.

**Last Updated:** January 29, 2026

**See also:** `COMPLETED_WORK.md` for finished items.

---

## Status Summary

| Phase | Status | Remaining |
|-------|--------|-----------|
| Phase 1: Foundation | ✅ Complete | - |
| Phase 2: Performance | ✅ 95% | Minor optimizations |
| Phase 3: Code Quality | ✅ 85% | Constants migration, style fixes |
| Phase 4: Architecture | ✅ 90% | Data-driven design |
| Phase 5: Features | 🔲 Not Started | Settings menu, bugs |

---

## Remaining Work

### Code Quality (Low Priority)

**Constants Migration**
- Replace remaining `== -1` with `NO_ENTITY` where applicable
- Replace magic tile IDs with `TileIDRange.*`
- Replace hardcoded colors with `Colors.*`

**Style Fixes**
- Fix remaining `== None` → `is None` (1 occurrence in `summon_school.py`)
- Replace remaining `print()` with `logging`
- Remove commented code blocks
- Add type hints to core files

**Dead Code**
- Remove unused import in `monsters/monster.py` (references deleted `unused/` folder)

---

### Data-Driven Design (Medium Priority)

Move definitions to JSON/YAML for easier modding:
- Monster stats
- Item stats
- Spawn rates
- Level progression

---

### Features (Phase 5)

**From Notes/todo.txt:**
- [ ] Range weapons system
- [ ] Fix mini examine window
- [ ] Spell hotkey hover display
- [ ] Skill vs Spell distinction (cooldown vs mana)
- [ ] Monster AI escape behavior fix
- [ ] Split item screen description/buttons

**New Features:**
- [ ] Settings menu (volume, keybindings, display)
- [ ] Windowed/fullscreen toggle
- [ ] Resolution selection
- [ ] Accessibility options

---

### Known Bugs (from bugs.txt)

| Bug | Severity |
|-----|----------|
| IndexError on fire terrain | 🔴 Crash |
| Duplicate skill from item + book | 🟡 Gameplay |
| Dojo art covering stairs | 🟡 Visual |
| Gateway direction issues | 🟡 Gameplay |
| Loading into wrong room | 🟡 Gameplay |
| Dialogue font apostrophes | 🟢 Minor |
| Enchant scroll inventory filter | 🟢 Minor |
| Summon hornet damage effect | 🟢 Minor |
| Blink scroll range validation | 🟡 Gameplay |

---

## Build Commands

```bash
# Install dependencies
pip install -r requirements.txt pyinstaller

# Run game
python roguewriting.py

# Build executable
pyinstaller RogueGame.spec

# Mac: Create distributable zip
cd dist && zip -r RogueGame-Mac.zip RogueGame.app
```

---

## Key Files

| Purpose | File |
|---------|------|
| Entry point | `roguewriting.py` |
| Asset loading | `static_configs.py` |
| Main display | `display_generation/display.py` |
| UI components | `display_generation/ui.py` |
| UI theme | `assets/theme.json` |
| Screen helpers | `display_generation/ui_utils.py` |
| Event system | `src/core/events.py` |
| Constants | `src/core/constants.py` |
