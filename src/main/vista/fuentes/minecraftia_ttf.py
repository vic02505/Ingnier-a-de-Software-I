"""
Módulo para la fuente agregada 'Minecraftia'.
"""

from typing import TYPE_CHECKING

from pygame.font import Font

if TYPE_CHECKING:
    from os import PathLike

MINECRAFTIA_PATH: "PathLike" = "./media/fuentes/Minecraftia-Regular.ttf"


class FuenteMinecraftia(Font):
    "Fuente minecraftia."


    def __init__(self, tam: int=12) -> None:
        """
        Inicializa la fuente 'Minecraftia'.
        -
        'tamanio': El tamaño de la fuente. Es necesario especificarlo exlusivamente acá en el
                  inicializador.
        """

        super().__init__(MINECRAFTIA_PATH, tam)
