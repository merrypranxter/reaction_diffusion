"""
Alternative reaction-diffusion models.
"""
from .belousov_zhabotinsky import OregonatorBZ, BZExcitableMedium
from .fitzHugh_nagumo import FitzHughNagumo, FHNNetwork
from .cahn_hilliard import CahnHilliard, CahnHilliardWithNoise
from .schnakenberg import Schnakenberg

__all__ = [
    'OregonatorBZ',
    'BZExcitableMedium',
    'FitzHughNagumo',
    'FHNNetwork',
    'CahnHilliard',
    'CahnHilliardWithNoise',
    'Schnakenberg',
]
