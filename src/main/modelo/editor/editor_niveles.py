"""
Módulo para el editor de niveles.
"""

from math import pi
from pathlib import Path
from typing import TYPE_CHECKING

from ...modelo.niveles import (EXT, RUTA_NIVELES_DEFAULT, InfoCelda,
                               MatrizInfoCeldas, Nivel)
from ..celdas import TiposCelda

if TYPE_CHECKING:
    from os import PathLike

    from ..niveles import InfoNivel


MAX_ID: int = 100


class EditorNiveles:
    "Clase para el editor de niveles."

    def __init__(self,
                 *,
                 col_inic: int=32,
                 fil_inic: int=16) -> None:
        """
        Inicializa el editor de niveles.
        -
        'col_inic/fil_inic': Las columnas/filas iniciales de la matriz de celdas.
        """

        self.matriz: MatrizInfoCeldas = self.generar_matriz(col_inic, fil_inic)
        self.tipos_celdas: list[TiposCelda] = list(TiposCelda)

        self._celda_ind: int = 0
        self.celda_sostenida: TiposCelda = self.tipos_celdas[self._celda_ind]
        self.rot_sostenida: float = 0.0
        self.visibilidad_sostenida: bool = True
        self.id_sostenido: int = 0


    def sig_tipo(self) -> TiposCelda:
        "Cambia el tipo de celda sostenida por el siguiente en la lista."

        self._celda_ind = (self._celda_ind + 1) % len(self.tipos_celdas)
        self.celda_sostenida = self.tipos_celdas[self._celda_ind]
        return (self.celda_sostenida
                if self.celda_sostenida != TiposCelda.AIRE
                else self.sig_tipo())


    def ant_tipo(self) -> TiposCelda:
        "Cambia el tipo de celda sostenida por el anterior en la lista."

        self._celda_ind = (self._celda_ind - 1) % len(self.tipos_celdas)
        self.celda_sostenida = self.tipos_celdas[self._celda_ind]
        return (self.celda_sostenida
                if self.celda_sostenida != TiposCelda.AIRE
                else self.ant_tipo())


    def rotar(self, drot: float) -> float:
        """
        Cambia el estado de rotación de la celda sostenida.
        -
        'drot': La diferencia de rotación, en radianes. Si drot > 0 la rotación se hace
                en sentido ANTIHORARIO; si por el contrario drot < 0 se hace en sentido HORARIO.
        """

        self.rot_sostenida = (self.rot_sostenida + drot) % (2 * pi)
        return self.rot_sostenida


    def reiniciar_rot(self) -> None:
        "Devuelve la rotación a 0."

        self.rot_sostenida = 0.0


    def alternar_visibilidad(self) -> bool:
        "Cambia entre visible y no visible."

        self.visibilidad_sostenida = not self.visibilidad_sostenida
        return self.visibilidad_sostenida


    @property
    def forma(self) -> tuple[int, int]:
        "Devuelve las dimensiones de la matriz."

        return len(self.matriz[0]), len(self.matriz)


    def generar_matriz(self, ancho: int, alto: int) -> MatrizInfoCeldas:
        """
        Genera una matriz de un tamaño específico.
        -
        'ancho/alto': El número de columnas/filas a usar en la matriz.
        """

        matriz = []
        for _ in range(alto):
            fila = []
            for _ in range(ancho):
                fila.append(InfoCelda())
            matriz.append(fila)

        return matriz


    def cambiar_celda(self, ancho: int, alto: int) -> InfoCelda:
        """
        Cambia una celda de la matriz.
        -
        'ancho/alto': Las coordenadas de la celda de la matriz.
        """

        self.matriz[alto][ancho] = InfoCelda(self.celda_sostenida,
                                             self.rot_sostenida,
                                             self.visibilidad_sostenida,
                                             self.id_sostenido)
        return self.matriz[alto][ancho]


    def borrar_celda(self, ancho: int, alto: int) -> InfoCelda:
        """
        Borra la celda en una posición dada.
        -
        'ancho/alto': Las coordenadas de la celda de la matriz.
        """

        if self.matriz[alto][ancho].tipo != TiposCelda.AIRE:
            self.matriz[alto][ancho] = InfoCelda()

        return self.matriz[alto][ancho]


    def ocupado(self, ancho: int, alto: int) -> bool:
        """
        Verifica si una celda no está ocupada por aire.
        -
        'ancho/alto': Las coordenadas de la celda de la matriz.
        """

        return self.matriz[alto][ancho].tipo != TiposCelda.AIRE


    def es_visible(self, ancho: int, alto: int) -> bool:
        """
        Verifica si una celda es visible.
        -
        'ancho/alto': Las coordenadas de la celda de la matriz.
        """

        return self.matriz[alto][ancho].visible


    def existe_jugador(self) -> bool:
        "Verifica si existe la celda de posición del jugador."

        ancho, alto = self.forma
        for j in range(alto):
            for i in range(ancho):
                if self.matriz[j][i].tipo == TiposCelda.POS_JUGADOR:
                    return True

        return False


    def aumentar_id(self) -> int:
        "Intenta aumentar el id sostenido en 1."

        if self.id_sostenido < MAX_ID:
            self.id_sostenido += 1

        return self.id_sostenido


    def disminuir_id(self) -> int:
        "Intenta disminuir el id sostenido en 1."

        if self.id_sostenido > 0:
            self.id_sostenido -= 1

        return self.id_sostenido


    def set_ancho(self, ancho: int) -> None:
        """
        Modifica el ancho de la matriz.
        -
        'ancho': El ancho objetivo de la matriz.
        """

        ed_ancho, _ = self.forma

        dif = ancho - ed_ancho
        if dif == 0:
            return

        if dif <= -ed_ancho:
            dif = -ed_ancho + 1

        self.extender_ancho(dif)


    def extender_ancho(self, cuanto: int) -> None:
        """
        Extiende o contrae el ancho de la matriz.
        -
        'cuanto': Cuántas columnas agregar o sacar.
        """

        ed_ancho, _ = self.forma

        if cuanto == 0:
            return
        if cuanto <= -ed_ancho:
            cuanto = -ed_ancho + 1

        if cuanto > 0:
            for fila in self.matriz:
                fila.extend([InfoCelda() for _ in range(cuanto)])

        elif cuanto < 0:
            for fila in self.matriz:
                for _ in range(abs(cuanto)):
                    fila.pop()


    def set_alto(self, alto: int) -> None:
        """
        Modifica el alto de la matriz.
        -
        'alto': El alto objetivo de la matriz.
        """

        _, ed_alto = self.forma

        dif = alto - ed_alto
        if dif == 0:
            return

        if dif <= -ed_alto:
            dif = -ed_alto + 1

        self.extender_alto(dif)


    def extender_alto(self, cuanto: int) -> None:
        """
        Extiende o contrae el alto de la matriz.
        -
        'cuanto': Cuántas filas agregar o sacar.
        """

        ed_ancho, ed_alto = self.forma

        if cuanto == 0:
            return
        if cuanto <= -ed_alto:
            cuanto = -ed_alto + 1

        if cuanto > 0:
            for _ in range(cuanto):
                self.matriz.append([InfoCelda() for _ in range(ed_ancho)])

        elif cuanto < 0:
            for _ in range(abs(cuanto)):
                self.matriz.pop()


    def importar(self, titulo: str) -> "InfoNivel":
        """
        Importa un nivel desde un archivo con el nombre dado.
        -
        'titulo': El nombre del archivo.
        """

        ruta_nivel = Path(RUTA_NIVELES_DEFAULT) / f"{'_'.join(titulo.lower().split())}{EXT}"
        datos_nivel = Nivel.cargar_desde_ruta(ruta_nivel, ignorar_pos_jugador=True)
        self.matriz = datos_nivel["matriz"]

        return datos_nivel


    def exportar(self, titulo: str) -> "PathLike":
        """
        Exporta el nivel a un archivo con nombre.
        -
        'titulo': El nombre del archivo.
        """

        ruta = Path(RUTA_NIVELES_DEFAULT) / f"{'_'.join(titulo.lower().split())}{EXT}"
        Nivel.exportar_nivel(self.matriz, ruta.as_posix())

        return ruta.as_posix()
