"""
Módulo para la celda que es la salida del nivel.
"""

from typing import TYPE_CHECKING

from ..celda_abc import Celda
from ..tipos_de_celda import TiposCelda

if TYPE_CHECKING:
    from pygame import Rect

    from ...jugador import Jugador


class Salida(Celda):
    "Clase para la salida de un nivel."

    def __init__(self, rect: "Rect", rot: float=0.0, vis: bool=True) -> None:
        """
        Inicializa la salida.
        -
        'rect': Una instancia de `pygame.Rect()` que contiene tanto la posición como el
                tamaño de la celda.

        'rot': La rotación dada por la orientación de la celda, en radianes.
               Por defecto, esto es 0.

        'vis': Si la celda se puede ver o no.
        """

        self.rect: "Rect" = rect
        self.rot: float = rot
        self.visible: bool = vis


    @property
    def tipo(self) -> TiposCelda:
        "Devuelve el tipo de celda."

        return TiposCelda.SALIDA


    def es_tangible(self) -> bool:
        "Indica si permite colisiones."

        return False


    def es_movil(self) -> bool:
        "Indica si la celda es móvil."

        return False


    def efecto_jug_arriba(self, jugador: "Jugador") -> None:
        """
        Define el efecto que esta celda tendría sobre el jugador en el caso
        de colisionar con el mismo desde arriba de la celda, de haber uno.
        -
        'jugador': La instancia de jugador sobre la que actuar el efecto.
        """

        return None


    def efecto_jug_izq(self, jugador: "Jugador") -> None:
        """
        Define el efecto que esta celda tendría sobre el jugador en el caso
        de colisionar con el mismo desde la izquierda de la celda, de haber uno.
        -
        'jugador': La instancia de jugador sobre la que actuar el efecto.
        """

        return None


    def efecto_jug_der(self, jugador: "Jugador") -> None:
        """
        Define el efecto que esta celda tendría sobre el jugador en el caso
        de colisionar con el mismo desde la derecha de la celda, de haber uno.
        -
        'jugador': La instancia de jugador sobre la que actuar el efecto.
        """

        return None


    def efecto_jug_abajo(self, jugador: "Jugador") -> None:
        """
        Define el efecto que esta celda tendría sobre el jugador en el caso
        de colisionar con el mismo desde debajo de la celda, de haber uno.
        -
        'jugador': La instancia de jugador sobre la que actuar el efecto.
        """

        return None
