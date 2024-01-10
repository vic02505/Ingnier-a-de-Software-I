"""
Módulo para el estado del juego.
"""

from typing import TYPE_CHECKING, Optional, TypeAlias

from pygame.constants import K_ESCAPE, KEYDOWN
from pygame.display import get_surface
from pygame.event import Event
from pygame.event import post as ev_post

from ...controlador.eventos import EventosJuego
from ..eventos import EventosSonidos
from ..jugador import Jugador
from ..niveles import Nivel

if TYPE_CHECKING:
    from os import PathLike

    from pygame import Surface

RutasNiveles: TypeAlias = tuple["PathLike", ...]
TuplaVersion: TypeAlias = tuple[int, int, int, str]

# ----- Rutas de niveles -----
NIVEL_1: "PathLike" = "./niveles/default/nivel_1.nivel"
NIVEL_2: "PathLike" = "./niveles/default/nivel_2.nivel"
NIVEL_3: "PathLike" = "./niveles/default/nivel_3.nivel"
# ----------------------------


class Juego:
    "Clase maestra para el estado del juego."

    def __init__(self,
                 *,
                 gravedad: float=0.5,
                 friccion_plataforma: float=0.08,
                 friccion_aire: float=0.04,
                 niveles: tuple["PathLike", ...]=(NIVEL_1, NIVEL_2, NIVEL_3)
    ) -> None:
        """
        Inicializa el estado del juego.
        -
        'gravedad' Qué tan fuerte los objetos son atraídos hacia 'abajo'.

        'friccion_plataforma': Qué tanto el movimiento es impedido cuando se está en el suelo
                               o en paredes.

        'friccion_aire': Qué tanto el movimiento es impedido cuando se está en el aire.

        'niveles': La serie de niveles a pasar para ganar el juego.
        """

        if niveles == ():
            raise ValueError("Debe haber al menos 1 ruta de nivel en la lista.")

        self.jugador: Optional[Jugador] = None
        self.grav: float = gravedad
        self.fric_plat: float = friccion_plataforma
        self.fric_aire: float = friccion_aire

        # ---------- Niveles ---------
        self.rutas_niveles: RutasNiveles = niveles
        self.rutas_niveles_default: RutasNiveles = niveles
        self._ind_nivel: int = 0
        self.nivel_actual: Optional[Nivel] = None
        # ----------------------------

        # --- Atributos de control ---
        self.en_juego: bool = False
        # ----------------------------


    @property
    def version(self) -> TuplaVersion:
        """
        Devuelve una tupla con la versión del juego.
        Obedece el estilo X.Y.Z-A donde:
            - 'X' es la versión de parche mayor (cambios considerables retroincompatibles)
            - 'Y' es la versión de parche menor (cambios considerables retrocompatibles)
            - 'Z' es un posible parche rápido entre versiones (cambios menores retrocompatibles)
            - 'A' es un string que indica el estado de la build, como por ejemplo 'alpha',
              o 'Beta', etc...
        """

        return (1, 0, 0, "release")


    def jugar(self, preservar_vidas: bool=True) -> None:
        """
        Modifica los atributos correctos, tal que el juego entiende que se
        entra en un nivel.
        -
        'preservar_vidas': Si el jugador debería quedarse con las mismas vidas que en
        el nivel anterior.
        """

        self.en_juego = True
        if self.nivel_actual is None:
            self._ind_nivel = 0
        else:
            self._ind_nivel += 1

        self.cargar_nivel(ruta_nivel=self.rutas_niveles[self._ind_nivel],
                          ruta_sig=(self.rutas_niveles[self._ind_nivel + 1]
                                    if self._ind_nivel < (len(self.rutas_niveles) - 1) else None),
                          preservar_vidas=preservar_vidas)


    def cargar_nivel(self,
                     *,
                     ruta_nivel: Optional["PathLike"],
                     nivel: Optional[Nivel]=None,
                     ruta_sig: Optional["PathLike"]=None,
                     preservar_vidas: bool=True) -> None:
        """
        Carga el nivel desde una ruta específica.
        -
        'ruta_nivel': La ruta donde está el archivo de nivel.

        'nivel': Un objeto de nivel ya cargado se puede usar opcionalmente.

        'ruta_sig': La ruta del siguiente nivel.

        'preservar_vidas': Si el jugador debería quedarse con las mismas vidas que en
        el nivel anterior.
        """

        if ruta_nivel is None and nivel is None:
            raise ValueError("Se debe especificar o una ruta de nivel o un objeto nivel.")

        if nivel is None:
            self.nivel_actual = Nivel(ruta_nivel, ruta_sig)
        else:
            self.nivel_actual = nivel

        pos_x, pos_y = self.nivel_actual.pos_inicial
        incr_x, incr_y = self.nivel_actual.incremento_celda

        # El jugador siempre es un poquito más chico que las celdas
        incr_x_chic = incr_x * 0.9
        incr_y_chic = incr_y * 0.9

        if preservar_vidas and self.jugador is not None:
            vidas_inic = self.jugador.hp
        else:
            vidas_inic = None

        self.jugador = Jugador(incr_x * pos_x, incr_y * pos_y,
                               incr_x_chic, incr_y_chic,
                               vidas_iniciales=vidas_inic,

                               # Estos deben ser relativos al tamaño del nivel
                               poder_de_salto=incr_y * 0.32,
                               poder_de_dash=incr_x * 0.45)


    def reiniciar_niveles(self, nuevas_rutas: Optional[RutasNiveles]=None) -> None:
        """
        Reinicia el puntero de niveles de vuelta al primero.
        -
        'nuevas_rutas': En caso de querer el pack de niveles por otro, se especifica en
                        este parámetro.
        """

        if nuevas_rutas is not None and nuevas_rutas == ():
            raise ValueError("Las rutas de niveles deben tener al menos un valor.")

        self.rutas_niveles = (self.rutas_niveles_default
                              if nuevas_rutas is None else nuevas_rutas)
        self.nivel_actual = None
        self._ind_nivel = 0


    def salir(self) -> None:
        """
        Modifica los atributos correctos, tal que el juego entiende que se
        sale hacia los menus.
        """

        self.en_juego = False


    def se_esta_jugando(self) -> bool:
        "Averigua si el juego esta dentro de un nivel o no."

        return self.en_juego


    def perdio(self) -> bool:
        "Indica si el juego está perdido."

        return self.jugador.muerto()


    def gano(self) -> tuple[bool, bool]:
        """
        Verifica si el jugador gano el nivel, y si hay un siguiente nivel después de éste.
        """

        if self.nivel_actual is None:
            return False, False

        jug_x, jug_y = self.jugador.hitbox.center # pylint: disable=unpacking-non-sequence
        return (self.nivel_actual.jugador_sobre_salida(jug_x, jug_y),
                self.nivel_actual.sig is not None)


    def reiniciar_vel_jugador(self) -> None:
        "Reinicia la aceleración y trunca la velocidad si ésta cae a un valor muy chico."

        return self.jugador.reiniciar_vel()


    def reiniciar_pos_jugador(self) -> None:
        "Reinicia la posición del jugador en el nivel a su valor inicial."

        self.jugador.reiniciar_pos()


    def actualizar(self, eventos: list[Event]) -> None:
        """
        Actualiza el estado de juego. Esto es, corre el ciclo tal que refresca la pantalla
        y redibuja todo, a la vez que procesa los eventos que hayan ocurrido.
        -
        'eventos': La lista de eventos de Pygame a procesar.
        """

        _, alto = get_surface().get_size()
        self.jugador.actualizar(eventos)

        for ev in eventos:
            if ev.type == KEYDOWN:
                if ev.key == K_ESCAPE:
                    self.salir()

            elif ev.type == EventosJuego.PROCESAR_MOV_JUGADOR:
                self.jugador.procesar_mov(self.grav, self.fric_plat,
                                          self.fric_aire, self.nivel_actual)


        if self.jugador.hitbox.top - self.jugador.hitbox.height > alto:
            self.jugador.lastimar(2)
            self.reiniciar_pos_jugador()
            ev_post(Event(EventosSonidos.DANIO_FUERTE))
