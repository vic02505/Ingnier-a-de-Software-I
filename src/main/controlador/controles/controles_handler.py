"""
Módulo para el handler de los controles del teclado y mouse.
"""

from typing import TYPE_CHECKING, Optional, TypeAlias

from pygame.key import get_pressed, key_code

from ..archivos import RutaJSON
from .tipos_acciones import TiposAccion

if TYPE_CHECKING:
    from os import PathLike

    from ..logger import LoggerJuego

ControlesDict: TypeAlias = dict[TiposAccion, list[str]]

CONTROLES_CONFIG: "PathLike" = "./config/controles.json"
CONTROLES_DEFAULT: ControlesDict = {
    TiposAccion.IZQUIERDA: ["a", "left"],
    TiposAccion.DERECHA: ["d", "right"],
    TiposAccion.SALTAR: ["space"],
    TiposAccion.DASH: ["c"]
}


class ControlesHandler:
    "Handler de los controles."

    def __init__(self,
                 controles: Optional[ControlesDict]=None,
                 logger: Optional["LoggerJuego"]=None) -> None:
        """
        Inicializa el handler de los controles.
        -
        'controles': Un diccionario de controles en los que las claves son uno de los tipos
                     de `TiposAccion`, y los valores son listas con identificadores de las teclas
                     o botones que activan dicha acción, según las constantes de Pygame.

        'logger': El registrador del juego.
        """

        self.ruta_configs: RutaJSON = RutaJSON(CONTROLES_CONFIG)

        self.controles: ControlesDict = (self.ruta_configs.cargar()
                                         if controles is None
                                         else controles)
        self.logger: Optional["LoggerJuego"] = logger

        if self.controles == {}: # Para prevenir que el juego no se pueda controlar
            self.controles = CONTROLES_DEFAULT


    def esta_repetido(self, tecla: str) -> bool:
        """
        Determina si una tecla está repetida.
        -
        'tecla'_ El nombre de la tecla a revisar.
        """

        for lista_teclas in self.controles.values():
            for tec in lista_teclas:
                if tecla == tec:
                    return True

        return False


    def como_codigos(self, accion: TiposAccion) -> list[int]:
        """
        Devuelve la lista de teclas asociadas a una acción, pero en vez de los nombres,
        devuelve las constantes usadas por pygame.
        -
        'accion': El nombre de la acción en cuestión.
        """

        return [key_code(tecla) for tecla in self.controles[accion]]


    def tecla_apretada(self, accion: TiposAccion) -> bool:
        """
        Determina si una tecla de las asociadas a una acción están apretadas.
        -
        'accion': El nombre de la acción en cuestión.
        """

        teclas = get_pressed()
        return any(teclas[key_code(tecla)] for tecla in self.controles[accion])


    def pertenece_tecla(self, accion: TiposAccion, tecla: int) -> bool:
        """
        Determina si una tecla, dada por su constante en Pygame, pertenece a un grupo asociado
        a una acción.
        -
        'accion': El nombre de la acción en cuestión.

        'tecla': La constante de Pygame de dicha tecla.
        """

        return tecla in self.como_codigos(accion)


    def quedan_pocas_teclas(self, accion: TiposAccion, piso: int=1) -> bool:
        """
        Determina si las teclas asociadas a una acción caen por debajo de cierto número.
        -
        'accion': El nombre de la acción en cuestión.

        'piso': La cantidad mínima aceptable de teclas asociadas. Por defecto debería haber
                al menos una.
        """

        return len(self.controles[accion]) <= piso


    def quitar_ultima_tecla(self, accion: TiposAccion) -> str:
        """
        Intenta devolver la última tecla asociada, la cual elimina de la lista.
        Si no lo logra, levanta una excepción.
        -
        'accion': La acción que se relaciona con las teclas.
        """

        if self.quedan_pocas_teclas(accion, 1):
            raise ValueError("Quedan demasiadas pocas teclas como para poder eliminarlas.")

        return self.controles[accion].pop()


    def guardar_config(self) -> None:
        """
        Guarda la configuración de controles para que persista en la siguiente
        ejecución del juego.
        """

        self.ruta_configs.guardar(self.controles)
        self.logger.info("Configuración de controles guardada")
