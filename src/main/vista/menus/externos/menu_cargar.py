"""
Módulo para el menú de cargar niveles.
"""

from pathlib import Path
from typing import TYPE_CHECKING, Optional, TypeAlias

from pygame.display import get_surface
from pygame_menu import BaseImage

from ...temas import TemaFresh
from ..supermenu import SuperMenu, MENUS_IMG
from .menu_controles import ARROW_LEFT_IMG_PATH

if TYPE_CHECKING:
    from os import PathLike

    from pygame import Surface
    from pygame_menu import Menu
    from pygame_menu.widgets import Button

    from ....controlador.estado import JuegoHandler
    from ..supermenu import KwargsDict

BotonesNiveles: TypeAlias = dict[str, "Button"]

NIVEL_EXT: str = ".nivel"
RUTA_NIVELES: "PathLike" = "./niveles"
# --- Assets ---
NIVEL_IMG: "PathLike" = f"{MENUS_IMG}/nivel.png"
NIVEL_PACK_IMG: "PathLike" = f"{MENUS_IMG}/nivel_pack.png"
# --------------


class DirectorioNoExiste(FileNotFoundError):
    "Cuando un directorio que se busca no existe en realidad."


class MenuCargar(SuperMenu):
    "Clase del menú de cargar niveles."

    def __init__(self, juego_handler: "JuegoHandler") -> None:
        """
        Incializa el menú de cargar niveles.
        -
        'juego_handler': Una instancia de controlador del juego. El mismo debería estar ya
                         inicializado, y por lo tanto, contener una instancia del juego dentro.
        """

        super().__init__(juego_handler)

        self.btn_volver: Optional["Button"] = None
        self.botones_niveles: BotonesNiveles = {}


    def _actualizar_volver_btn(self) -> None:
        "Actualiza la imagen para volver del menú."

        ancho, alto = get_surface().get_size()
        tam_icon = alto * 0.05

        self.btn_volver.translate(ancho * 0.75, -(alto * 0.1))

        dec_volver = self.btn_volver.get_decorator()
        dec_volver.add_baseimage(-(ancho * 0.095), (alto * 0.002),
                                 BaseImage(ARROW_LEFT_IMG_PATH).resize(tam_icon * 1.2, tam_icon),
                                 centered=True)


    def get_super_kwargs(self) -> "KwargsDict":
        "Devuelve el diccionario de argumentos a usar en la clase madre."

        pantalla = get_surface()
        ancho, alto = pantalla.get_size()

        return dict(title="Cargar Niveles",
                    width=ancho,
                    height=alto * 0.65,
                    column_max_width=None,
                    menu_id="menu_load_lvl",
                    position=(0, alto * 0.38, False),
                    theme=TemaFresh())


    def _dir_es_compatible(self, directorio: Path) -> bool:
        """
        Decide si un directorio es un archivo de nivel válido.
        -
        'directorio': La ruta en cuestión.
        """

        return directorio.is_file() and directorio.suffix.lower() == NIVEL_EXT


    def _dir_habitado(self, directorio: Path) -> bool:
        """
        Decide si un directorio no está vacío y contine archivos de niveles válidos.
        -
        'directorio': La ruta en cuestión.
        """

        for arch in directorio.iterdir():
            if self._dir_es_compatible(arch):
                return True

        return False


    def cargar_botones(self) -> None:
        "Carga los botones de niveles."

        self.actualizar_rutas_niveles(RUTA_NIVELES)

        self.btn_volver = self.add.button(
            title="Volver",
            action=self.juego_handler.cambiar_a_principal,
            float=True,
            float_origin_position=True,
        )
        self._actualizar_volver_btn()


    def actualizar_rutas_niveles(self,
                                 ruta_madre: "PathLike",
                                 purgar: bool=True) -> None:
        """
        Carga todas las rutas de niveles que encuentra bajo el directorio especificado.
        -
        'ruta_madre': El directorio donde buscar.

        'purgar': Si eliminar preventivamente todos los widgets que habían antes.
        """

        if purgar:
            self.clear()

        ruta = Path(ruta_madre)

        if not ruta.exists():
            raise DirectorioNoExiste(f"Directorio especificado '{ruta.as_posix()}' no encontrado.")

        ancho, alto = get_surface().get_size()
        tam_icono = alto * 0.075

        for direc in ruta.iterdir():
            if direc.is_dir() and self._dir_habitado(direc):
                self.botones_niveles[direc.name] = self.add.button(
                    title=f"{direc.name}/",
                    action=self.juego_handler.iniciar_juego,
                    button_id=f"btn_dir_{direc.name}",
                    accept_kwargs=True,
                    niveles=self._inspeccionar_dir_niveles(direc)
                )
                ruta_img = NIVEL_PACK_IMG

            elif self._dir_es_compatible(direc):
                self.botones_niveles[direc.name] = self.add.button(
                    title=direc.name,
                    action=self.juego_handler.iniciar_juego,
                    button_id=f"btn_file_{direc.name}",
                    accept_kwargs=True,
                    niveles=(direc.as_posix(),)
                )
                ruta_img = NIVEL_IMG

            else:
                ruta_img = None


            if ruta_img is not None:
                dec_btn = self.botones_niveles[direc.name].get_decorator()
                dec_btn.add_baseimage(
                    -(self.botones_niveles[direc.name].get_width() * 0.5 + ancho * 0.03), 0,
                    BaseImage(ruta_img).resize(tam_icono, tam_icono),
                    centered=True,
                )


    def _inspeccionar_dir_niveles(self, ruta_niv: Path) -> tuple["PathLike", ...]:
        """
        Inspecciona y devuelve una tupla de todas las rutas compatibles
        de niveles.
        -
        'ruta_niv': Un objeto de ruta que contiene directorios dentro, los cuales son los
                    que se analizan.
        """

        lista_rutas = []

        for direc in ruta_niv.iterdir():
            if self._dir_es_compatible(direc):
                lista_rutas.append(direc.as_posix())

        return tuple(lista_rutas)


    def dibujar_titulo_cargar_nv(self, superficie: "Surface") -> None:
        """
        Dibuja el título del juego en este menú de cargar niveles.
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
        Dibuja el menú de cargar niveles.
        -
        'surface': La superficie sobre la que dibujar.

        'clear_surface': Si refrescar la superficie cada vez.
        """

        self.dibujar_titulo_cargar_nv(surface)
        return super().draw(surface, clear_surface)
