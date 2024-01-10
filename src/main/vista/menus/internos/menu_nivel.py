"""
Módulo para el menú de un nivel.
"""

from math import pi
from typing import TYPE_CHECKING

from pygame import Rect
from pygame.display import get_surface
from pygame.draw import arc
from pygame.image import load as img_load
from pygame.transform import scale
from pygame_menu import BaseImage
from pygame_menu._types import Optional
from pygame_menu.menu import Menu

from ...fuentes import FuenteMinecraftia
from ...temas import TemaEditor
from ..supermenu import SuperMenu

if TYPE_CHECKING:
    from os import PathLike

    from pygame import Surface
    from pygame_menu.widgets import Button, Label

    from ....controlador.estado import JuegoHandler
    from ..supermenu import KwargsDict

# ----- Imágenes -----
ASSETS: "PathLike" = "./media/img/nivel"
CORAZON_LLENO: "PathLike" = f"{ASSETS}/corazon_lleno.png"
CORAZON_MITAD: "PathLike" = f"{ASSETS}/corazon_mitad.png"
CORAZON_ROTO: "PathLike" = f"{ASSETS}/corazon_roto.png"
CORAZON_VACIO: "PathLike" = f"{ASSETS}/corazon_vacio.png"
TROFEO: "PathLike" = f"{ASSETS}/trofeo.png"
# --------------------

# ----- Colores -----
COLOR_SALTO: str = "#3f48c8"
COLOR_SALTO_ACTIVO: str = "#6666ff"
COLOR_DASH: str = "#6fd806"
COLOR_DASH_ACTIVO: str = "#80ff00"
COLOR_UI: str = "#ffffff"
# -------------------


class MenuNivel(SuperMenu):
    "Menú de nivel."

    def __init__(self, juego_handler: "JuegoHandler") -> None:
        """
        Incializa el menú de nivel.
        -
        'juego_handler': Una instancia de controlador del juego. El mismo debería estar ya
                         inicializado, y por lo tanto, contener una instancia del juego dentro.
        """

        super().__init__(juego_handler)

        ancho, alto = get_surface().get_size()
        nivel = self.juego_handler.nivel
        tam_icono = alto * 0.05

        self.titulo_nivel: "Label" = self.add.label(
            title=(nivel.titulo if nivel is not None else ""),
            label_id="level_title",
            float=True,
            float_origin_position=True,
            font_name=FuenteMinecraftia(tam=int(alto * 0.03)),
            font_color=COLOR_UI
        ).translate(ancho * 0.75, -(alto * 0.085))

        self.trofeos: "Label" = self.add.label(
            title="",
            label_id="level_trophies",
            float=True,
            float_origin_position=True,
            font_name=FuenteMinecraftia(tam=int(alto * 0.03)),
            font_color=COLOR_UI
        ).translate(ancho * 0.7, -(alto * 0.085))

        dec_trofeos = self.trofeos.get_decorator()

        dec_trofeos.add_baseimage(-(ancho * 0.045), -(alto * 0.005),
                                  BaseImage(TROFEO).resize(tam_icono, tam_icono),
                                  centered=True)


    def actualizar_widgets(self) -> None:
        "Cambia algunos atributos de los widgets cuando se inicia un nivel."

        ancho, alto = get_surface().get_size()
        nivel = self.juego_handler.nivel

        self.titulo_nivel.set_title(nivel.titulo)
        self.titulo_nivel.translate(ancho * (0.765 - 0.00015 * self.titulo_nivel.get_size()[0]),
                                    -(alto * 0.085))

        recolectados, totales = nivel.trofeos()
        self.trofeos.set_title(f"{recolectados} / {totales}")
        self.trofeos.translate(ancho * 0.655, -(alto * 0.085))


    def get_super_kwargs(self) -> "KwargsDict":
        "Devuelve el diccionario de argumentos a usar en la clase madre."

        pantalla = get_surface()
        ancho, alto = pantalla.get_size()

        return dict(title="",
                    width=ancho,
                    height=alto,
                    column_max_width=None,
                    menu_id="menu_level",
                    position=(0, 0, False),
                    theme=TemaEditor())


    def dibujar_anillos_stamina(self, superficie: "Surface") -> None:
        """
        Dibuja los anillos que indican el cooldown de algunas habilidades.
        -
        'superficie': La superficie sobre la que dibujar.
        """

        ancho, alto = get_surface().get_size()

        salto = self.juego_handler.juego.jugador.salto_cooldown
        dash = self.juego_handler.juego.jugador.dash_cooldown
        start = (0.5 * pi)
        stop = (2.1 * pi)
        grosor = int(alto * 0.005)
        anillo_chico = alto * 0.0905
        anillo_grande = alto * 0.1045

        arc(superficie,
            color=(COLOR_SALTO if salto.esta_contando() else COLOR_SALTO_ACTIVO),
            rect=Rect(ancho * 0.0157, alto * 0.028,
                      anillo_grande, anillo_grande),
            width=grosor,
            start_angle=start,
            stop_angle=(start + ((stop - start) * (1.0 - salto.porcentaje()))))

        arc(superficie,
            color=(COLOR_DASH if dash.esta_contando() else COLOR_DASH_ACTIVO),
            rect=Rect(ancho * 0.01877, alto * 0.03333335,
                      anillo_chico, anillo_chico),
            width=grosor,
            start_angle=start,
            stop_angle=(start + ((stop - start) * (1.0 - dash.porcentaje()))))


    def dibujar_corazones(self, superficie: "Surface") -> None:
        """
        Dibuja los corazones de vida.
        -
        'superficie': La superficie sobre la que dibujar.
        """

        jug = self.juego_handler.juego.jugador

        if jug.hp < 0:
            return

        ancho, alto = get_surface().get_size()
        tam_grande = int(ancho * 0.04)
        tam_chico = int(ancho * 0.028)

        llenos = jug.hp // 2
        mitad = jug.hp % 2
        vacios = (jug.max_hp - jug.hp) // 2

        for i in range(llenos + mitad + vacios):
            if i < llenos:
                img = CORAZON_LLENO
            elif i < llenos + mitad:
                img = CORAZON_MITAD
            else:
                img = CORAZON_VACIO

            if i == 0:
                cor = scale(img_load(CORAZON_ROTO if jug.hp == 1 else img).convert_alpha(),
                            (tam_grande, tam_grande))
                superficie.blit(cor, (ancho * 0.04, alto * 0.025))
                continue

            cor = scale(img_load(img).convert_alpha(), (tam_chico, tam_chico))
            superficie.blit(cor, (ancho * 0.035 * (i + 1.5), alto * 0.035))


    def dibujar_nivel(self, superficie: "Surface") -> None:
        """
        Dibuja todos los elementos de la interfaz de nivel, como las puntos de vida, etc...
        -
        'superficie': La superficie sobre la que dibujar.
        """

        self.dibujar_anillos_stamina(superficie)
        self.dibujar_corazones(superficie)


    def draw(self, surface: Optional["Surface"]=None, clear_surface: bool=False) -> Menu:
        """
        Dibuja el menú del editor.
        -
        'surface': La superficie sobre la que dibujar.

        'clear_surface': Si refrescar la superficie cada vez.
        """

        self.dibujar_nivel(surface)
        self.actualizar_widgets()
        return super().draw(surface, clear_surface)
