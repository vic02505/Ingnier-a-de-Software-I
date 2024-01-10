"""
Módulo para el motor de sonidos.
"""

from typing import TYPE_CHECKING, Optional, TypeAlias, Union

from pygame.mixer import Channel, Sound, get_num_channels, music
from pygame_menu.sound import Sound as MenuSound

from ..archivos import RutaJSON

if TYPE_CHECKING:
    from os import PathLike

    from ..logger import LoggerJuego


SoundPathDict: TypeAlias = dict[str, "PathLike"]
SoundsDict: TypeAlias = dict[str, Sound]

AUDIO_CONFIG: "PathLike" = "./config/audio.json"
SONIDOS_JUG: "PathLike" = "./media/sfx/jugador"
SONIDOS_NIVEL: "PathLike" = "./media/sfx/nivel"


class MotorSFX:
    "Clase que administra el audio del juego."

    def __init__(self,
                 *,
                 volumen: float=50.0,
                 audio: bool=True,
                 logger: Optional["LoggerJuego"]=None) -> None:
        """
        Inicializa el motor de sonido.
        -
        'volumen': El volumen inicial. Debe ser un número flotante en el rango [0.0, 100.0].

        'audio': Booleano que indica si hay audio o no inicialmente.

        'logger': El registrador del juego.
        """

        if not 0.0 <= float(volumen) <= 100.0:
            raise ValueError(f"El valor volumen={volumen} no está en entre 0.0 y 100.0.")

        self.ruta_configs: RutaJSON = RutaJSON(AUDIO_CONFIG)
        audio_configs = self.ruta_configs.cargar()
        self.logger: Optional["LoggerJuego"] = logger

        self.volumen: float = float(audio_configs.get("volumen", volumen))
        self.audio_sfx: bool = bool(audio_configs.get("audio", audio))

        self.menus_sfx: MenuSound = MenuSound()

        self.sonidos: SoundsDict = {}
        self._cargar_sonidos(salto=f"{SONIDOS_JUG}/salto.wav",
                             dash=f"{SONIDOS_JUG}/dash.wav",
                             derrota=f"{SONIDOS_JUG}/derrota.wav",
                             victoria=f"{SONIDOS_JUG}/victoria.wav",
                             danio=f"{SONIDOS_JUG}/danio.wav",
                             danio_fuerte=f"{SONIDOS_JUG}/danio_fuerte.wav",
                             # -- Nivel --
                             llave=f"{SONIDOS_NIVEL}/llave.wav",
                             trofeo=f"{SONIDOS_NIVEL}/trofeo.wav")

        # La 'música' son archivos de audio grandes, por lo que no se carga todo
        # en memoria a la vez, y sólo soporta un archivo al mismo tiempo
        self.soundtrack = music
        self.bgm: SoundPathDict = dict()


    def _cargar_sonidos(self, **rutas: SoundPathDict) -> None:
        """
        Carga los sonidos al diccionario, tal que queden en memoria como objetos
        'Sound()'.
        -
        '**rutas': Una colección de rutas donde cada una debería apuntar a una dirección
                   válida para inicializar un archivo de sonido. (se prefiere .WAV)
        """

        for nombre, ruta in rutas.items():
            try:
                self.sonidos[nombre] = Sound(ruta)
            except FileNotFoundError:
                self.logger.error(f"Archivo '{ruta}' no encontrado. Ignorando...")


    @property
    def mixer(self) -> Channel:
        "Devuelve el primer canal de reproducción disponible."

        num_ch = get_num_channels()
        for i in range(0, num_ch + 1):
            ch = Channel(i)
            if not ch.get_busy():
                return ch

        return Channel(0)


    def cambiar_volumen(self, nuevo_vol: float) -> bool:
        """
        Cambia el volumen del motor de sonido. Devuelve `True` si logra hacerlo,
        de lo contrario devuelve `False`.
        Debe ser un valor entre 0.0 y 100.0.
        -
        'nuevo_vol': El nuevo valor del volumen a aplicar.
        """

        if not isinstance(nuevo_vol, Union[int, float]) and 0.0 <= nuevo_vol < 100.0:
            return False

        self.volumen = round(nuevo_vol, 1)

        return True


    def cambiar_audio(self, hay_audio: bool) -> bool:
        """
        Cambia el audio del motor de sonido. Devuelve `True` si logra hacerlo,
        de lo contrario devuelve `False`.
        -
        'hay_audio': Un booleano que indica si debe haber o no audio.
        """

        if not isinstance(hay_audio, bool):
            return False

        self.audio_sfx = hay_audio

        return True


    def guardar_config(self) -> None:
        "Guarda la configuración de audio para que persista en la siguiente ejecución del juego."

        self.ruta_configs.guardar({"volumen": self.volumen,
                                    "audio": self.audio_sfx})
        self.logger.info("Configuración de audio guardada")
