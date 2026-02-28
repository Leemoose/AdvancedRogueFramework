"""
Spell definitions - Python-based spell library.

All spells are defined in this package and auto-register when imported.
Each school has its own module for organization.

Usage:
    # Import all spells
    from spell_system import spells

    # Or import a specific school
    from spell_system.spells import fire
"""

# Import all schools to register their spells
from . import fire
from . import mind
from . import necromancy
from . import space
from . import summon

# Re-export for convenience
from .fire import *
from .mind import *
from .necromancy import *
from .space import *
from .summon import *
