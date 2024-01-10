"""
Módulo para el handler del estado del juego.
"""

from typing import TYPE_CHECKING, Optional, TypeAlias

from pygame.constants import K_ESCAPE, KEYDOWN
from pygame.display import set_caption
from pygame.time import set_timer
from pygame_menu.sound import (SOUND_EXAMPLE_WIDGET_SELECTION,
                               SOUND_TYPE_CLICK_MOUSE,
                               SOUND_TYPE_WIDGET_SELECTION)

from ...modelo.eventos import EventosSonidos
from ...vista.menus import (MenuCargar, MenuControles, MenuEditor, MenuNivel,
                            MenuOpciones, MenuPerderPartida, MenuPrincipal,
                            MenuVictoria)
from ...vista.niveles import RenderizadorNivel
from ..controles import ControlesHandler
from ..editor import EditorHandler
from ..eventos import EventosJuego
from ..jugador import JugadorHandler
from ..sonidos import MotorSFX

if TYPE_CHECKING:
    from os import PathLike

    from pygame import Surface
    from pygame.event import Event

    from ...modelo.estado import Juego, RutasNiveles
    from ...modelo.niveles import Nivel
    from ...vista.menus import SuperMenu
    from ..logger import LoggerJuego

TuplaMenus: TypeAlias = tuple["SuperMenu", ...]

# -- sfx --
MENU_CLICK_PATH: "PathLike" = "./media/sfx/menus/menu_click.wav"
# ---------

