"""
Módulo para un nivel del juego.
"""

from math import degrees, radians
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional, TypeAlias

from pygame import Rect
from pygame.display import get_surface
from pygame.math import Vector2

from ..celdas import (Llave, PlataformaPincho, PlataformaSimple, Puerta,
                      Salida, TiposCelda, Trofeo)
from .info_celda import InfoCelda, MatrizInfoCeldas

if TYPE_CHECKING:
    from os import PathLike

    from ..celdas import Celda

InfoNivel: TypeAlias = dict[str, Any]
MatrizCeldas: TypeAlias = list[list[Optional["Celda"]]]

EXT: str = ".nivel"
COMENTARIO_CHAR: str = "#"
SEP = ","
RUTA_NIVELES_DEFAULT: "PathLike" = "./niveles"
CLASES_CELDAS: dict[TiposCelda, type["Celda"]] = {
    TiposCelda.PLATAFORMA: PlataformaSimple,
    TiposCelda.PINCHO: PlataformaPincho,
    TiposCelda.LLAVE: Llave,
    TiposCelda.PUERTA: Puerta,
    TiposCelda.TROFEO: Trofeo,
    TiposCelda.SALIDA: Salida
}


class ExtensionIncorrecta(Exception):
    "Cuando el archivo no tiene la extensión querida."


class JugadorNoEncontrado(Exception):
    "Cuando el jugador no se encuentra en la matriz de celdas."


