"""
Módulo del handler del editor de niveles.
"""

from enum import StrEnum
from math import degrees, pi
from typing import TYPE_CHECKING, Optional, TypeAlias, Union

from pygame import Rect
from pygame.constants import (BUTTON_LEFT, BUTTON_MIDDLE, BUTTON_RIGHT,
                              BUTTON_WHEELDOWN, BUTTON_WHEELUP, K_KP_MINUS,
                              K_KP_PLUS, K_MINUS, K_PLUS, KEYDOWN,
                              MOUSEBUTTONUP, MOUSEMOTION, K_v)
from pygame.display import get_surface
from pygame.draw import rect
from pygame.math import Vector2

from ...modelo.celdas import TiposCelda
from ...modelo.editor import EditorNiveles
from ...modelo.utils import Temporizador
from ...vista.fuentes import FuenteMinecraftia
from ...vista.sprites import Animacion
from ..eventos import EventosJuego

if TYPE_CHECKING:
    from os import PathLike

    from pygame import Surface
    from pygame.event import Event

    from ...modelo.niveles import InfoNivel
    from ..logger import LoggerJuego

MatrizSprites: TypeAlias = list[list[Optional[Animacion]]]
DireccionesSprites: TypeAlias = dict[TiposCelda, "PathLike"]

SPRITES_CELDAS: "PathLike" = "./media/sprites/celdas"
MISSING_IMG_PATH: "PathLike" = "./media/sprites/otros/missing"
POS_JUGADOR_IMG_PATH: "PathLike" = f"{SPRITES_CELDAS}/pos_jugador"
PLATAFORMA_IMG_PATH: "PathLike" = f"{SPRITES_CELDAS}/plataforma_simple"
PINCHO_IMG_PATH: "PathLike" = f"{SPRITES_CELDAS}/pincho"
LLAVE_IMG_PATH: "PathLike" = f"{SPRITES_CELDAS}/llave"
PUERTA_IMG_PATH: "PathLike" = f"{SPRITES_CELDAS}/candado_fill"
TROFEO_IMG_PATH: "PathLike" = f"{SPRITES_CELDAS}/trofeo"
SALIDA_IMG_PATH: "PathLike" = f"{SPRITES_CELDAS}/salida"

DIRECCIONES_SPRITES: DireccionesSprites = {
    TiposCelda.POS_JUGADOR: POS_JUGADOR_IMG_PATH,
    TiposCelda.PLATAFORMA: PLATAFORMA_IMG_PATH,
    TiposCelda.PINCHO: PINCHO_IMG_PATH,
    TiposCelda.LLAVE: LLAVE_IMG_PATH,
    TiposCelda.PUERTA: PUERTA_IMG_PATH,
    TiposCelda.TROFEO: TROFEO_IMG_PATH,
    TiposCelda.SALIDA: SALIDA_IMG_PATH
}

TRANSPARENCIA: int = 100

# --- Colores ---
COLOR_FONDO: str = "#dfdfdf"
COLOR_FONDO_1: str = "#cccccc"
COLOR_FONDO_2: str = "#bbbbbb"
COLOR_FONDO_MENU: str = "#333333"
COLOR_IDS: str = "#fefeee"
# ---------------


class PosicionesMensajesEditor(StrEnum):
    "Posiciones para los mensajes del editor."

    CURSOR_ARRIBA = "cur_arriba"
    CURSOR_IZQUIERDA = "cur_izq"
    CURSOR_DERECHA = "cur_der"
    CURSOR_ABAJO = "cur_abajo"
    INFO_ARRIBA = "info_arriba"


