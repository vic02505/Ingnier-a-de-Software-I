"""
Módulo para eventos de sonido.
Esto normalmente se usa para reproducir sonidos por fuera del modelo,
mandando eventos de Pygame.
"""

from enum import IntEnum


class EventosSonidos(IntEnum):
    "Enumerador para eventos de audio."

    DANIO = 1000
    DANIO_FUERTE = 1001
    LLAVE = 1002
    TROFEO = 1003
