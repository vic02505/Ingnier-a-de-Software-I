"""
Módulo para el renderizador de un nivel.
"""

from math import degrees
from typing import TYPE_CHECKING, Optional, TypeAlias

from pygame import Rect, Surface
from pygame.constants import K_F3, KEYDOWN
from pygame.display import get_surface
from pygame.draw import circle, rect
from pygame.math import Vector2

from ...controlador.editor import (DIRECCIONES_SPRITES, MISSING_IMG_PATH,
                                   MatrizSprites)
from ...modelo.utils import Temporizador
from ..fuentes import FuenteMinecraftia
from ..sprites import Animacion

if TYPE_CHECKING:
    from pygame.event import Event

    from ...controlador.estado import JuegoHandler

ListaPuntos: TypeAlias = dict[tuple[int, int], Temporizador]
MatrizVisibilidad: TypeAlias = list[list[bool]]

COLOR_FONDO: str = "#bbbbbb"
COLOR_INFO: str = "#ffffff"
COLOR_ADY: str = "#dddd00"
COLOR_ADY_2: str = "#aaaa00"
COLOR_PUNTO: str = "#ff0000"
INVISIBLE: tuple[int, int, int, int] = (0, 0, 0, 0)


class RenderizadorNivel:
    """
    Clase que dibuja cosas en un nivel.
    Esto es distinto del 'menú' que también está presente dentro un nivel. Este renderizador,
    más que botones y etiquetas, dibuja los sprites mismos de las celdas, así como los fondos.
    """

    def __init__(self, juego_handler: "JuegoHandler") -> None:
        """
        Inicializa el renderizador de nivel.
        -
        'juego_handler': El handler que engloba todo aspecto del juego.
        """

        self.juego_handler: "JuegoHandler" = juego_handler
        self.matriz_sprites: Optional[MatrizSprites] = None
        self._visibles: Optional[MatrizVisibilidad] = None
        self.mostrar_debug: bool = False
        self.debug_puntos: ListaPuntos = {}


    def hay_nivel(self) -> bool:
        "Verifica si el juego tiene un nivel asignado."

        return self.juego_handler.nivel is not None


    def alternar_debug(self) -> bool:
        "Alterna entre si mostrar la info de debug o no."

        self.mostrar_debug = not self.mostrar_debug


    def get_sprite(self, col: int, fil: int) -> Optional[Animacion]:
        """
        Genera un sprite para la celda en las coordenadas pedidas.
        -
        'col/fil': La columna y fila de la matriz de celdas.
        """

        celda = self.juego_handler.nivel.celda(col, fil)

        if celda is None or not celda.visible:
            return None

        incr_x, incr_y = self.juego_handler.nivel.incremento_celda

        return Animacion(
            pos=Vector2(col * incr_x, fil * incr_y),
            tam=Vector2(incr_x, incr_y),
            ruta=DIRECCIONES_SPRITES.get(celda.tipo, MISSING_IMG_PATH)
        ).rotar(degrees(celda.rot))


    def generar_sprites(self) -> MatrizSprites:
        """
        Genera todos los sprites en la matriz correspondiente.
        Se presupone que existe un nivel y este no es `None`.
        """

        col, fil = self.juego_handler.nivel.forma
        matriz = []

        for j in range(fil):
            fila = []
            for i in range(col):
                fila.append(self.get_sprite(i, j))

            matriz.append(fila)

        return matriz


    def _generar_visibilidad(self) -> MatrizVisibilidad:
        """
        Genera una matriz auxiliar para llevar cuenta de la
        visibilidad de las celdas.
        """

        col, fil = self.juego_handler.nivel.forma
        matriz_vis = []

        for j in range(fil):
            fila = []
            for i in range(col):
                celda = self.juego_handler.nivel.celda(i, j)
                fila.append(celda.visible if celda is not None else False)

            matriz_vis.append(fila)

        return matriz_vis


    def dibujar_fondo(self, superficie: Surface) -> None:
        """
        Dibuja el fondo del nivel.
        -
        'superficie': La superficie sobre la que dibujar.
        """

        superficie.fill(COLOR_FONDO)


    def dibujar_sprites(self, superficie: Surface) -> None:
        """
        Dibuja todos los sprites de la matriz del nivel.
        -
        'superficie': La superficie sobre la que dibujar.
        """

        for fila in self.matriz_sprites:
            for spr in fila:
                if spr is not None:
                    spr.dibujar(superficie)


    def _analizar_visibilidad(self) -> None:
        """
        Analiza cada celda para ver si su visibilidad cambió.
        Si ya no es visible, no se debería dibujar esa celda.
        """

        col, fil = self.juego_handler.nivel.forma

        for j in range(fil):
            for i in range(col):
                celda = self.juego_handler.nivel.celda(i, j)
                if celda is None or celda.visible == self._visibles[j][i]:
                    continue

                self._visibles[j][i] = celda.visible
                self.matriz_sprites[j][i] = self.get_sprite(i, j)


    def _renderizar_info(self, contenido: str, tam: int=12) -> list[Surface]:
        """
        Renderiza un string de varias líneas en varias superficies listas
        para usar.
        -
        'contenido': El mensaje entero, normalmente de varias líneas.

        'tam': El tamaño de la fuente del mensaje.
        """

        fuente = FuenteMinecraftia(tam=tam)
        rend = []
        for linea in contenido.split("\n"):
            rend.append(fuente.render(linea.rstrip(), False, COLOR_INFO))

        return rend


    def dibujar_debug_info(self, superficie: Surface) -> None:
        """
        Dibuja información destinada a depurar el juego.
        -
        'superficie': La superficie sobre la que dibujar.
        """

        if not self.mostrar_debug:
            return

        ancho, alto = get_surface().get_size()
        jug = self.juego_handler.juego.jugador
        cooldown_msg = lambda num: num if num else "Listo!"
        jug_col, jug_fil = self.juego_handler.nivel.coords_matriz(jug.hitbox.centerx,
                                                                  jug.hitbox.centery)
        incr_x, incr_y = self.juego_handler.nivel.incremento_celda

        info = (
f"""Pos={jug.pos}
Vel={jug.vel}
Acc={jug.acc}
tam={jug.hitbox.width, jug.hitbox.height}
Vidas={jug.hp}
Estado='{jug.estado}'
¿Mira hacia la derecha?={"Sí" if jug.mira_derecha else "No"}
Salto={jug.salto}   |   Cooldown={cooldown_msg(jug.salto_cooldown.actual)}
Dash={jug.dash}      |   Cooldown={cooldown_msg(jug.dash_cooldown.actual)}
Inv={cooldown_msg(jug.invulnerabilidad.actual)}
Version='v{self.juego_handler.version_str}'"""
)

        self.debug_puntos[jug.hitbox.center] = Temporizador(200)

        for (pos_x, pos_y), temp in self.debug_puntos.items():
            tam = int(alto * 0.004)
            surf_punto = Surface((tam, tam)) 
            circle(surface=surf_punto, color=COLOR_PUNTO,
                   center=(tam // 2, tam // 2), radius=tam)
            surf_punto.set_alpha(255 * temp.porcentaje())
            superficie.blit(surf_punto, (pos_x - tam, pos_y - tam))

        for j in range(-1, 2):
            for i in range(-1, 2):
                if (i, j) == (0, 0) or not self.juego_handler.nivel.existe(jug_col + i,
                                                                           jug_fil + j):
                    continue

                surf = Surface((int(incr_x), int(incr_y)))
                rect(surf, COLOR_ADY, Rect(0, 0, incr_x, incr_y))
                rect(surf, COLOR_ADY_2, Rect(0, 0, incr_x, incr_y), width=int(alto * 0.005))
                surf.set_alpha(50)
                superficie.blit(surf, ((jug_col + i) * incr_x, (jug_fil + j) * incr_y))

        for i, fuente_img in enumerate(self._renderizar_info(info, int(alto * 0.02))[::-1]):
            superficie.blit(fuente_img, (ancho * 0.01, alto * ( 1 - 0.03 * (i + 1))))


    def _actualizar_puntos(self) -> None:
        """
        Actualiza el diccionario de puntos de posición, para la
        información de depuración.
        """

        puntos_copia = self.debug_puntos.copy()
        for pos, temp in self.debug_puntos.items():
            temp.actualizar(1)
            if not temp.esta_contando():
                puntos_copia.pop(pos)
        self.debug_puntos = puntos_copia


    def reiniciar_nivel(self) -> None:
        "Reinicia los datos de nivel."

        self.matriz_sprites = self.generar_sprites()
        self._visibles = self._generar_visibilidad()


    def actualizar(self, superficie: Surface, eventos: list["Event"]) -> None:
        """
        Actualiza todos los elementos de la interfaz del nivel.
        -
        'superficie': La superficie sobre la que dibujar.

        'eventos': Lista de eventos de Pygame.
        """

        if not self.hay_nivel():
            return

        if self.matriz_sprites is None:
            self.reiniciar_nivel()

        for ev in eventos:
            if ev.type == KEYDOWN and ev.key == K_F3:
                self.alternar_debug()

        self.dibujar_fondo(superficie)
        self._analizar_visibilidad()
        self.dibujar_sprites(superficie)
        self._actualizar_puntos()
