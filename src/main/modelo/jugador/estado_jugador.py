"""
Módulo para un enumerador de los estados del jugador.
"""

from enum import StrEnum


class EstadoJugador(StrEnum):
    "Numerosos estados del jugador."

    QUIETO = "quieto"
    CAMINANDO_IZQ = "caminando_izq"
    CAMINANDO_DER = "caminando_der"
    PARED_IZQ = "pared_izq"
    PARED_DER = "pared_der"
    DASH_IZQ = "dash_izq"
    DASH_DER = "dash_der"
    SALTANDO = "saltando"
    CAYENDO = "cayendo"
