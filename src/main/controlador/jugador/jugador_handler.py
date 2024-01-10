"""
Módulo para el handler de una instancia de jugador.
"""

from typing import TYPE_CHECKING, Optional

from pygame.constants import KEYDOWN

from ...modelo.jugador import EstadoJugador
from ...modelo.utils import Temporizador
from ...vista.sprites import SpritesManager
from ..controles import TiposAccion
from ..eventos import EventosJuego
from ...modelo.eventos import EventosSonidos

if TYPE_CHECKING:
    from os import PathLike

    from pygame import Surface
    from pygame.event import Event

    from ...modelo.jugador import Jugador
    from ...modelo.niveles import Nivel
    from ..controles import ControlesHandler
    from ..logger import LoggerJuego
    from ..sonidos import MotorSFX


# -- sprites --
SPRITES_JUGADOR: "PathLike" = "./media/sprites/jugador"
QUIETO: "PathLike" = f"{SPRITES_JUGADOR}/idle"
CAMINANDO_IZQ: "PathLike" = f"{SPRITES_JUGADOR}/walking_left"
CAMINANDO_DER: "PathLike" = f"{SPRITES_JUGADOR}/walking_right"
PARED_IZQ: "PathLike" = f"{SPRITES_JUGADOR}/grabbing_left"
PARED_DER: "PathLike" = f"{SPRITES_JUGADOR}/grabbing_right"
DASH_IZQ: "PathLike" = f"{SPRITES_JUGADOR}/dashing_left"
DASH_DER: "PathLike" = f"{SPRITES_JUGADOR}/dashing_right"
SALTANDO: "PathLike" = f"{SPRITES_JUGADOR}/jumping"
CAYENDO: "PathLike" = f"{SPRITES_JUGADOR}/falling"
# -------------


class JugadorHandler:
    """
    Clase que maneja los sprites y la vista de un jugador.
    La lógica de movimiento debería ser manejada por una instancia de juego; la única
    excepción a esto son los movimientos que requieren de teclas.
    """


    def __init__(self,
                 jugador: "Jugador",
                 sonidos: "MotorSFX",
                 controles: "ControlesHandler",
                 logger: Optional["LoggerJuego"]=None) -> None:
        """
        Inicializa el handler del jugador.
        -
        'jugador': La instancia de jugador a la que está asociada este handler.

        'sonidos': El motor de sonido.

        'controles': Los controles del juego.

        'logger': El registrador del juego.
        """

        self.jugador: "Jugador" = jugador
        self.sfx: "MotorSFX" = sonidos
        self.controles: "ControlesHandler" = controles
        self.logger: Optional["LoggerJuego"] = logger
        self.inv_sprites: Temporizador = Temporizador(10)
        self.dibujar_inv: bool = True

        self.sprites: SpritesManager = SpritesManager(
            pos=self.jugador.pos,
            tam=self.jugador.tam,
            rutas_anim={
                EstadoJugador.QUIETO: QUIETO,
                EstadoJugador.CAMINANDO_IZQ: CAMINANDO_IZQ,
                EstadoJugador.CAMINANDO_DER: CAMINANDO_DER,
                EstadoJugador.PARED_IZQ: PARED_IZQ,
                EstadoJugador.PARED_DER: PARED_DER,
                EstadoJugador.DASH_IZQ: DASH_IZQ,
                EstadoJugador.DASH_DER: DASH_DER,
                EstadoJugador.SALTANDO: SALTANDO,
                EstadoJugador.CAYENDO: CAYENDO
            },
            default=EstadoJugador.QUIETO
        )


    def _cambio_estado_jugador(self) -> bool:
        """
        Determina si desde el último ciclo, el estado de jugador es distinto.
        Si lo es, cambiar sprites y realizar otras actualizaciones acordes.
        """

        return self.jugador.estado != self.sprites.nombre_actual


    def _alternar_dibujar_inv(self) -> None:
        """
        Alterna el atributo de control que decide si dibujar el sprite del jugador
        cuando éste es invencible o no.
        """

        self.dibujar_inv = not self.dibujar_inv


    def procesar_teclas_jugador(self, eventos: list["Event"], nivel: "Nivel") -> None:
        """
        Procesa los movimientos del jugador que requieren de presionar una tecla.
        -
        'eventos': La lista de eventos de Pygame a procesar.
        """

        if self.controles.tecla_apretada(TiposAccion.IZQUIERDA):
            self.jugador.moverse_izquierda()
        if self.controles.tecla_apretada(TiposAccion.DERECHA):
            self.jugador.moverse_derecha()

        for ev in eventos:
            if ev.type == KEYDOWN:
                if (self.controles.pertenece_tecla(TiposAccion.SALTAR, ev.key)
                    and not self.jugador.salto_cooldown.esta_contando()):
                    if self.jugador.saltar(nivel):
                        self.sfx.mixer.play(self.sfx.sonidos["salto"])

                elif (self.controles.pertenece_tecla(TiposAccion.DASH, ev.key)
                      and not self.jugador.dash_cooldown.esta_contando()):
                    if self.jugador.dashear():
                        self.sfx.mixer.play(self.sfx.sonidos["dash"])


    def _actualizar_timers(self) -> None:
        "Actualiza toods los temporizadores del handler."

        if not self.inv_sprites.esta_contando():
            self._alternar_dibujar_inv()

        self.inv_sprites.actualizar(1, reiniciar=self.jugador.es_invulnerable())


    def actualizar(self, superficie: "Surface", eventos: list["Event"],
                   **kwargs) -> None:
        """
        Actualiza los eventos que le ocurren al jugador.
        -
        'superficie': La superficie (`pygame.Surface`) en donde se va a dibujar todos los
                      cambios visuales a aplicar.

        'eventos': La lista de eventos de Pygame a procesar.

        '**kwargs': Atributos extra.
        """

        self._actualizar_timers()

        for ev in eventos:
            if ev.type == EventosJuego.REDIBUJAR_JUGADOR:
                self.sprites.siguiente_frame()

            elif ev.type == EventosSonidos.DANIO:
                self.sfx.mixer.play(self.sfx.sonidos["danio"])

        self.procesar_teclas_jugador(eventos, kwargs.get("nivel"))

        if self._cambio_estado_jugador():
            self.sprites.cambiar_animacion(self.jugador.estado)
        self.sprites.cambiar_pos(self.jugador.pos)

        if self.jugador.es_invulnerable():
            if self.dibujar_inv:
                self.sprites.dibujar(superficie, alpha=100)
        else:
            self.sprites.dibujar(superficie)
