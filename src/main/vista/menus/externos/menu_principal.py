"""
Módulo de menú principal.
"""

from typing import TYPE_CHECKING, Optional

from pygame.display import get_surface
from pygame_menu import BaseImage

from ...fuentes import FuenteMinecraftia
from ...temas import TemaFresh
from ..supermenu import MENUS_IMG, SuperMenu

if TYPE_CHECKING:
    from os import PathLike

    from pygame import Surface
    from pygame_menu import Menu
    from pygame_menu.widgets import Button, Label

    from ....controlador.estado import JuegoHandler
    from ..supermenu import KwargsDict

PLAY_IMG_PATH: "PathLike" = f"{MENUS_IMG}/play.png"
LOAD_IMG_PATH: "PathLike" = f"{MENUS_IMG}/load.png"
EDITOR_IMG_PATH: "PathLike" = f"{MENUS_IMG}/editor.png"
COG_IMG_PATH: "PathLike" = f"{MENUS_IMG}/cog_white.png"
EXIT_IMG_PATH: "PathLike" = f"{MENUS_IMG}/exit.png"


class MenuPrincipal(SuperMenu):
    "Clase del menú principal."


    def __init__(self, juego_handler: "JuegoHandler") -> None:
        """
        Incializa el menú principal.
        -
        'juego_handler': Una instancia de controlador del juego. El mismo debería estar ya
                         inicializado, y por lo tanto, contener una instancia del juego dentro.
        """

        super().__init__(juego_handler)

        self.btn_jugar: "Button" = self.add.button(title="Jugar",
                                                   action=self.juego_handler.iniciar_juego)
        self.btn_cargar: "Button" = self.add.button("Cargar",
                                                    action=self.juego_handler.cambiar_a_cargar)
        self.btn_editor: "Button" = self.add.button(title="Editor",
                                                    action=self.juego_handler.cambiar_a_editor)
        self.btn_opciones: "Button" = self.add.button(title="Opciones",
                                                      action=self.juego_handler.cambiar_a_opciones)
        self.btn_salir: "Button" = self.add.button(title="Salir",
                                                   action=self.juego_handler.salir)

        ancho, alto = get_surface().get_size()

        self.msg_version: "Label" = self.add.label(
            title=f"v{self.juego_handler.version_str}",
            label_id="msg_ver",
            float=True,
            float_origin_position=True,
            font_name=FuenteMinecraftia(tam=int(alto * 0.03))
        ).translate(ancho * 0.72, alto * 0.44)

        dec_jugar = self.btn_jugar.get_decorator()
        dec_cargar = self.btn_cargar.get_decorator()
        dec_editor = self.btn_editor.get_decorator()
        dec_opciones = self.btn_opciones.get_decorator()
        dec_salir = self.btn_salir.get_decorator()

        tam_icon = alto * 0.075

        dec_jugar.add_baseimage(-(ancho * 0.092), 0,
                                BaseImage(PLAY_IMG_PATH).resize(tam_icon, tam_icon),
                                centered=True)
        dec_cargar.add_baseimage(-(ancho * 0.105), 0,
                                BaseImage(LOAD_IMG_PATH).resize(tam_icon * 1.1, tam_icon),
                                centered=True)
        dec_editor.add_baseimage(-(ancho * 0.09), 0,
                                 BaseImage(EDITOR_IMG_PATH).resize(tam_icon * 1.2, tam_icon),
                                   centered=True)
        dec_opciones.add_baseimage(-(ancho * 0.125), 0,
                                   BaseImage(COG_IMG_PATH).resize(tam_icon * 1.1, tam_icon),
                                   centered=True)
        dec_salir.add_baseimage(-(ancho * 0.078), 0,
                                BaseImage(EXIT_IMG_PATH).resize(tam_icon, tam_icon).flip(x=True,
                                                                                         y=False),
                                centered=True)


    def get_super_kwargs(self) -> "KwargsDict":
        "Devuelve el diccionario de argumentos a usar en la clase madre."

        pantalla = get_surface()
        ancho, alto = pantalla.get_size()

        return dict(title="Menú Principal",
                    width=ancho,
                    height=alto * 0.6,
                    column_max_width=None,
                    menu_id="menu_main",
                    position=(0, alto * 0.38, False),
                    theme=TemaFresh())


    def dibujar_titulo_principal(self, superficie: "Surface") -> None:
        """
        Dibuja el título del juego en el menú principal.
        Éste no puede ser renderizado como un widget del menú, pues se posiciona
        fuera del mismo.
        -
        'superficie': La superficie sobre la que dibujar.
        """

        ancho, alto = get_surface().get_size()
        self.dibujar_titulo(superficie,
                            (ancho * 0.4, alto * 0.0),
                            (ancho * 0.5, alto * 0.4))


    def draw(self, surface: Optional["Surface"]=None, clear_surface: bool=False) -> "Menu":
        """
        Dibuja el menú principal.
        -
        'surface': La superficie sobre la que dibujar.

        'clear_surface': Si refrescar la superficie cada vez.
        """

        self.dibujar_titulo_principal(surface)
        return super().draw(surface, clear_surface)
