"""
Módulo para los tipos de acciones de los controles.
"""

from enum import StrEnum

class TiposAccion(StrEnum):
    "Tipos de acciones de controles."

    IZQUIERDA = "Izquierda"
    DERECHA = "Derecha"
    SALTAR = "Salto"
    DASH = "Impulso"
