"""
Paquete para todos los tests unitarios.
"""

# ----- Sin esto Pygame muestra un cartel cada vez que se corre el programa -----
from os import environ

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
# -------------------------------------------------------------------------------

from unittest import main as test_main

from .modelo.estado import *
from .modelo.jugador import *
from .modelo.utils import *

if __name__ == "__main__":
    test_main()
