"""
Módulo para un manejador de archivos JSON.
"""

from json import dump, load
from pathlib import Path
from typing import TYPE_CHECKING, Any, TypeAlias

if TYPE_CHECKING:
    from os import PathLike

DicJson: TypeAlias = dict[str, Any]

ENCODING: str = "utf-8"
EXT: str = ".json"


class FormatoIncorrecto(Exception):
    "Cuando el nombre del archivo tiene un formato que no es válido."


class RutaJSON:
    "Manejador de archivo JSON."

    def __init__(self, ruta_archivo: "PathLike") -> None:
        """
        Inicializa el manejador de ruta.
        -
        ruta_archivo: La ruta del archivo. De no existir, la crea.
        """

        self.ruta: Path = Path(ruta_archivo)
        if self.ruta.suffix.lower() != EXT.lower():
            raise FormatoIncorrecto(f"La ruta '{self.ruta.as_posix()}' debería terminar con "
                                    f"el sufijo '{EXT.lower()}', pero termina en "
                                    f"'{self.ruta.suffix.lower()}'.")

        self._crear_si_no_existe()


    def _crear_si_no_existe(self) -> None:
        "Si el archivo no existe, crea un JSON nuevo."

        if not self.ruta.exists():
            self.ruta.parent.mkdir(parents=True, exist_ok=True)
            with self.ruta.open(mode="w", encoding=ENCODING) as archivo:
                archivo.write("{}")


    def cargar(self) -> DicJson:
        "Carga un archivo desde la ruta."

        with self.ruta.open(mode="r", encoding=ENCODING) as archivo:
            dic = load(archivo)

        return dic


    def guardar(self, dic: DicJson, sangria: int=4) -> None:
        """
        Guarda un diccionario en formato JSON en la ruta.
        -
        'dic': El diccionario en cuestión.

        'sangria': La cantidad de espacios a usar de sangría.
        """

        with self.ruta.open(mode="w", encoding=ENCODING) as archivo:
            dump(dic, archivo, indent=sangria)
