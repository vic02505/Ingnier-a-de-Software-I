"""
Módulo para tests del temporizador.
"""

from random import randint
from unittest import TestCase

from src.main.modelo.utils.temporizador import *


class TemporizadorTest(TestCase):
    "Tests del temporizador."

    def test_1_no_inicializa_con_tiempo_negativo(self) -> None:
        "No debe inicializar con valores menores o iguales a 0."

        with self.assertRaises(ValueError):
            Temporizador(0.0)

        with self.assertRaises(ValueError):
            Temporizador(-27.6)


    def test_2_tiempo_actual_igual_al_inicial(self) -> None:
        "Al ser creado, el tiempo del temporizador debería ser igual al inicial."

        for _ in range(100):
            temp = Temporizador(randint(1, 10000))
            self.assertEqual(temp.actual, temp.inic)


    def test_3_al_terminar_queda_en_cero(self) -> None:
        "Debería quedarse en 0 cuando termina de contar."

        temp = Temporizador(randint(1, 1000))
        for _ in range(temp.inic):
            self.assertTrue(temp.esta_contando())
            temp.contar(1)

        self.assertEqual(temp.actual, 0.0)
        self.assertNotEqual(temp.actual, temp.inic)


    def test_4_descontar_solo_con_numeros_positivos(self) -> None:
        "No debería dejar descontar con números negativos o 0."

        temp = Temporizador(randint(1, 1000))

        with self.assertRaises(ValueError):
            temp.contar(0.0)

        with self.assertRaises(ValueError):
            temp.contar(-58.60)


    def test_5_al_reiniciar_vuelve_al_valor_inicial(self) -> None:
        "'Reiniciar' implica configurar el valor actual al inicial otra vez."

        # Descontamos primero
        temp = Temporizador(randint(1, 1000))
        for _ in range(temp.inic):
            temp.contar(1)

        temp.reiniciar()
        self.assertEqual(temp.actual, temp.inic)

        # Esto no cambia aunque se haga de nuevo
        temp.reiniciar()
        self.assertEqual(temp.actual, temp.inic)


    def test_6_porcentaje_vacio_es_cero(self) -> None:
        "Si el contador llegó a 0, su 'porcentaje' debería ser 0%"

        temp = Temporizador(randint(1, 1000))
        for _ in range(temp.inic):
            temp.contar(1)

        self.assertEqual(temp.porcentaje(), 0.0)


    def test_7_porcentaje_lleno_es_uno(self) -> None:
        "Si el contador se reinició o no contó todavía, su 'porcentaje' debería ser 100%"

        temp1 = Temporizador(randint(1, 1000))
        temp2 = Temporizador(randint(1, 1000))

        for _ in range(temp1.inic):
            temp1.contar(1)

        temp1.reiniciar()

        self.assertEqual(temp1.porcentaje(), 1.0)
        self.assertEqual(temp2.porcentaje(), 1.0)


    def test_8_contar_no_lo_deja_en_cero_pero_actualizar_si(self) -> None:
        "'Actualizar' es contar en el temporizador pero dejando en 0 si se sobrepasa."

        valor_muy_grande = 100000
        temp = Temporizador(1257.0)
        temp.contar(valor_muy_grande)

        self.assertNotEqual(temp.actual, 0.0)
        self.assertLess(temp.actual, 0.0)

        temp.reiniciar()
        temp.actualizar(valor_muy_grande)

        self.assertEqual(temp.actual, 0.0)


    def test_9_descuenta_mas_o_menos_bien_con_floats(self) -> None:
        "Al descontar con floats (que el caso debería ser raro) el error no debería ser tanto."

        temp = Temporizador(1000.0)

        temp.contar(12.7)
        self.assertAlmostEqual(temp.actual, 987.3)

        temp.contar(65.2)
        self.assertAlmostEqual(temp.actual, 922.1)

        temp.contar(170.3)
        self.assertAlmostEqual(temp.actual, 751.8)

        temp.contar(257.967)
        self.assertAlmostEqual(temp.actual, 493.833)

        temp.contar(493.701)
        self.assertAlmostEqual(temp.actual, 0.132)

        temp.contar(1200.01)
        self.assertLess(temp.actual, 0.0)
        self.assertNotAlmostEqual(temp.actual, 0.0)


    def test_10_agotar_salta_el_tiempo_a_cero(self) -> None:
        "El método 'agotar' debería vaciar el contador."

        temp = Temporizador(1000.0)

        self.assertTrue(temp.esta_contando())
        self.assertEqual(temp.inic, temp.actual)

        temp.contar(450.0)

        self.assertTrue(temp.esta_contando())
        self.assertGreater(temp.inic, temp.actual)

        temp.agotar()
        self.assertFalse(temp.esta_contando())
        self.assertEqual(temp.actual, 0.0)