class EditorHandler:
    "Clase de handler del editor de niveles."

    def __init__(self, logger: Optional["LoggerJuego"]=None) -> None:
        """
        Inicializa el handler del editar de niveles.
        -
        'logger': El registrador del juego.
        """

        _, alto = get_surface().get_size()

        self.editor: EditorNiveles = EditorNiveles()
        self.logger: Optional["LoggerJuego"] = logger
        self.espacio_menu: float = alto * 0.15
        self.matriz_sprites: MatrizSprites = self._generar_matriz_sprites()

        self._enfocada: Vector2 = Vector2(0, 0)
        self.mouse: Vector2 = Vector2(0.0, 0.0)

        self.mensajes: dict[str, list[Union[str, Temporizador]]] = {
            PosicionesMensajesEditor.CURSOR_ARRIBA: ["", Temporizador(2000)],
            PosicionesMensajesEditor.CURSOR_IZQUIERDA: ["", Temporizador(2000)],
            PosicionesMensajesEditor.CURSOR_DERECHA: ["", Temporizador(2000)],
            PosicionesMensajesEditor.CURSOR_ABAJO: ["", Temporizador(2000)],
            PosicionesMensajesEditor.INFO_ARRIBA: ["", Temporizador(5000)]
        }


    @property
    def enfocada(self) -> tuple[int, int]:
        "Devuelve los índices de la celda actualmente enfocada."

        return self._enfocada.x, self._enfocada.y


    @enfocada.setter
    def enfocada(self, valores: tuple[int, int]) -> None:
        """
        Cambia el valor de la celda enfocada.
        -
        valores: Una tupla de dos números enteros, que indican los índices.
        """

        x, y = valores
        self._enfocada.x = x
        self._enfocada.y = y


    @property
    def incremento_x(self) -> float:
        "Devuelve el incremento horizontal de las celdas."

        ancho_ventana, _ = get_surface().get_size()
        ed_ancho, _ = self.editor.forma
        return ancho_ventana / ed_ancho


    @property
    def incremento_y(self) -> float:
        "Devuelve el incremento vertical de las celdas."

        _, alto_ventana = get_surface().get_size()
        _, ed_alto = self.editor.forma
        return (alto_ventana - self.espacio_menu) / ed_alto


    def set_ancho(self, ancho: int) -> None:
        """
        Modifica el ancho de la matriz.
        -
        'ancho': El ancho objetivo de la matriz.
        """

        ed_ancho, _ = self.editor.forma

        dif = ancho - ed_ancho
        if dif == 0:
            return

        if dif <= -ed_ancho:
            dif = -ed_ancho + 1

        self.editor.set_ancho(ancho)
        self.extender_ancho(dif)


    def extender_ancho(self, cuanto: int) -> None:
        """
        Extiende o contrae el ancho de la matriz.
        -
        'cuanto': Cuántas columnas agregar o sacar.
        """

        ed_ancho, _ = self.editor.forma

        if cuanto == 0:
            return
        if cuanto <= -ed_ancho:
            cuanto = -ed_ancho + 1

        if cuanto > 0:
            for fila in self.matriz_sprites:
                fila.extend([None for _ in range(cuanto)])

        elif cuanto < 0:
            for fila in self.matriz_sprites:
                for _ in range(abs(cuanto)):
                    fila.pop()

        self._refrescar_pos_sprites()


    def set_alto(self, alto: int) -> None:
        """
        Modifica el alto de la matriz.
        -
        'alto': El alto objetivo de la matriz.
        """

        _, ed_alto = self.editor.forma

        dif = alto - ed_alto
        if dif == 0:
            return

        if dif <= -ed_alto:
            dif = -ed_alto + 1

        self.editor.set_alto(alto)
        self.extender_alto(dif)


    def extender_alto(self, cuanto: int) -> None:
        """
        Extiende o contrae el alto de la matriz.
        -
        'cuanto': Cuántas filas agregar o sacar.
        """

        _, ed_alto = self.editor.forma

        if cuanto == 0:
            return
        if cuanto <= -ed_alto:
            cuanto = -ed_alto + 1

        if cuanto > 0:
            ancho = len(self.matriz_sprites[0])
            for _ in range(cuanto):
                self.matriz_sprites.append([None for _ in range(ancho)])

        elif cuanto < 0:
            for _ in range(abs(cuanto)):
                self.matriz_sprites.pop()

        self._refrescar_pos_sprites()


    def importar(self, titulo: str) -> "InfoNivel":
        """
        Importa un nivel desde un archivo con el nombre dado.
        -
        'titulo': El nombre del archivo.
        """

        datos_nivel = self.editor.importar(titulo)
        self.matriz_sprites = self._generar_matriz_sprites()
        self.enfocada = 0, 0

        return datos_nivel


    def exportar(self, titulo: str) -> Optional["PathLike"]:
        """
        Exporta el nivel a un archivo con nombre.
        -
        'titulo': El nombre del archivo.
        """

        if not self.editor.existe_jugador():
            self.refrescar_mensaje("ERROR: Se necesita la casilla del jugador para que "
                                   "el nivel sea jugable",
                                   PosicionesMensajesEditor.INFO_ARRIBA)
            return None

        return self.editor.exportar(titulo)


    def _get_sprite(self, ancho: int, alto: int,
                    tipo: Optional[TiposCelda]=None,
                    rot: Optional[float]=None) -> Optional[Animacion]:
        """
        Consigue el
        -
        'ancho/alto': Las coordenadas de la celda de la matriz.

        'tipo': El tipo de la celda. Si no se especifica se trata de buscarlo en la
                matriz de sprites.

        'rot': La rotación deseada del sprite. Si no se especifica se trata de
               buscarlo en la matriz de sprites.
        """

        ocupado = True

        if tipo is None:
            tipo = self.editor.matriz[alto][ancho].tipo
            ocupado = self.editor.ocupado(ancho, alto)

        if rot is None:
            rot = self.editor.matriz[alto][ancho].rot

        ruta_spr = (DIRECCIONES_SPRITES.get(tipo, MISSING_IMG_PATH)
                    if ocupado else None)

        if ruta_spr is None:
            return None

        return Animacion(pos=Vector2(self.incremento_x * ancho,
                                     self.incremento_y * alto + self.espacio_menu),
                         tam=Vector2(self.incremento_x, self.incremento_y),
                         ruta=ruta_spr).rotar(degrees(rot))


    def _generar_matriz_sprites(self) -> MatrizSprites:
        "Genera una animación de sprite por cada celda en al grilla."

        matriz = []
        ancho, alto = self.editor.forma

        for j in range(alto):
            fila = []
            for i in range(ancho):
                fila.append(self._get_sprite(i, j))
            matriz.append(fila)

        return matriz


    def _refrescar_pos_sprites(self) -> None:
        "Refresca las posiciones de los elementos de la matriz de sprites."

        ancho, alto = self.editor.forma

        for j in range(alto):
            for i in range(ancho):
                spr = self.matriz_sprites[j][i]
                if spr is not None:
                    spr.pos = Vector2(self.incremento_x * i,
                                      self.incremento_y * j + self.espacio_menu)


    def coords_matriz(self, px_x: float, px_y: float) -> tuple[int, int]:
        """
        Dadas las coordenadas en pixeles del cursor, devuelve a qué casilla
        de la matriz cae.
        -
        'px_x/px_y': Las coordenadas del cursor, en pixeles de la pantalla.
        """

        coord_x = int(px_x / self.incremento_x)
        coord_y = int((px_y - self.espacio_menu) / self.incremento_y)
        return coord_x, coord_y


    def aplicar_sprite(self, ancho: int, alto: int) -> Animacion:
        """
        Aplica la animación del tipo sostenido.
        -
        'ancho/alto': Las coordenadas de la celda de la matriz.
        """

        spr = self._get_sprite(ancho, alto,
                               self.editor.celda_sostenida, self.editor.rot_sostenida)
        self.matriz_sprites[alto][ancho] = spr
        return spr


    def borrar_sprite(self, ancho: int, alto: int) -> None:
        """
        Borra el sprite en las coordenadas dadas.
        -
        'ancho/alto': Las coordenadas de la celda de la matriz.
        """

        self.matriz_sprites[alto][ancho] = None


    # pylint: disable=invalid-name
    def esta_en_area(self, mx: Optional[float]=None, my: Optional[float]=None) -> bool:
        """
        Verifica que las coordenadas del cursor están adentro del área de la grilla.
        -
        'mx/my': Las coordenadas del cursor. Si no son especificadas, se intenta con
                 las últimas coordenadas registradas del cursor.
        """

        ancho, alto = get_surface().get_size()

        if mx is None:
            mx = self.mouse.x

        if my is None:
            my = self.mouse.y

        return (0 < mx < ancho) and (self.espacio_menu < my < alto)


    def _purgar_pos_jugador(self) -> None:
        "Va celda por celda eliminando todas las que sean posiciones de jugadores."

        ancho, alto = self.editor.forma

        for j in range(alto):
            for i in range(ancho):
                if self.editor.matriz[j][i].tipo == TiposCelda.POS_JUGADOR:
                    self.editor.borrar_celda(i, j)
                    self.borrar_sprite(i, j)


    def dibujar_fondo(self, superficie: "Surface") -> None:
        """
        Dibuja el fondo del editor, con los colores predeterminados.
        -
        'superficie': La superficie sobre la que dibujar.
        """

        ancho_ventana, _ = get_surface().get_size()
        ancho, alto = self.editor.forma

        superficie.fill(COLOR_FONDO)
        rect(superficie, color=COLOR_FONDO_MENU,
             rect=Rect(0, 0, ancho_ventana, self.espacio_menu))

        for j in range(alto):
            for i in range(ancho):
                rect(superficie,
                    color=(COLOR_FONDO_1 if ((i % 2 == 0) == (j % 2 == 0)) else COLOR_FONDO_2),
                    rect=Rect(self.incremento_x * i,
                              (self.incremento_y * j) + self.espacio_menu,
                              self.incremento_x, self.incremento_y))


    def dibujar_celdas(self, superficie: "Surface") -> None:
        """
        Dibuja el sprite de cada celda de la grilla.
        -
        'superficie': La superficie sobre la que dibujar.
        """

        ancho, alto = self.editor.forma
        for j in range(alto):
            for i in range(ancho):
                spr = self.matriz_sprites[j][i]
                if spr is not None:
                    vis = self.editor.matriz[j][i].visible
                    spr.dibujar(superficie, alpha=(255 if vis else 125))


    def dibujar_ids(self, superficie: "Surface", tipos_aceptados: tuple[TiposCelda, ...]) -> None:
        """
        Dibuja los IDs sobre las celdas correspondientes.
        -
        'superficie': La superficie sobre la que dibujar.

        'tipos_aceptados': Una tupla con todos los tipos de celda a considerar para
                           dibujar los IDs.
        """

        _, alto = get_surface().get_size()
        fuente = FuenteMinecraftia(tam=int(alto * 0.025))
        ancho, alto = self.editor.forma

        for j in range(alto):
            for i in range(ancho):
                if self.editor.matriz[j][i].tipo not in tipos_aceptados:
                    continue

                fuente_img = fuente.render(str(self.editor.matriz[j][i].id),
                                           False, COLOR_IDS)
                superficie.blit(fuente_img, (i * self.incremento_x,
                                             j * self.incremento_y + self.espacio_menu))


    def dibujar_sostenido(self, superficie: "Surface") -> None:
        """
        Dibuja la celda que está siendo sostenida por el cursor.
        -
        'superficie': La superficie sobre la que dibujar.
        """

        if not self.esta_en_area():
            return

        enf_x, enf_y = self.enfocada
        spr = self._get_sprite(enf_x, enf_y,
                               self.editor.celda_sostenida, self.editor.rot_sostenida)
        spr.set_transparencia(TRANSPARENCIA)
        spr.dibujar(superficie)


    def _actualizar_timers(self) -> None:
        "Actualiza los temporizadores y cooldowns."

        for _, temp in self.mensajes.values():
            temp.actualizar(1)


    def _get_nombre_sostenido(self) -> str:
        "Consigue un nombre legible del tipo de celda sostenida."

        return " ".join(self.editor.celda_sostenida.name.split("_"))


    def _get_rot_sostenida(self) -> str:
        "Consigue un string legible de los grados de rtoación actuales."

        return f"{degrees(self.editor.rot_sostenida)}°"


    def sostiene_jugador(self) -> bool:
        "Verifica si la celda sostenida es el centinela para la posición del jugador."

        return self.editor.celda_sostenida == TiposCelda.POS_JUGADOR


    def refrescar_mensaje(self, mensaje: str, cual: PosicionesMensajesEditor) -> None:
        """
        Refresca un mensaje del editor.
        -
        'mensaje': El contenido del nuevo mensaje.

        'cual': El identificador del mensaje.
        """

        self.mensajes[cual][0] = mensaje
        self.mensajes[cual][1].reiniciar()


    def _refrescar_msg_id(self) -> None:
        "Refresca el mensaje que indica el ID sostenido."

        self.refrescar_mensaje(f"ID: {self.editor.id_sostenido}",
                               PosicionesMensajesEditor.CURSOR_ABAJO)


    def actualizar(self, superficie: "Surface", eventos: list["Event"]) -> None:
        """
        Actualiza el editor de niveles.
        -
        'superficie': La superficie (`pygame.Surface`) en donde se va a dibujar todos los
                      cambios visuales a aplicar.

        'eventos': La lista de eventos de Pygame a procesar.
        """

        self.dibujar_fondo(superficie)
        self.dibujar_celdas(superficie)
        self.dibujar_ids(superficie, (TiposCelda.PUERTA, TiposCelda.LLAVE))
        self.dibujar_sostenido(superficie)

        for ev in eventos:
            if ev.type == MOUSEBUTTONUP:
                mx, my = ev.pos
                if not self.esta_en_area(mx, my):
                    continue

                col, fil = self.coords_matriz(mx, my)

                if ev.button == BUTTON_LEFT:
                    if self.sostiene_jugador():
                        self._purgar_pos_jugador()
                    self.editor.cambiar_celda(col, fil)
                    self.aplicar_sprite(col, fil)

                elif ev.button == BUTTON_RIGHT:
                    self.editor.borrar_celda(col, fil)
                    self.borrar_sprite(col, fil)

                elif ev.button == BUTTON_MIDDLE:
                    if self.sostiene_jugador():
                        self.refrescar_mensaje("(No se puede cambiar la rotación del jugador)",
                                               PosicionesMensajesEditor.CURSOR_DERECHA)
                    else:
                        self.editor.rotar(pi / 2)
                        self.refrescar_mensaje(f"({self._get_rot_sostenida()})",
                                               PosicionesMensajesEditor.CURSOR_DERECHA)

                elif ev.button == BUTTON_WHEELUP:
                    self.editor.ant_tipo()
                    if self.sostiene_jugador():
                        self.editor.reiniciar_rot()
                        self.editor.visibilidad_sostenida = True
                    self.refrescar_mensaje(self._get_nombre_sostenido(),
                                           PosicionesMensajesEditor.CURSOR_ARRIBA)

                elif ev.button == BUTTON_WHEELDOWN:
                    self.editor.sig_tipo()
                    if self.sostiene_jugador():
                        self.editor.reiniciar_rot()
                        self.editor.visibilidad_sostenida = True
                    self.refrescar_mensaje(self._get_nombre_sostenido(),
                                           PosicionesMensajesEditor.CURSOR_ARRIBA)

            elif ev.type == KEYDOWN:
                if ev.key == K_v:
                    if self.sostiene_jugador():
                        self.refrescar_mensaje("(No se puede cambiar la visibilidad del jugador)",
                                               PosicionesMensajesEditor.CURSOR_IZQUIERDA)
                    else:
                        visib = self.editor.alternar_visibilidad()
                        self.refrescar_mensaje(("(Visible)" if visib else "(No visible)"),
                                                PosicionesMensajesEditor.CURSOR_IZQUIERDA)

                elif ev.key in (K_MINUS, K_KP_MINUS):
                    self.editor.disminuir_id()
                    self._refrescar_msg_id()

                elif ev.key in (K_PLUS, K_KP_PLUS):
                    self.editor.aumentar_id()
                    self._refrescar_msg_id()

            elif ev.type == MOUSEMOTION:
                mx, my = ev.pos
                self.mouse.x = mx
                self.mouse.y = my
                self.enfocada = self.coords_matriz(mx, my)

            elif ev.type == EventosJuego.CONTAR_TIMERS:
                self._actualizar_timers()


        for iden, (_, temp) in self.mensajes.items():
            if not temp.esta_contando():
                self.refrescar_mensaje("", iden)
