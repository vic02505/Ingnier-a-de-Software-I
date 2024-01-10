"""
Módulo para la ventana de perder una partida.
"""


from typing import TYPE_CHECKING

from pygame.display import get_surface
from pygame_menu import BaseImage

from ...temas import TemaFresh
from ..supermenu import SuperMenu
from .menu_controles import ARROW_LEFT_IMG_PATH
from .menu_opciones import BACK_IMG_PATH
from .menu_principal import EXIT_IMG_PATH

if TYPE_CHECKING:
    from os import PathLike

    from pygame_menu.widgets import Button

    from ....controlador.estado import JuegoHandler
    from ..supermenu import KwargsDict

PLAY_AGAIN_IMG_PATH: "PathLike" = BACK_IMG_PATH
GO_BACK_IMG_PATH: "PathLike" = ARROW_LEFT_IMG_PATH


class MenuPerderPartida(SuperMenu):
    "Clase del menú principal."


    def __init__(self, juego_handler: "JuegoHandler") -> None:
        """
        Incializa el menú principal.
        -
        'juego_handler': Una instancia de controlador del juego. El mismo debería estar ya
                         inicializado, y por lo tanto, contener una instancia del juego dentro.
        """

        super().__init__(juego_handler)

        self.btn_jugar: "Button" = self.add.button(title="Jugar de nuevo",
                                                   action=self.juego_handler.iniciar_juego)
        self.btn_volver: "Button" = self.add.button(title="Volver al menú principal",
                                                    action=self.juego_handler.cambiar_a_principal)
        self.btn_salir: "Button" = self.add.button(title="Salir del juego",
                                                   action=self.juego_handler.salir)

        dec_jugar = self.btn_jugar.get_decorator()
        dec_volver = self.btn_volver.get_decorator()
        dec_salir = self.btn_salir.get_decorator()

        ancho, alto = get_surface().get_size()
        tam_icon = alto * 0.075

        dec_jugar.add_baseimage(-(ancho * 0.1855), 0,
                                BaseImage(PLAY_AGAIN_IMG_PATH).resize(tam_icon, tam_icon),
                                centered=True)
        dec_volver.add_baseimage(-(ancho * 0.27), -(alto * 0.01),
                                 BaseImage(GO_BACK_IMG_PATH).resize(tam_icon, tam_icon),
                                 centered=True)
        dec_salir.add_baseimage(-(ancho * 0.1775), -(alto * 0.01),
                                BaseImage(EXIT_IMG_PATH).resize(tam_icon, tam_icon).flip(x=True,
                                                                                         y=False),
                                centered=True)


    def get_super_kwargs(self) -> "KwargsDict":
        "Devuelve el diccionario de argumentos a usar en la clase madre."

        pantalla = get_surface()
        ancho, alto = pantalla.get_size()

        return dict(title="¡Has perdido!",
                    width=ancho * 0.55,
                    height=alto * 0.55,
                    column_max_width=None,
                    menu_id="game_lost",
                    position=(0, alto * 0.4, False),
                    theme=TemaFresh())
