"""
Class-based spell definitions.

Each spell is a class that inherits from BaseSpell and defines
its behavior through class attributes and method overrides.

Import all spell classes here for easy registration.
"""

from .burning_attack import BurningAttack
from .burning_circle import BurningCircle
from .fireball import Fireball

# Fire spells
__all__ = [
    'BurningAttack',
    'BurningCircle',
    'Fireball',
]