class JuegoHandler:
    "Clase para el handler de una instancia de juego."

    def __init__(self,
                 juego: "Juego",
                 logger: "LoggerJuego") -> None:
        """
        Inicializa el handler del juego.
        -
        'juego': La instancia del estado del juego, tal que se pueda acceder a ella.

        'logger': El registrador del juego.
        """

        self.juego: "Juego" = juego
        self.logger: "LoggerJuego" = logger
        self.controles: ControlesHandler = ControlesHandler(logger=self.logger)
        self.sfx: MotorSFX = MotorSFX(logger=self.logger)
        self.jugador_handler: Optional[JugadorHandler] = None
        self.editor_handler: EditorHandler = EditorHandler()

        # -- Niveles --
        self.rend_nivel: RenderizadorNivel = RenderizadorNivel(self)
        self.trofeos_recogidos: int = 0
        # -------------

        # -- Atributos de control --
        self._salir: bool = False
        self.conservar_vidas: bool = True
        # --------------------------

        # -- Menús --
        self.menu_principal: MenuPrincipal = MenuPrincipal(self)
        self.menu_opciones: MenuOpciones = MenuOpciones(self)
        self.menu_controles: MenuControles = MenuControles(self)
        self.menu_editor: MenuEditor = MenuEditor(self)
        self.menu_nivel: MenuNivel = MenuNivel(self)
        self.menu_perder: MenuPerderPartida = MenuPerderPartida(self)
        self.menu_ganar: MenuVictoria = MenuVictoria(self)
        self.menu_cargar: MenuCargar = MenuCargar(self)

        self.menus_ext: TuplaMenus = (self.menu_principal, self.menu_cargar, self.menu_opciones,
                                      self.menu_controles, self.menu_editor, self.menu_perder,
                                      self.menu_ganar)
        self.menus_in: TuplaMenus = (self.menu_nivel,)

        self.menu_actual: "SuperMenu" = self.menu_principal
        # -----------

        # -- eventos --
        set_timer(EventosJuego.PROCESAR_MOV_JUGADOR, millis=22)
        set_timer(EventosJuego.REDIBUJAR_JUGADOR, millis=25) # Actualizar sprite cada 0.025 seg
        set_timer(EventosJuego.CONTAR_TIMERS, millis=1)
        # -------------


    @property
    def menus(self) -> TuplaMenus:
        "Devuelve todos los menús disponibles en el juego."

        return self.menus_ext + self.menus_in


    @property
    def nivel(self) -> Optional["Nivel"]:
        "Devuelve el nivel actual del juego."

        return self.juego.nivel_actual


    @property
    def version_str(self) -> str:
        "Devuelve una representación en string de la versión."

        mayor, menor, parche, estado = self.juego.version
        estado_str = (f"-{estado}" if estado else "")
        return f"{mayor}.{menor}.{parche}{estado_str}"


    def set_titulo_juego(self, extra: str="") -> str:
        """
        Refresca y devuelve el string que se muestra en el título de la
        ventana del juego.
        -
        'extra': Un substring extra que agregar al título.
        """

        titulo_ventana = f"Cube Jumper v{self.version_str}{extra}"
        set_caption(titulo_ventana)

        return titulo_ventana


    def get_volumen(self) -> float:
        "Devuelve el nivel de volumen de los menús."

        return self.sfx.volumen


    def hay_audio(self) -> bool:
        "Determina si los menús tienen audio de sonidos (no música) o no."

        return self.sfx.audio_sfx


    def cambiar_volumen(self, nuevo_vol: float) -> bool:
        """
        Cambia el volumen de la instancia de juego. Devuelve `True` si logra hacerlo,
        de lo contrario devuelve `False`.
        """

        nuevo_vol_frac = round(nuevo_vol / 100, 1)

        self.sfx.menus_sfx.set_sound(SOUND_TYPE_CLICK_MOUSE,
                                     MENU_CLICK_PATH,
                                     volume=nuevo_vol_frac)
        self.sfx.menus_sfx.set_sound(SOUND_TYPE_WIDGET_SELECTION,
                                     SOUND_EXAMPLE_WIDGET_SELECTION,
                                     volume=nuevo_vol_frac)

        return self.sfx.cambiar_volumen(nuevo_vol)


    def cambiar_audio(self, hay_audio: bool) -> bool:
        """
        Cambia el audio de la instancia de juego. Devuelve `True` si logra hacerlo,
        de lo contrario devuelve `False`.
        -
        'hay_audio': Un booleano que indica si debe haber audio o no.
        """

        for menu in self.menus:
            menu.set_sound((self.sfx.menus_sfx if hay_audio else None), recursive=True)
        return self.sfx.cambiar_audio(hay_audio)


    def cambiar_a_principal(self) -> None:
        "Cambia al menú principal."

        self.menu_actual = self.menu_principal
        self.logger.info("Cambiando al menú principal")
        self.set_titulo_juego(" - Principal")


    def cambiar_a_cargar(self) -> None:
        "Cambia al menú de cargar niveles."

        self.menu_actual = self.menu_cargar
        self.menu_cargar.cargar_botones()
        self.logger.info("Cargando niveles")
        self.set_titulo_juego(" - Cargando niveles")


    def cambiar_a_opciones(self) -> None:
        "Cambia al menú opciones."

        self.menu_actual = self.menu_opciones
        self.logger.info("Cambiando al menú de opciones")
        self.set_titulo_juego(" - Opciones")


    def cambiar_a_controles(self) -> None:
        "Cambia al menú de controles."

        self.menu_actual = self.menu_controles
        self.logger.info("Cambiando al menú de controles")
        self.set_titulo_juego(" - Controles")

    def cambiar_a_editor(self) -> None:
        "Cambia al menú del editor de niveles."

        self.menu_actual = self.menu_editor
        self.logger.info("Cambiando al menú del editor de niveles")
        self.set_titulo_juego(" - Editor de niveles")


    def cambiar_a_nivel(self) -> None:
        "Cambia al menú de nivel."

        self.menu_actual = self.menu_nivel
        if self.nivel is not None:
            msg = f"l nivel '{self.nivel.titulo}'"
        else:
            msg = " un nivel"
        self.logger.info(f"Entrando a{msg}")
        self.set_titulo_juego(f" ({self.nivel.titulo})")


    def mostrar_derrota(self) -> None:
        "Cambia al menú de perder un nivel."

        self.menu_actual = self.menu_perder
        self.logger.info("Partida perdida...")
        self.sfx.mixer.play(self.sfx.sonidos["derrota"])
        self.set_titulo_juego()


    def mostrar_victoria(self) -> None:
        "Cambia al menú de ganar."

        self.menu_actual = self.menu_ganar
        self.menu_ganar.actualizar_etiqueta_trofeos()
        self.logger.info("¡Partida ganada!")
        self.sfx.mixer.play(self.sfx.sonidos["victoria"])
        self.set_titulo_juego()


    def en_editor(self) -> bool:
        "Verifica si el juego está en el editor."

        return self.menu_actual == self.menu_editor


    def se_esta_jugando(self) -> bool:
        "Averigua si el juego esta dentro de un nivel o no."

        return self.juego.se_esta_jugando() and self.menu_actual in self.menus_in


    def iniciar_juego(self, niveles: Optional["RutasNiveles"]=None) -> None:
        """
        Inicia el juego por primera vez.
        -
        'niveles': Las rutas de los niveles a cargar, si es que se quiere cargar un pack en
                   particular. Si no se especifica, se utilizan los niveles que vienen con
                   el juego.
        """

        self.juego.reiniciar_niveles(niveles)
        self.trofeos_recogidos = 0
        self.jugar(conservar_vidas=False) # Al ser la primera vez, la vida se debe reiniciar


    def jugar(self, conservar_vidas: Optional[bool]=None) -> None:
        """
        Intenta iniciar el juego.
        -
        'conservar_vidas': Si conservar las vidas de niveles anteriores.
        """

        if conservar_vidas is None:
            conservar_vidas = self.conservar_vidas

        self.juego.jugar(preservar_vidas=conservar_vidas)
        self.jugador_handler = JugadorHandler(self.juego.jugador,
                                              self.sfx,
                                              self.controles,
                                              self.logger)
        self.rend_nivel.reiniciar_nivel()
        self.cambiar_a_nivel()


    def hay_que_salir(self) -> bool:
        "Determina si hay que salir del programa o no."

        return self._salir


    def salir(self) -> None:
        """
        Cambia un atributo interno tal que el ciclo principal entiende que tiene que
        terminar la ejecución del programa.
        """

        self._salir = True


    def actualizar(self, superficie: "Surface", eventos: list["Event"],
                   **kwargs) -> None:
        """
        Actualiza el menú actual. Esto es, corre el ciclo tal que refresca la pantalla
        y redibuja todo, a la vez que procesa los eventos que hayan ocurrido.
        -
        'superficie': La superficie (`pygame.Surface`) en donde se va a dibujar todos los
                      cambios visuales a aplicar.

        'eventos': La lista de eventos de Pygame a procesar.

        '**kwargs': Atributos extra.
        """

        for ev in eventos:
            if ev.type == KEYDOWN:
                if ev.key == K_ESCAPE and (self.en_editor() or self.se_esta_jugando()):
                    self.cambiar_a_principal()

            elif ev.type == EventosSonidos.DANIO_FUERTE:
                self.sfx.mixer.play(self.sfx.sonidos["danio_fuerte"])

            elif ev.type == EventosSonidos.LLAVE:
                self.sfx.mixer.play(self.sfx.sonidos["llave"])

            elif ev.type == EventosSonidos.TROFEO:
                self.sfx.mixer.play(self.sfx.sonidos["trofeo"])
                self.trofeos_recogidos += 1

        if self.se_esta_jugando():
            gano_nivel, hay_siguiente = self.juego.gano()

            if self.juego.perdio():
                self.juego.salir()
                self.mostrar_derrota()

            elif gano_nivel:
                if hay_siguiente:
                    self.jugar()
                else:
                    self.juego.salir()
                    self.mostrar_victoria()

            self.rend_nivel.actualizar(superficie, eventos)
            self.juego.reiniciar_vel_jugador() # Necesariamente antes que procesar las teclas
            self.jugador_handler.actualizar(superficie, eventos, nivel=self.nivel, **kwargs)
            self.juego.actualizar(eventos)
            self.rend_nivel.dibujar_debug_info(superficie)

        elif self.en_editor():
            self.editor_handler.actualizar(superficie, eventos)

        self.menu_actual.update(eventos)
        self.menu_actual.draw(superficie)


    def guardar_config(self) -> None:
        """
        Guarda las configuraciones de distintos handlers para que persistan en la
        siguiente ejecución del juego.
        """

        self.controles.guardar_config()
        self.sfx.guardar_config()
