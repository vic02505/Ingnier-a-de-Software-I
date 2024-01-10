"""
Módulo para la clase del jugador.
"""

from typing import TYPE_CHECKING, Callable, Optional, TypeAlias

from pygame import Rect
from pygame.display import get_surface
from pygame.math import Vector2

from ...controlador.eventos import EventosJuego
from ..utils import Temporizador
from .estado_jugador import EstadoJugador

if TYPE_CHECKING:
    from pygame import Surface
    from pygame.event import Event

    from ..celdas import Celda
    from ..niveles import Nivel

TuplaColision: TypeAlias = tuple[bool, Optional["Celda"], bool]
CondColision: TypeAlias = Callable[["Celda"], bool]


class Jugador:
    "Clase del jugador."

    def __init__(self,
                 pos_x: float,
                 pos_y: float,
                 tam_x: int=64,
                 tam_y: int=64,
                 *,
                 vidas_maximas: int=8,
                 vidas_iniciales: Optional[int]=None,
                 aceleracion: float=0.5,
                 poder_de_salto: float=17.0,
                 poder_de_dash: float=25.0,
                 salto_cooldown: float=100.0,
                 dash_cooldown: float=1000.0) -> None:
        """
        Inicializa el jugador.
        -
        'pos_x/pos_y': La posición inicial del jugador.
    
        'tam_x/tam_y': El tamaño (en pixeles) del jugador.

        'vidas_maximas': La cantidad máxima de veces que el jugador puede
                         recibir daño antes de morir.

        'vidas_iniciales': La cantidad de vidas con la que el jugador empieza inicialmente.

        'aceleracion': Un factor que afecta qué tan rápido acelera el jugador.

        'poder_de_dash': Un factor que mide qué tan fuerte es el impulso al moverse horizontalmente.

        'poder_de_salto': Un factor que mide qué tan fuerte es el impulso al saltar verticalmente.

        'salto_cooldown/dash_cooldown': El tiempo que requiere el jugador para saltar o
                                        impulsarse de nuevo, en milisegundos.
        """

        if vidas_maximas <= 0:
            raise ValueError(f"Valor vidas={vidas_maximas} no válido. "
                             "Debe ser un número entero positivo.")

        self.pos_inicial: Vector2 = Vector2(pos_x, pos_y) # Esto sí es en pixeles
        self.hitbox: Rect = Rect(pos_x, pos_y,
                                 tam_x, tam_y)
        self.max_hp: int = vidas_maximas
        self.hp: int = (vidas_iniciales if vidas_iniciales is not None else vidas_maximas)
        self.acc_fact: float = aceleracion
        self.salto: float = poder_de_salto
        self.dash: float = poder_de_dash
        self.mira_derecha: bool = True # O mira a derecha o mira hacia la izquierda

        self.vel: Vector2 = Vector2(0, 0)
        self.acc: Vector2 = Vector2(0, 0)

        # Si la velocidad cae por debajo de este valor, entenderla como cero
        self.tol_vel: float = self.acc_fact - 0.1
        self.estado: EstadoJugador = EstadoJugador.QUIETO

        # --- Cooldowns ---
        self.invulnerabilidad: Temporizador = Temporizador(2000)
        self.salto_cooldown: Temporizador = Temporizador(salto_cooldown)
        self.dash_cooldown: Temporizador = Temporizador(dash_cooldown)
        # -----------------


    @property
    def pos(self) -> Vector2:
        "Devuelve la posición del jugador (o más epecíficamente, de su hitbox)."

        return Vector2(self.hitbox.x, self.hitbox.y)


    @pos.setter
    def pos(self, nueva_pos: Vector2) -> None:
        "Redefine la posición del jugador."

        if not isinstance(nueva_pos, Vector2):
            return

        pos_x, pos_y = nueva_pos
        self.hitbox.x = pos_x
        self.hitbox.y = pos_y


    @property
    def tam(self) -> Vector2:
        "Devuelve el tamaño del jugador (o más epecíficamente, de su hitbox)."

        return Vector2(self.hitbox.width, self.hitbox.height)


    def lastimar(self, cantidad: int) -> None:
        """
        Le hace daño al jugador.
        -
        'cantidad': Las vidas que pierde.
        """

        if self.hp > 0 and not self.es_invulnerable():
            self.hp -= cantidad
            if self.hp < 0:
                self.hp = 0

            self.invulnerabilidad.reiniciar()


    def matar(self) -> None:
        "Mata instantáneamente al jugador."

        self.lastimar(self.hp)


    def muerto(self) -> bool:
        "Verifica si el jugador se quedó sin vidas."

        return self.hp <= 0


    def cambiar_estado(self, nuevo_estado: EstadoJugador) -> None:
        """
        Cambia el estado del jugador.
        -
        'nuevo_estado': El nuevo estado del jugador.
        """

        if isinstance(nuevo_estado, EstadoJugador):
            self.estado = nuevo_estado


    def coords_nivel(self, nivel: "Nivel") -> tuple[int, int]:
        """
        Devuelve a qué celda del nivel pertenece la posición actual del jugador.
        -
        'nivel': El nivel en cuestión.
        """

        px_x, px_y = self.hitbox.center # pylint: disable=unpacking-non-sequence
        return nivel.coords_matriz(px_x, px_y)


    def reiniciar_pos(self, reiniciar_vel: bool=True, reiniciar_acc: bool=True) -> None:
        """
        Reinicia la posición del jugador a la inicial.
        -
        'reiniciar_vel/reiniciar_acc': Decidir si reiniciar también la velocidad
                                       y aceleración.
        """

        self.pos = Vector2(self.pos_inicial)

        if reiniciar_vel:
            self.vel = Vector2(0, 0)

        if reiniciar_acc:
            self.acc = Vector2(0, 0)


    def _colisiona_con_celda(self,
                             nivel: "Nivel",
                             cond_extra: CondColision=lambda celda: True) -> TuplaColision:
        """
        Determina si el jugador colisionó con alguna celda del nivel, más
        una condición extra.
        -
        'nivel': El nivel actual del juego con sus celdas, con las que verificar colisiones.
        """

        col, fil = nivel.forma

        for j in range(fil):
            for i in range(col):
                celda = nivel.celda(i, j)
                if celda is None:
                    continue

                if celda.rect.colliderect(self.hitbox) and cond_extra(celda):
                    return True, celda

        return False, None


    def esta_en_piso(self, nivel: "Nivel") -> TuplaColision:
        """
        Determina si el jugador está 'en el suelo'. Esto sucede cuando el
        jugador NO está en el aire o agarrado a las paredes.
        Devuelve si colisionó y con qué celda lo hizo si es así.
        -
        'nivel': El nivel actual del juego con sus celdas, con las que verificar colisiones.
        """

        jug_x, jug_y = self.coords_nivel(nivel)
        for dx in (0, -1, 1):
            if not nivel.existe(jug_x + dx, jug_y + 1):
                continue

            celda = nivel.celda(jug_x + dx, jug_y + 1)
            if celda is None:
                continue

            cond = True

            if dx == -1:
                cond = (celda.rect.top <= self.hitbox.bottom
                        and celda.rect.right >= self.hitbox.left
                )
            elif dx == 0:
                cond = celda.rect.top <= self.hitbox.bottom
            elif dx == 1:
                cond = (celda.rect.top <= self.hitbox.bottom
                        and celda.rect.left <= self.hitbox.right
                )

            if (celda.es_tangible()
                and cond):
                return True, celda, dx == 0

        return False, None, False


    def choca_con_pared_izq(self,
                            nivel: "Nivel",
                            en_piso: bool=False,
                            en_techo: bool=False) -> TuplaColision:
        """
        Determina si el jugador está agarrado a una pared a su izquierda.
        -
        'nivel': El nivel actual del juego con sus celdas, con las que verificar colisiones.

        'en_piso': Si el jugador está ya en el piso. En cuyo caso, ignorar el vecino de
                   abajo a la izquierda, pues ése se entiende como piso, no pared.

        'en_techo': Similar al piso, ignorar la esquina correspondiente si ya se está
                    chocando con el techo.
        """

        jug_x, jug_y = self.coords_nivel(nivel)
        for dy in (0, -1, 1):
            if not nivel.existe(jug_x - 1, jug_y + dy):
                continue

            celda = nivel.celda(jug_x - 1, jug_y + dy)
            if celda is None:
                continue

            cond = True

            if dy == -1:
                cond = (not en_techo
                        and celda.rect.right >= self.hitbox.left
                        and celda.rect.bottom >= self.hitbox.top
                        and (celda.rect.right - self.hitbox.left) <=
                            (celda.rect.bottom - self.hitbox.top)
                )
            elif dy == 0:
                cond = celda.rect.right >= self.hitbox.left
            elif dy == 1:
                cond = (not en_piso
                        and celda.rect.right >= self.hitbox.left
                        and celda.rect.top <= self.hitbox.bottom
                        and (celda.rect.right - self.hitbox.left) <=
                            (celda.rect.top - self.hitbox.bottom)
                )

            if (celda.es_tangible()
                and cond):
                return True, celda, dy == 0

        return False, None, False


    def choca_con_pared_der(self,
                            nivel: "Nivel",
                            en_piso: bool=False,
                            en_techo: bool=False) -> TuplaColision:
        """
        Determina si el jugador está agarrado a una pared a su derecha.
        -
        'nivel': El nivel actual del juego con sus celdas, con las que verificar colisiones.

        'en_piso': Si el jugador está ya en el piso. En cuyo caso, ignorar el vecino de
                   abajo a la izquierda, pues ése se entiende como piso, no pared.

        'en_techo': Similar al piso, ignorar la esquina correspondiente si ya se está
                    chocando con el techo.
        """

        jug_x, jug_y = self.coords_nivel(nivel)
        for dy in (0, -1, 1):
            if not nivel.existe(jug_x + 1, jug_y + dy):
                continue

            celda = nivel.celda(jug_x + 1, jug_y + dy)
            if celda is None:
                continue

            cond = True

            if dy == -1:
                cond = (not en_techo
                        and celda.rect.left <= self.hitbox.right
                        and celda.rect.bottom >= self.hitbox.top
                        and (celda.rect.left - self.hitbox.right) <=
                            (celda.rect.bottom - self.hitbox.top)
                )
            elif dy == 0:
                cond = celda.rect.left <= self.hitbox.right
            elif dy == 1:
                cond = (not en_piso
                        and celda.rect.left <= self.hitbox.right
                        and celda.rect.top <= self.hitbox.bottom
                        and (celda.rect.left - self.hitbox.right) <=
                            (celda.rect.top - self.hitbox.bottom)
                )

            if (celda.es_tangible()
                and cond):
                return True, celda, dy == 0

        return False, None, False


    def esta_en_techo(self, nivel: "Nivel") -> TuplaColision:
        """
        Determina si el jugador está 'en el techo'.
        Devuelve si colisionó y con qué celda lo hizo si es así.
        -
        'nivel': El nivel actual del juego con sus celdas, con las que verificar colisiones.
        """

        jug_x, jug_y = self.coords_nivel(nivel)
        for dx in (0, -1, 1):
            if not nivel.existe(jug_x + dx, jug_y - 1):
                continue

            celda = nivel.celda(jug_x + dx, jug_y - 1)
            if celda is None:
                continue

            cond = True

            if dx == -1:
                cond = (celda.rect.bottom >= self.hitbox.top
                        and celda.rect.right >= self.hitbox.left
                )
            elif dx == 0:
                cond = celda.rect.bottom >= self.hitbox.top
            elif dx == 1:
                cond = (celda.rect.bottom >= self.hitbox.top
                        and celda.rect.left <= self.hitbox.right
                )

            if (celda.es_tangible()
                and cond):
                return True, celda, dx == 0

        return False, None, False


    def esta_quieto(self) -> bool:
        "Determina si la velocidad del jugador es cero, y su aceleración tampoco cambia."

        return self.vel == (0, 0) and self.acc == (0, 0)


    def esta_en_pared(self) -> bool:
        "Verifica si el jugador actualmente se está agarrando de una pared."

        return self.estado in (EstadoJugador.PARED_IZQ, EstadoJugador.PARED_DER)


    def esta_cayendo(self) -> bool:
        "Verifica si el jugador actualmente está siendo afectado por la gravedad."

        return self.vel.y > 0


    def esta_dasheando(self) -> bool:
        "Verifica si el jugador recientemente recibió un impulso horizontal."

        return self.dash_cooldown.porcentaje() > 0.6


    def es_invulnerable(self) -> bool:
        "Verifica si el jugador es inmune al daño."

        return self.invulnerabilidad.esta_contando()


    def moverse_izquierda(self) -> None:
        """
        Se mueve hacia a la izquierda.
        """

        self.acc.x += -self.acc_fact
        self.mira_derecha = False


    def moverse_derecha(self) -> None:
        """
        Se mueve hacia a la derecha.
        """

        self.acc.x += self.acc_fact
        self.mira_derecha = True


    def efectuar_salto(self) -> None:
        "Realiza el salto del jugador."

        self.vel.y = -self.salto
        self.salto_cooldown.reiniciar()


    def saltar(self, nivel: Optional["Nivel"]=None) -> bool:
        """
        Se impulsa verticalmente. Devuelve un booleano dependiendo de si
        logró hacer el salto o no.
        -
        'nivel': Una posible instancia de nivel, para verificar colisiones con el suelo.
        """

        exito = False

        if nivel is not None and self.esta_en_piso(nivel)[0]:
            self.efectuar_salto()
            exito = True

        elif self.esta_en_pared():
            direccion = (-1 if self.mira_derecha else 1) # Al revés a propósito
            self.efectuar_salto()
            self.vel.x = direccion * self.salto * 0.3
            exito = True

        return exito


    def dashear(self) -> None:
        """
        Se impulsa horizontalmente. Devuelve un booleano dependiendo de si
        logró hacer el dash o no.
        """

        exito = True

        self.vel.x += (1 if self.mira_derecha else -1) * self.dash
        self.dash_cooldown.reiniciar()

        return exito


    def _actualizar_timers(self) -> None:
        "Va contando todos los timers que tiene el jugador."

        self.invulnerabilidad.actualizar(1)
        self.salto_cooldown.actualizar(1)
        self.dash_cooldown.actualizar(1)


    def actualizar_estado_x(self) -> None:
        "Actualiza el estado de movimiento horizontal."

        self.cambiar_estado(EstadoJugador.CAMINANDO_IZQ if self.vel.x < 0
                            else EstadoJugador.CAMINANDO_DER)


    def actualizar_estado_caida_libre(self) -> None:
        "Actualiza el estado de movimiento vertical."

        if not self.esta_en_pared():
            self.cambiar_estado(EstadoJugador.SALTANDO if not self.esta_cayendo()
                                else EstadoJugador.CAYENDO)


    def actualizar_estado_dash(self) -> None:
        "Actualiza el estado de impulso horizontal."

        if self.vel.x < 0:
            self.cambiar_estado(EstadoJugador.DASH_IZQ)

        elif self.vel.x > 0:
            self.cambiar_estado(EstadoJugador.DASH_DER)


    def reiniciar_vel(self) -> None:
        "Reinicia la aceleración y trunca la velocidad si ésta cae a un valor muy chico."

        self.acc.x = 0
        if abs(self.vel.x) <= self.tol_vel:
            self.vel.x = 0


    def actualizar(self, eventos: list["Event"]) -> None:
        """
        Actualiza todo lo relacionado al jugador.
        -
        'eventos': La lista de eventos de Pygame a procesar.
        """

        for ev in eventos:
            if ev.type == EventosJuego.CONTAR_TIMERS:
                self._actualizar_timers()


    def procesar_mov(self,
                     grav: float,
                     fric_plat: float,
                     fric_aire: float,
                     nivel: "Nivel") -> None:
        """
        Procesa el movimiento del jugador.
        -
        'grav': El factor de gravedad que afecta al jugador.

        'fric_plat/fric_aire': La fricción que el jugador experimento en plataformas o en el aire.

        'nivel': El nivel actual del juego con sus celdas, con las que verificar colisiones.
        """

        ancho, _ = get_surface().get_size()

        # ecuaciones horarias de posición
        self.acc.x += self.vel.x * (-fric_plat
                                    if self.esta_en_piso(nivel)[0]
                                    else -fric_aire)
        self.vel += self.acc
        self.pos += (self.vel + 0.5 * self.acc)

        if self.hitbox.left > ancho:
            self.hitbox.right = 0
        if self.hitbox.right < 0:
            self.hitbox.left = ancho

        self.actualizar_estado_x()

        en_piso, celda_piso, dir_piso = self.esta_en_piso(nivel)
        en_techo, celda_techo, dir_techo = self.esta_en_techo(nivel)
        choca_izq, celda_izq, _dir_izq = self.choca_con_pared_izq(nivel, en_piso, en_techo)
        choca_der, celda_der, _dir_der = self.choca_con_pared_der(nivel, en_piso, en_techo)

        if choca_izq:
            celda_izq.efecto_jug_der(self)
            self.cambiar_estado(EstadoJugador.PARED_IZQ)

        elif choca_der:
            celda_der.efecto_jug_izq(self)
            self.cambiar_estado(EstadoJugador.PARED_DER)

        if en_techo:
            if not ((choca_izq or choca_der) and not dir_techo):
                celda_techo.efecto_jug_abajo(self)

        if en_piso:
            if not ((choca_izq or choca_der) and not dir_piso):
                celda_piso.efecto_jug_arriba(self)
        else:
            if self.esta_en_pared() and self.esta_cayendo():
                self.acc.y = grav * 0.1
            else:
                self.actualizar_estado_caida_libre()
                self.acc.y = grav

        if self.esta_dasheando():
            self.actualizar_estado_dash()

        if self.esta_quieto():
            self.cambiar_estado(EstadoJugador.QUIETO)
