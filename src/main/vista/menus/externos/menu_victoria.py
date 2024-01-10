"""
Módulo de menú de victoria.
"""

from typing import TYPE_CHECKING

from pygame.display import get_surface
from pygame_menu import BaseImage

from ...temas import TemaFresh
from ..supermenu import SuperMenu
from .menu_principal import PLAY_IMG_PATH
from .menu_controles import ARROW_LEFT_IMG_PATH

if TYPE_CHECKING:
    from pygame_menu.widgets import Button, Label

    from ....controlador.estado import JuegoHandler
    from ..supermenu import KwargsDict


class MenuVictoria(SuperMenu):
    "Clase de un menú de victoria."

    def __init__(self, juego_handler: "JuegoHandler") -> None:
        """
        Incializa el menú de victoria.
        -
        'juego_handler': Una instancia de controlador del juego. El mismo debería estar ya
                         inicializado, y por lo tanto, contener una instancia del juego dentro.
        """

        super().__init__(juego_handler)

        self.trofeos: "Label" = self.add.label(
            title="",
            label_id="trophy_lbl"
        )
        self.btn_jugar: "Button" = self.add.button(title="Jugar de nuevo",
                                                   action=self.juego_handler.iniciar_juego)
        self.btn_volver_menu_ppal: "Button" = self.add.button(title="Volver al menu principal",
                                                   action=self.juego_handler.cambiar_a_principal)

        dec_jugar = self.btn_jugar.get_decorator()
        btn_volver_menu_ppal = self.btn_volver_menu_ppal.get_decorator()

        ancho, alto = get_surface().get_size()
        tam_icon = alto * 0.075

        dec_jugar.add_baseimage(-(ancho * 0.187), -(alto * 0.01),
                                BaseImage(PLAY_IMG_PATH).resize(tam_icon, tam_icon),
                                centered=True)
        btn_volver_menu_ppal.add_baseimage(
            -(ancho * 0.27), -(alto * 0.01),
            BaseImage(ARROW_LEFT_IMG_PATH).resize(tam_icon, tam_icon),
            centered=True)

        self.actualizar_etiqueta_trofeos()

    def get_super_kwargs(self) -> "KwargsDict":
        "Devuelve el diccionario de argumentos a usar en la clase madre."

        pantalla = get_surface()
        ancho, alto = pantalla.get_size()

        return dict(title="¡Has ganado!",
                    width=ancho * 0.55,
                    height=alto * 0.5,
                    column_max_width=None,
                    menu_id="game_won",
                    position=(0, alto * 0.4, False),
                    theme=TemaFresh())

    def actualizar_etiqueta_trofeos(self) -> None:
        "Actualiza y refresca la etiqueta de trofeos acorde."

        self.trofeos.set_title(f"Trofeos recogidos:  {self.juego_handler.trofeos_recogidos}")
