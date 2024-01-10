"""
Módulo para la interfaz de una celda.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from .tipos_de_celda import TiposCelda

if TYPE_CHECKING:
    from pygame import Rect

    from ..jugador import Jugador


class Celda(ABC):
    "Interfaz base para una celda en el mapa de un nivel."

    rect: "Rect"
    rot: float
    visible: float

    @abstractmethod
    def __init__(self, rect: "Rect", rot: float=0.0, vis: bool=True) -> None:
        """
        Inicializa la celda.
        -
        'rect': Una instancia de `pygame.Rect()` que contiene tanto la posición como el
                tamaño de la celda.

        'rot': La rotación dada por la orientación de la celda, en radianes.
               Por defecto, esto es 0.

        'vis': Si la celda se puede ver o no.
        """

        raise NotImplementedError


    @property
    @abstractmethod
    def tipo(self) -> TiposCelda:
        "Devuelve el tipo de celda."

        raise NotImplementedError


    @abstractmethod
    def es_tangible(self) -> bool:
        "Indica si permite colisiones."

        raise NotImplementedError


    @abstractmethod
    def es_movil(self) -> bool:
        "Indica si la celda es móvil."

        raise NotImplementedError


    @abstractmethod
    def efecto_jug_arriba(self, jugador: "Jugador") -> None:
        """
        Define el efecto que esta celda tendría sobre el jugador en el caso
        de colisionar con el mismo desde arriba de la celda, de haber uno.
        -
        'jugador': La instancia de jugador sobre la que actuar el efecto.
        """

        raise NotImplementedError


    @abstractmethod
    def efecto_jug_izq(self, jugador: "Jugador") -> None:
        """
        Define el efecto que esta celda tendría sobre el jugador en el caso
        de colisionar con el mismo desde la izquierda de la celda, de haber uno.
        -
        'jugador': La instancia de jugador sobre la que actuar el efecto.
        """

        raise NotImplementedError


    @abstractmethod
    def efecto_jug_der(self, jugador: "Jugador") -> None:
        """
        Define el efecto que esta celda tendría sobre el jugador en el caso
        de colisionar con el mismo desde la derecha de la celda, de haber uno.
        -
        'jugador': La instancia de jugador sobre la que actuar el efecto.
        """

        raise NotImplementedError


    @abstractmethod
    def efecto_jug_abajo(self, jugador: "Jugador") -> None:
        """
        Define el efecto que esta celda tendría sobre el jugador en el caso
        de colisionar con el mismo desde debajo de la celda, de haber uno.
        -
        'jugador': La instancia de jugador sobre la que actuar el efecto.
        """

        raise NotImplementedError
