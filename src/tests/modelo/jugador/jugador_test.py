"""
Módulo para tests del jugador.
"""

from typing import TYPE_CHECKING
from unittest import TestCase
from random import choice

from pygame.constants import HIDDEN
from pygame.display import set_mode

from src.main.main import ANCHO_PANTALLA, ALTO_PANTALLA
from src.main.modelo.jugador import Jugador, EstadoJugador
from src.main.modelo.niveles import Nivel

if TYPE_CHECKING:
    from os import PathLike
    from pygame import Surface

NIVEL_TEST: "PathLike" = "./niveles/testing/collision_test.nivel"


class JugadorTest(TestCase):
    "Tests del jugador."

    def __init__(self, methodName: str="runTest") -> None:
        "Inicializa las pruebas del jugador."

        super().__init__(methodName)

        self.pantalla: "Surface" = set_mode((ANCHO_PANTALLA, ALTO_PANTALLA), flags=HIDDEN)


    def setUp(self) -> None:
        "Crea objetos comunes a todos los tests antes de correrlos."

        ancho, alto = self.pantalla.get_size()
        self.jug: Jugador = Jugador(ancho // 2, alto // 2)
        self.grav: float = 0.5
        self.fric_suelo: float = 0.08
        self.fric_aire: float = 0.04
        self.nivel: Nivel = Nivel(NIVEL_TEST)


    def test_1_al_ser_creado_esta_quieto(self) -> None:
        """
        Debería empezar con el estado EstadoJugador.QUIETO, y tener velocidad
        y aceleración nulas.
        """

        self.assertEqual(self.jug.estado, EstadoJugador.QUIETO)
        self.assertEqual(self.jug.vel, (0, 0))
        self.assertEqual(self.jug.acc, (0, 0))
        self.assertTrue(self.jug.esta_quieto())


    def test_2_pos_es_igual_a_la_hitbox(self) -> None:
        """
        'Jugador.pos' es un alias a las coordenadas de la hitbox, así que deberían cambiar los
        valores al mismo tiempo.
        """

        self.assertEqual(self.jug.pos.x, self.jug.hitbox.x)
        self.assertEqual(self.jug.pos.y, self.jug.hitbox.y)

        self.jug.pos += (12, -56)

        self.assertEqual(self.jug.pos.x, self.jug.hitbox.x)
        self.assertEqual(self.jug.pos.y, self.jug.hitbox.y)

        self.jug.pos += (-120, 28)

        self.assertEqual(self.jug.pos.x, self.jug.hitbox.x)
        self.assertEqual(self.jug.pos.y, self.jug.hitbox.y)


    def test_3_mira_correctamente_a_los_lados(self) -> None:
        "Si se mueve hacia una dirección horizontal, está 'mirando' hacia allí."

        self.jug.moverse_derecha()
        self.jug.vel += self.jug.acc
        self.assertTrue(self.jug.mira_derecha)

        self.jug.actualizar_estado_x()
        self.assertEqual(self.jug.estado, EstadoJugador.CAMINANDO_DER)

        # Para cancelar el movimiento a la derecha
        self.jug.acc.x = 0
        self.jug.vel.x = 0

        self.jug.moverse_izquierda()
        self.jug.vel += self.jug.acc
        self.assertFalse(self.jug.mira_derecha)

        self.jug.actualizar_estado_x()
        self.assertEqual(self.jug.estado, EstadoJugador.CAMINANDO_IZQ)


    def test_4_si_no_se_mueve_horizontalmente_cae_vertical(self) -> None:
        "Si el jugador no está apretando teclas, el personaje debe caer verticalmente."

        pos_x, pos_y = self.jug.pos
        self.assertEqual(self.jug.acc.y, 0)
    
        self.jug.procesar_mov(self.grav, self.fric_suelo, self.fric_aire, self.nivel)

        self.assertEqual(self.jug.pos.x, pos_x)
        self.assertEqual(self.jug.pos.y, pos_y)
        self.assertEqual(self.jug.acc.y, self.grav)


    def test_5_usa_el_poder_de_salto(self) -> None:
        "El impulso de salto debe ser igual al atributo correspondiente."

        self.jug.efectuar_salto()
        self.assertEqual(self.jug.vel.y, -self.jug.salto)


    def test_6_usa_el_poder_de_dash(self) -> None:
        "El impulso horizontal debería tener el factor de dash."

        for _ in range(50):
            self.jug.mira_derecha = choice((True, False))
            direccion = (1 if self.jug.mira_derecha else -1)

            while self.jug.dash_cooldown.esta_contando():
                self.jug.dash_cooldown.actualizar(1)

            self.jug.dashear()
            self.assertEqual(self.jug.vel.x, direccion * (self.jug.dash))

            # Para que en el siguiente ciclo no se sumen
            self.jug.vel.x = 0
