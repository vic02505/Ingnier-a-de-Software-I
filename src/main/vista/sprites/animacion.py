"""
Módulo para una animación.
"""

from pathlib import Path
from typing import TYPE_CHECKING, TypeAlias

from pygame.image import load as img_load
from pygame.transform import rotate
from pygame.math import Vector2
from pygame.sprite import WeakDirtySprite
from pygame.transform import scale

if TYPE_CHECKING:
    from os import PathLike

    from pygame import Surface


SpriteElegido: TypeAlias = WeakDirtySprite
TuplaSprites: TypeAlias = tuple[SpriteElegido, ...]

EXT: str = "png"


class Animacion:
    "Clase para una colección de sprites."

    def __init__(self,
                 pos: Vector2,
                 tam: Vector2,
                 ruta: "PathLike") -> None:
        """
        Inicializa los sprites del jugador.
        -
        'pos': Un vector en 2 dimensiones (`pygame.math.Vector2`), el cual representa
               la posición del jugador.

        'tam': El tamaño horizontal/vertical del sprite del jugador.

        'ruta': Directorio padre donde se encuentran los sprites
        """

        self.pos: Vector2 = pos
        # Esto idealmente debería ser igual para todos los frames
        self.tam: Vector2 = tam
        self.sprites: TuplaSprites = self._cargar_sprites(ruta)

        self._spr_ind: int = 0


    def _cargar_sprites(self, ruta: "PathLike") -> TuplaSprites:
        """
        Dada una ruta donde está la carpeta contenedora, esta función carga
        todos los sprites que allí encuentra y los compila en una lista.
        -
        'ruta': La ruta donde se encuentran todos los frames.
        """

        path = Path(ruta)
        sprites = []

        for arch in path.iterdir():
            if arch.is_file() and arch.name.lower().endswith(f".{EXT.lower()}"):
                spr = SpriteElegido()
                spr.dirty = 0
                spr.image = scale(img_load(arch.as_posix()).convert_alpha(), self.tam)
                sprites.append(spr)

        return tuple(sprites)


    def _siguiente_spr_ind(self, inplace: bool=True) -> int:
        """
        Devuelve el índice de lo que sería el siguiente frame de la animación.
        -
        'inplace': Si modificar el atributo interno de la animación o no.
        """

        sig_ind = (self._spr_ind + 1) % len(self.sprites)

        if inplace:
            self._spr_ind = sig_ind

        return sig_ind


    def reiniciar_indice(self) -> None:
        "Reinicia al índice de los frames al primero."

        self._spr_ind = 0


    def siguiente_frame(self) -> int:
        "Cambia el frame actual por el siguiente."

        return self._siguiente_spr_ind()


    def rotar(self, rot: float) -> "Animacion":
        """
        Intenta rotar todos los sprites de la animación.
        Se devuelve la instancia de la animación.
        -
        'rot': La cantidad de grados a rotar, en radianes.
        """

        for spr in self.sprites:
            spr.image = rotate(spr.image, rot)

        return self


    def set_transparencia(self, alpha: int) -> "Animacion":
        """
        Cambia la transparencia de la animación.
        """

        if alpha < 0:
            alpha = 0
        elif alpha > 255:
            alpha = 255

        for spr in self.sprites:
            spr.image = spr.image.convert_alpha()
            spr.image.set_alpha(alpha)

        return self


    def dibujar(self, superficie: "Surface", alpha: int=255) -> SpriteElegido:
        """
        Dibuja esta animación. Devuelve el sprite que se acaba de dibujar.
        -
        'superficie': La superficie sobre la que dibujar.

        'alpha': La transparencia de la imagen. Debe ser un número entre 0 y 255.
        """

        spr_actual = self.sprites[self._spr_ind]
        spr_actual.image = spr_actual.image.convert_alpha()
        spr_actual.image.set_alpha(alpha)
        superficie.blit(spr_actual.image, self.pos)
        return spr_actual
