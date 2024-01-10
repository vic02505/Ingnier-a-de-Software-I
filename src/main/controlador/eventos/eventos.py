"""
Módulo para eventos personalizados.
"""

from enum import IntEnum


class EventosJuego(IntEnum):
    """
    Eventos personalizados para el juego.
    Mientras sean números enteros, no habrá problema con los IDs, pero se recomienda que sean
    mayores a 900 para no hacer conflicto con los eventos de Pygame.
    """

    PROCESAR_MOV_JUGADOR = 900
    REDIBUJAR_JUGADOR = 901
    CONTAR_TIMERS = 902
    PEDIR_INPUT_TECLA = 903
