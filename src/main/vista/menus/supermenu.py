"""
Módulo para la clase base de menús personalizados.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Optional, TypeAlias, Union

from pygame.image import load as img_load
from pygame.transform import scale
from pygame_menu import Menu

if TYPE_CHECKING:
    from os import PathLike

    from pygame import Surface
    from pygame.math import Vector2

    from ...controlador.estado import JuegoHandler

KwargsDict: TypeAlias = dict[str, Any]
ValorCoord: TypeAlias = Union[int, float]
Coord: TypeAlias = Union[tuple[ValorCoord, ValorCoord], "Vector2"]

MENUS_IMG: "PathLike" = "./media/img/menus"
TITLE_IMG_PATH: "PathLike" = "./media/img/titulo/cube_jumper.png"


class SuperMenu(ABC, Menu):
    "Clase base de menú personalizado."

    def __init__(self, juego_handler: "JuegoHandler") -> None:
        """
        Inicializa un menú personalizado.
        -
        'juego_handler': Una instancia de controlador del juego. El mismo debería estar ya
                         inicializado, y por lo tanto, contener una instancia del juego dentro.
        """

        super_kwargs = self.get_super_kwargs()
        super_kwargs.update(
            mouse_motion_selection=True,
        )

        super().__init__(**super_kwargs)
        self.juego_handler: "JuegoHandler" = juego_handler

        # ----- sfx -----
        # Importante: NO llamar a self.menu_handler.cambiar_audio() en este __init__
        self.juego_handler.cambiar_volumen(self.juego_handler.get_volumen())
        self.set_sound(self.juego_handler.sfx.menus_sfx)
        # ---------------


    @abstractmethod
    def get_super_kwargs(self) -> KwargsDict:
        "Devuelve el diccionario de argumentos a usar en la clase madre."

        raise NotImplementedError


    def dibujar_titulo(self,
                       superficie: "Surface",
                       dest: Coord,
                       tam: Optional[Coord]=None) -> None:
        """
        Dibuja el título del juego.
        Éste no puede ser renderizado como un widget del menú, pues se posiciona
        fuera del mismo.
        -
        'superficie': La superficie sobre la que dibujar.

        'dest': Dónde pegar la imagen del título en la superficie.

        'tam': El tamaño del título mismo. Si no se especifica, se utiliza el tamaño
               con el que viene.
        """

        im = img_load(TITLE_IMG_PATH).convert_alpha()
        if tam is not None:
            im = scale(im, tam)

        superficie.blit(im, dest)
