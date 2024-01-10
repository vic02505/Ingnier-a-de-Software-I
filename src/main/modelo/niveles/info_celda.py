"""
Módulo para una estructura de información de una celda.
"""

from typing import NamedTuple, TypeAlias

from ..celdas import TiposCelda

MatrizInfoCeldas: TypeAlias = list[list["InfoCelda"]]


class InfoCelda(NamedTuple):
    "Tupla con propiedades de una celda."

    tipo: TiposCelda = TiposCelda.AIRE
    rot: float = 0.0
    visible: bool = True
    id: int = 0
