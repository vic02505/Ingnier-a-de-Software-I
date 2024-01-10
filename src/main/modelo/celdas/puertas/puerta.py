"""
Módulo para una puerta.
"""

from typing import TYPE_CHECKING

from ..celda_abc import Celda
from ..tipos_de_celda import TiposCelda

if TYPE_CHECKING:
    from pygame import Rect

    from ...jugador import Jugador
    from ..llaves import Llave


class Puerta(Celda):
    "Clase para una puerta desbloqueable."

    def __init__(self, rect: "Rect", rot: float=0.0, vis: bool=True) -> None:
        """
        Inicializa la puerta.
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
        self.esta_cerrada: bool = True
        self.llaves_asociadas: list["Llave"] = []


    @property
    def tipo(self) -> TiposCelda:
        "Devuelve el tipo de celda."

        return TiposCelda.PUERTA


    def es_tangible(self) -> bool:
        "Indica si permite colisiones."

        return self.esta_cerrada


    def es_movil(self) -> bool:
        "Indica si la celda es móvil."

        return False


    def efecto_jug_arriba(self, jugador: "Jugador") -> None:
        """
        Define el efecto que esta celda tendría sobre el jugador en el caso
        de colisionar con el mismo, de haber uno.
        -
        'jugador': La instancia de jugador sobre la que actuar el efecto.
        """

        if self.es_tangible():
            if jugador.vel.y > 0:
                jugador.hitbox.y = self.rect.top - jugador.hitbox.height
                jugador.vel.y = 0
                jugador.acc.y = 0


    def efecto_jug_izq(self, jugador: "Jugador") -> None:
        """
        Define el efecto que esta celda tendría sobre el jugador en el caso
        de colisionar con el mismo desde la izquierda de la celda, de haber uno.
        -
        'jugador': La instancia de jugador sobre la que actuar el efecto.
        """

        if self.es_tangible():
            jugador.hitbox.x = self.rect.left - jugador.hitbox.width - 1
            jugador.vel.x = 0
            jugador.acc.x = 0


    def efecto_jug_der(self, jugador: "Jugador") -> None:
        """
        Define el efecto que esta celda tendría sobre el jugador en el caso
        de colisionar con el mismo desde la derecha de la celda, de haber uno.
        -
        'jugador': La instancia de jugador sobre la que actuar el efecto.
        """

        if self.es_tangible():
            jugador.hitbox.x = self.rect.right + 1
            jugador.vel.x = 0
            jugador.acc.x = 0


    def efecto_jug_abajo(self, jugador: "Jugador") -> None:
        """
        Define el efecto que esta celda tendría sobre el jugador en el caso
        de colisionar con el mismo desde debajo de la celda, de haber uno.
        -
        'jugador': La instancia de jugador sobre la que actuar el efecto.
        """

        if self.es_tangible():
            if jugador.vel.y < 0:
                jugador.hitbox.y = self.rect.bottom
                jugador.vel.y = 0
                jugador.acc.y = 0


    def abrir(self) -> None:
        """
        Abre la puerta.
        """

        self.esta_cerrada = False
        self.visible = False


    def cerrar(self) -> None:
        """
        Cierra la puerta.
        """

        self.esta_cerrada = True
        self.visible = True
