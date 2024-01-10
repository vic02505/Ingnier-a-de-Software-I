"""
Módulo principal, en el que habita la función que corre el programa.
"""

# ----- Sin esto Pygame muestra un cartel cada vez que se corre el programa -----
# pylint: disable=wrong-import-position
from os import environ

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
# -------------------------------------------------------------------------------

from traceback import format_exc
from typing import TYPE_CHECKING

from pygame import QUIT
from pygame import init as pygame_init
from pygame.display import flip, set_icon, set_mode
from pygame.event import get as event_get
from pygame.image import load as img_load
from pygame.transform import scale

from .controlador.estado import JuegoHandler
from .controlador.logger import LoggerJuego
from .modelo.estado import Juego

if TYPE_CHECKING:
    from os import PathLike

ANCHO_PANTALLA: int = 1280
ALTO_PANTALLA: int = 720
FPS: int = 60
COLOR_FONDO: str = "#000055"
ICONO: "PathLike" = "./media/img/icono/icono.png"


def main() -> int:
    "Función principal del programa."

    logger = LoggerJuego(nombre="Cube Jumper", verbose=True)

    try:
        pygame_init()
        set_icon(scale(img_load(ICONO), (32, 32))) # Por las dudas esto va antes que set_mode()
        pantalla = set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))

        juego_handler = JuegoHandler(Juego(), logger)
        juego_handler.set_titulo_juego()

        while not juego_handler.hay_que_salir():

            eventos = event_get()
            for evento in eventos:
                if evento.type == QUIT:
                    juego_handler.salir()

            pantalla.fill(COLOR_FONDO)
            juego_handler.actualizar(pantalla, eventos)
            flip()

        juego_handler.guardar_config()

        return 0

    # pylint: disable=W0718
    except BaseException: # Atrapa cualquier excepción, pero es el scope más alto y lo imprime igual
        error_bello = "\n\t|\t".join(f"¡Oh oh! Ha ocurrido un error:\n{format_exc()}".split("\n"))
        logger.error(error_bello)
        return 1


if __name__ == "__main__":
    main()
