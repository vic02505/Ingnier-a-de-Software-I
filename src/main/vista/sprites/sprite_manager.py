"""
Módulo para un manager de sprites.
"""

from typing import TYPE_CHECKING, Optional, TypeAlias

from pygame.math import Vector2

from .animacion import Animacion

if TYPE_CHECKING:
    from os import PathLike

    from pygame import Surface

    from .animacion import SpriteElegido

RutasDict: TypeAlias = dict[str, "PathLike"]
AnimDict: TypeAlias = dict[str, Animacion]


class SpritesManager:
    "Clase que contiene todos los sprites del jugador."


    def __init__(self,
                 pos: Vector2,
                 tam: Vector2,
                 rutas_anim: RutasDict,
                 default: Optional[str]=None) -> None:
        """
        Inicializa los sprites del jugador.
        -
        'pos': Un vector en 2 dimensiones (`pygame.math.Vector2`), el cual representa
               la posición del jugador.

        'tam': El tamaño horizontal/vertical del sprite del jugador.

        'rutas_anim': Un diccionario que contiene el nombre de la animación del sprite y la
                      carpeta donde encontrar los frames de dicha animación.

        'default': El nombre de la animación inicial.
        """

        if not rutas_anim:
            raise ValueError("Debe haber al menos 1 sprite en 'rutas_anim'")

        self.pos: Vector2 = pos
        self.tam: Vector2 = tam # Esto idealmente no debería cambiar

        self.animaciones: AnimDict = {}
        for nombre, ruta in rutas_anim.items():
            self.animaciones[nombre] = Animacion(self.pos, self.tam, ruta)

        self.nombre_actual: str = (default if default is not None
                                   else list(self.animaciones.keys())[0])


    @property
    def anim_actual(self) -> Animacion:
        "Devuelve la animación actualmente siendo dibujada."

        return self.animaciones[self.nombre_actual]


    def cambiar_animacion(self, nombre: str) -> Animacion:
        """
        Intenta cambiar la animación actual.
        -
        'nombre': El nombre de la animación actual. Si no la encuentra, no hace nada.
        """

        if nombre in self.animaciones:
            self.nombre_actual = nombre
            self.anim_actual.reiniciar_indice()

        return self.anim_actual


    def siguiente_frame(self) -> int:
        "Cambia el frame actual por el siguiente."

        return self.anim_actual.siguiente_frame()


    def cambiar_pos(self, nueva_pos: Vector2) -> None:
        "Cambia la posición de todas las animaciones."

        if not isinstance(nueva_pos, Vector2):
            return

        self.pos = nueva_pos
        for anim in self.animaciones.values():
            anim.pos = nueva_pos


    def dibujar(self, superficie: "Surface", alpha: int=255) -> "SpriteElegido":
        """
        Dibuja la animación actual. Devuelve el sprite que se acaba de dibujar.
        -
        'superficie': La superficie sobre la que dibujar.

        'alpha': La transparencia de la imagen. Debe ser un número entre 0 y 255.
        """

        return self.anim_actual.dibujar(superficie, alpha)
