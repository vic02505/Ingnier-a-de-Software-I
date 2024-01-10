"""
Módulos para los tipos de celda.
"""

from enum import IntEnum


class TiposCelda(IntEnum):
    "Distintos identificadores para los tipos de celda."

    POS_JUGADOR = -1 # No realmente una celda, sino un centinela para spawnear el jugador
    AIRE = 0
    PLATAFORMA = 1
    PINCHO = 2
    LLAVE = 3
    PUERTA = 4
    TROFEO = 5
    SALIDA = 6