class Nivel:
    "Clase de un nivel del juego."

    def __init__(self, ruta_nivel: "PathLike", sig_nivel: Optional["PathLike"]=None) -> None:
        """
        Inicializa un nivel.
        -
        'ruta_nivel': La ruta donde se encuentra el archivo de extensión '.nivel'
                      para cargar el nivel.

        'sig_nivel': Una mención a la ruta del siguiente nivel, en caso de querer guardarlo.
        """

        datos_nivel = self.cargar_desde_ruta(ruta_nivel)
        self.titulo: str = datos_nivel["titulo"]
        matriz_info: MatrizInfoCeldas = datos_nivel["matriz"]
        self.pos_inicial: Vector2 = Vector2(datos_nivel["pos_jugador"]) # En col/fil, NO pixeles

        self.matriz: MatrizCeldas = self.regenerar_matriz(matriz_info, (TiposCelda.AIRE,
                                                                        TiposCelda.POS_JUGADOR))

        self.victoria: bool = False
        self.sig: Optional["PathLike"] = sig_nivel


    @property
    def ancho(self) -> int:
        "Devuelve la cantidad de columnas de la matriz del nivel."

        return len(self.matriz[0])


    @property
    def alto(self) -> int:
        "Devuelve la cantidad de filas de la matriz del nivel."

        return len(self.matriz)


    @property
    def forma(self) -> tuple[int, int]:
        "Devuelve el ancho y alto de la matriz del nivel."

        return self.ancho, self.alto


    @property
    def incremento_celda(self) -> tuple[float, float]:
        "Devuelve el tamaño individual que cada celda ha de tener en el nivel."

        ancho_pantalla, alto_pantalla = get_surface().get_size()
        return ancho_pantalla / self.ancho, alto_pantalla / self.alto


    def coords_matriz(self, px_x: float, px_y: float) -> tuple[int, int]:
        """
        Dadas las coordenadas en pixeles del cursor, devuelve a qué casilla
        de la matriz cae.
        -
        'px_x/px_y': Las coordenadas del cursor, en pixeles.
        """

        incr_x, incr_y = self.incremento_celda
        return int(px_x / incr_x), int(px_y / incr_y)


    def existe(self, col: int, fil: int) -> bool:
        """
        Define si existe una celda en las coordenadas dadas.
        -
        'col/fil': La columna y fila de la matriz que se desea consultar.
        """

        return (0 <= col < self.ancho) and (0 <= fil < self.alto)


    def celda(self, col: int, fil: int) -> Optional["Celda"]:
        """
        Devuelve una celda en la matriz, dadas unas coordenadas.
        Utilizar este método se prefiere a acceder a la matriz interna.
        -
        'col/fil': La columna y fila de la matriz a la que se intenta acceder.
        """

        return self.matriz[fil][col]


    def trofeos(self) -> tuple[int, int]:
        """
        Devuelve la cantidad de trofeos que hay en el nivel, así como los que
        fueron recolectados.
        """

        ancho, alto = self.forma

        totales = 0
        recolectados = 0
        for j in range(alto):
            for i in range(ancho):
                celda = self.celda(i, j)
                if celda is not None and celda.tipo == TiposCelda.TROFEO:
                    totales += 1
                    if celda.recolectado:
                        recolectados += 1

        return recolectados, totales


    def jugador_sobre_salida(self, jug_x: int, jug_y: int) -> bool:
        """
        Dadas las coordenadas del jugador, decide si el jugador está sobre una
        celda de salida.
        -
        'jug_x/jug_y': Las coordenadas de ljugador, en PIXELES.
        """

        jug_col, jug_fil = self.coords_matriz(jug_x, jug_y)

        if not self.existe(jug_col, jug_fil):
            return False

        celda = self.celda(jug_col, jug_fil)
        return celda is not None and celda.tipo == TiposCelda.SALIDA


    @staticmethod
    def cargar_desde_ruta(ruta_nivel: "PathLike", ignorar_pos_jugador: bool=False) -> InfoNivel:
        """
        Carga una matriz de nivel desde una ruta.
        -
        'ruta_nivel': El directorio donde se encuentra el archivo de nivel.

        'ignorar_pos_jugador': Si debería ignorarse el hecho de que no haya una celda de jugador.
        """

        ruta = Path(ruta_nivel)

        if not ruta.exists():
            raise FileNotFoundError(f"El archivo '{ruta.as_posix()}' no existe.")

        if ruta.suffix.lower() != EXT.lower():
            raise ExtensionIncorrecta(f"El archivo '{ruta.as_posix()}' debería tener extensión "
                                      f"'{EXT.lower()}', pero termina en '{ruta.suffix.lower()}'")

        matriz = []
        j = 0
        jug_x, jug_y = None, None
        with ruta.open(mode="r", encoding="utf-8") as archivo:
            for linea in archivo:
                i = 0
                linea = "".join(linea.rstrip("\n").split(COMENTARIO_CHAR)[0])
                if not linea:
                    continue

                linea_matriz = []
                linea_celdas = linea.split()
                for info_raw in linea_celdas:
                    tipo, rotacion, visibilidad, c_id = info_raw.split(SEP)
                    if int(tipo) == TiposCelda.POS_JUGADOR:
                        jug_x, jug_y = i, j

                    linea_matriz.append(InfoCelda(TiposCelda(int(tipo)),
                                                  radians(float(rotacion)),
                                                  bool(int(visibilidad)),
                                                  int(c_id)))
                    i += 1

                matriz.append(linea_matriz)
                j += 1

        if not ignorar_pos_jugador and (jug_x is None or jug_y is None):
            raise JugadorNoEncontrado("No se pudo encontrar la celda de posición del jugador "
                                      "en esta matriz.")

        return  {
            "titulo": " ".join(ruta.stem.split("_")).upper(),
            "matriz": matriz,
            "pos_jugador": (jug_x, jug_y)
        }


    @staticmethod
    def exportar_nivel(matriz: MatrizInfoCeldas,
                       ruta_nivel: Optional["PathLike"]=None) -> None:
        """
        Exporta un nivel a un archivo para su uso posterior.
        -
        'matriz': La matriz llena de la información de celdas.

        'ruta_nivel': La ruta donde guardar el archivo. Si hay uno que se llama igual
                      se sobreescribe.
        """

        if ruta_nivel is None:
            ruta = Path(RUTA_NIVELES_DEFAULT) / f"nivel_prueba{EXT}"
        else:
            ruta = Path(ruta_nivel)

        if not ruta.parent.exists():
            ruta.parent.mkdir(parents=True, exist_ok=True)

        with ruta.open(mode="w", encoding="utf-8") as archivo:
            for fila in matriz:
                fila_str = []
                for info in fila:
                    tipo, rot, visib, c_id = info
                    fila_str.append(f"{tipo.value}{SEP}{degrees(rot)}{SEP}{int(visib)}"
                                    f"{SEP}{c_id}")
                archivo.write(f"{' '.join(fila_str)}\n")


    def regenerar_matriz(self,
                         matriz: MatrizInfoCeldas,
                         ignorar: tuple[TiposCelda, ...]) -> MatrizCeldas:
        """
        A partir de la información de las celdas, esta función genera otra matriz con
        los objetos inicializados que son dichas celdas.
        -
        'matriz': La matriz con la información de celdas.

        'ignorar': Una tupla de tipos de celda a los que ignorar. Para esos casos se creará un
                   espacio vacío en su lugar.
        """

        ancho, alto = get_surface().get_size()
        col, fil = len(matriz[0]), len(matriz)
        incr_x, incr_y = ancho / col, alto / fil
        matriz_celdas = []
        puertas = "puertas"
        llaves = "llaves"
        dic_ids = {}

        for j in range(fil):
            fila_celdas = []
            for i in range(col):
                tipo, rot, visibilidad, c_id = matriz[j][i]
                if c_id not in dic_ids:
                    dic_ids[c_id] = {puertas: [], llaves: []}
                if tipo in ignorar:
                    fila_celdas.append(None)
                    continue

                celda = CLASES_CELDAS[tipo](Rect(incr_x * i, incr_y * j,
                                                 incr_x, incr_y),
                                            rot=rot,
                                            vis=visibilidad)

                if tipo == TiposCelda.PUERTA:
                    dic_ids[c_id][puertas].append(celda)

                elif tipo == TiposCelda.LLAVE:
                    dic_ids[c_id][llaves].append(celda)

                fila_celdas.append(celda)

            matriz_celdas.append(fila_celdas)

        # Asocio todas las llaves con las puertas
        # pylint: disable=consider-using-dict-items
        for id_num in dic_ids:
            for puerta in dic_ids[id_num][puertas]:
                puerta.llaves_asociadas.extend(dic_ids[id_num][llaves])

            for llave in dic_ids[id_num][llaves]:
                llave.puertas_asociadas.extend(dic_ids[id_num][puertas])

        return matriz_celdas
