"""
Módulo de menú de controles.
"""

from typing import TYPE_CHECKING, Optional, TypeAlias, Union

from pygame.constants import K_ESCAPE, KEYDOWN, NOEVENT, USEREVENT
from pygame.display import get_surface
from pygame.event import Event, post
from pygame.event import wait as ev_wait
from pygame.key import name as key_name
from pygame_menu import BaseImage
from pygame_menu.widgets import Label

from ....controlador.controles import TiposAccion
from ....controlador.eventos import EventosJuego
from ...fuentes import FuenteMinecraftia
from ...temas import TemaFresh
from ..supermenu import SuperMenu, MENUS_IMG

if TYPE_CHECKING:
    from os import PathLike

    from pygame_menu import Menu
    from pygame_menu._types import EventVectorType
    from pygame_menu.widgets import Button, Widget

    from ....controlador.estado import JuegoHandler
    from ..supermenu import KwargsDict

ControlDict: TypeAlias = dict[str, Union[Label, "Button"]]
WidgetsControlesDict: TypeAlias = dict[str, ControlDict]
DescripcionesDict: TypeAlias = dict[TiposAccion, str]


ARROW_LEFT_IMG_PATH: "PathLike" = f"{MENUS_IMG}/flecha_izq.png"

# --- Widgets ---
NOMBRE: str = "nombre_accion"
TECLAS: str = "teclas_accion"
AGREGAR: str = "agregar_tecla"
QUITAR: str = "quitar_tecla"
# ---------------

# --- Strings ---
ESPERANDO: str = "[Ingresa una tecla...]"
AGREGAR_BTN: str = "+ "
QUITAR_BTN: str = "- "
# ---------------


class MenuControles(SuperMenu):
    "Clase del menú de opciones."


    def __init__(self, juego_handler: "JuegoHandler") -> None:
        """
        Incializa el menú de controles.
        -
        'juego_handler': Una instancia de controlador del juego. El mismo debería estar ya
                         inicializado, y por lo tanto, contener una instancia del juego dentro.
        """

        super().__init__(juego_handler)
        self.descripciones: DescripcionesDict = {
            TiposAccion.IZQUIERDA: """Cuando el jugador necesita moverse a la izquierda.""",
            TiposAccion.DERECHA: """Cuando el jugador necesita moverse a la derecha.""",
            TiposAccion.SALTAR: """Cuando el jugador se impulsa verticalmente.""",
            TiposAccion.DASH: """Cuando el jugador da un impulso horziontal repentino."""
        }
        self.widgets_controles: WidgetsControlesDict = {}
        self._generar_widgets()

        self.btn_volver: "Button" = self.add.button(
            title="Volver",
            action=self.juego_handler.cambiar_a_opciones,
            float=True, # No cuenta para la cuadrícula
            float_origin_position=True,
        )
        self._actualizar_volver_btn()

        self.descripcion: list[Label] = self._generar_desc()
        self._actualizar_desc_pos()


    def _generar_widgets(self) -> None:
        "Refresca los widgets según la info guardada en los controles."

        controles_dict = self.juego_handler.controles.controles

        # Necesariamente se tienen que agregar por columna, tal parece
        for i in range(self.cantidad_columnas):
            for accion in controles_dict:
                if accion not in self.widgets_controles:
                    self.widgets_controles[accion] = {}
                if i == 0:
                    self.widgets_controles[accion][NOMBRE] = self.add.label(
                        title=f"{accion} ",
                        label_id=f"{accion}_{NOMBRE}",
                        selectable=True,
                        onselect=self.cambiar_descripcion)
                elif i == 1:
                    self.widgets_controles[accion][TECLAS] = self.add.label(
                        title=self.teclas_accion_str(accion),
                        label_id=f"{accion}_{TECLAS}")
                elif i == 2:
                    self.widgets_controles[accion][AGREGAR] = self.add.button(
                        title=AGREGAR_BTN,
                        action=self.procesar_accion_agregar,
                        button_id=f"{accion}_{AGREGAR}",
                        accion=accion, # Éste es obligatorio para que self.procesar_accion funque
                        accept_kwargs=True)
                elif i == 3:
                    self.widgets_controles[accion][QUITAR] = self.generar_btn_quitar(accion)


    def _generar_desc(self, contenido: str="") -> list[Label]:
        """
        Genera la etiqueta de descripción.
        -
        'contenido': El texto de la descripción
        """

        _, alto = get_surface().get_size()

        desc = self.add.label(
            title=contenido,
            max_char=0, # No dividir a menos que encuentre '\n'
            wordwrap=False,
            float=True,
            float_origin_position=True,
            font_name=FuenteMinecraftia(tam=int(alto * 0.025)),

        )

        if isinstance(desc, Label):
            desc = [desc]

        return desc


    def refrescar_descripcion(self, contenido: str="") -> list[Label]:
        """
        Refresca la etiqueta de descripción.
        -
        'contenido': El texto de la descripción
        """

        for linea in self.descripcion:
            self.remove_widget(linea)

        self.descripcion = self._generar_desc(contenido)
        self._actualizar_desc_pos()


    @property
    def cantidad_columnas(self) -> int:
        """
        Devuelve la cantidad de columnas a usar para la 'grilla' de widgets.
        Éstas deberían distribuirse de la siguiente manera:
            - Una para el nombre de la acción
            - Una para las teclas asociadas a la acción
            - Una para un botón de agregar teclas a la acción
            - Una para un posible botón de quitar teclas de una acción.
        """

        return 4


    def cambiar_descripcion(self, selected: bool, widget: "Widget", _menu: "Menu") -> None:
        """
        Intenta cambiar la descripción del menú. Esta función se llama sola, no hace
        falta llamarla manualmente.
        -
        'selected': Un booleano que indica si el widget esta siendo seleccionado o no.
    
        'widget': El widget en cuestión: en nuestro caso es la etiqueta.

        'menu': El menú que contiene el widget.
        """

        accion = widget.get_id().removesuffix(f"_{NOMBRE}")

        if selected and hasattr(self, "descripcion") and accion in self.descripciones:
            desc = self.descripciones.get(accion, "")
            self.refrescar_descripcion(f"{accion.upper()}:\t{desc}"
                                       if accion in self.descripciones else desc)


    def _actualizar_desc_pos(self) -> None:
        "Actualiza la etiqueta de descripción."

        ancho, alto = get_surface().get_size()

        for i, linea in enumerate(self.descripcion):
            linea.translate(ancho * 0.3, (i + 1) * alto * 0.03)


    def _actualizar_volver_btn(self) -> None:
        "Actualiza la imagen para volver del menú."

        ancho, alto = get_surface().get_size()
        tam_icon = alto * 0.05

        self.btn_volver.translate(ancho * 0.06, alto * 0.01)

        dec_volver = self.btn_volver.get_decorator()
        dec_volver.add_baseimage(-(ancho * 0.075), (alto * 0.002),
                                 BaseImage(ARROW_LEFT_IMG_PATH).resize(tam_icon * 1.2, tam_icon),
                                 centered=True)


    def teclas_accion_str(self, accion: TiposAccion) -> str:
        """
        Formatea un string tal que se muestran las teclas asociadas a una acción.
        -
        'accion': El nombre de la acción en cuestión.
        """

        return f"{' - '.join(self.juego_handler.controles.controles[accion])} "


    def verificar_btn_quitar(self, accion: TiposAccion, btn: Optional["Button"]=None) -> "Button":
        """
        Verifica si un botón es visible o no, dependiendo de si tiene sólo una tecla asociada.
        Devuelve la instancia del botón.
        -
        'accion': El nombre de la acción.

        'btn': El botón a esconder o mostrar. Si es `None` entonces se lo busca entre
               los widgets registrados.
        """

        if btn is None:
            btn = self.widgets_controles[accion][QUITAR]

        if self.juego_handler.controles.quedan_pocas_teclas(accion):
            return btn.hide()

        return btn.show()


    def generar_btn_quitar(self, accion: TiposAccion) -> "Button":
        """
        Genera o un botón para quitar teclas de la acción, o un espacio vacío.
        -
        'accion': El nombre de la acción.
        """

        return self.verificar_btn_quitar(accion, self.add.button(
            title=QUITAR_BTN,
            button_id=f"{accion}_{QUITAR}",
            action=self.procesar_accion_quitar,
            accion=accion,
            accept_kwargs=True
        ))


    def procesar_accion_quitar(self, accion: TiposAccion) -> None:
        """
        Procesa el botón para quita una tecla de una acción.
        -
        'accion': El nombre de la acción a modificar.
        """

        tecla = self.juego_handler.controles.quitar_ultima_tecla(accion)
        self.refrescar_descripcion(f"Tecla '{tecla}' quitada de la acción '{accion.upper()}'")
        self._actualizar_botones_y_teclas(accion)


    def procesar_accion_agregar(self, accion: TiposAccion) -> None:
        """
        Procesa el botón para agregar una tecla a una acción.
        -
        'accion': El nombre de la acción a cambiar.
        """

        _, alto = get_surface().get_size()

        btn = self.widgets_controles[accion][AGREGAR]
        btn.set_title(ESPERANDO)
        btn.update_font({"name": FuenteMinecraftia(tam=int(alto * 0.025))})
        self.refrescar_descripcion("Por favor, ingresa una tecla para incluir en la "
                                   f"acción '{accion.upper()}'.\nPresiona 'Escape' para salir.")

        post(Event(USEREVENT, # Necesariamente del tipo USEREVENT, sino no guarda los atributos
                   custom_type=EventosJuego.PEDIR_INPUT_TECLA, accion=accion))


    def _actualizar_botones_y_teclas(self, accion: TiposAccion, guardar: bool=True) -> None:
        """
        Intenta actualizar el mensaje de las teclas y los botones de quitar.
        También intenta guardar las configuraciones.
        -
        'accion': El nombre de la acción a procesar.

        'guardar': Si guardar las configuraciones o no.
        """

        self.widgets_controles[accion][TECLAS].set_title(self.teclas_accion_str(accion))
        self.verificar_btn_quitar(accion)
        self._reposicionar_teclas_quitar()

        if guardar:
            self.juego_handler.controles.guardar_config()


    def _reposicionar_teclas_quitar(self) -> None:
        "Intenta mover las teclas de quitar, para que queden alineadas."

        _, alto = get_surface().get_size()
        # pylint: disable=consider-using-dict-items
        botones_quitar = [self.widgets_controles[accion][QUITAR]
                         for accion in self.widgets_controles]
        fact_x, fact_y = (0, 0)
        for btn in botones_quitar:
            btn.translate(0, 0) # Para mover desde el origen cada vez
            if not btn.is_visible():
                fact_y += 0.082
            btn.translate(fact_x, alto * fact_y)



    def pedir_tecla(self, accion: TiposAccion) -> None:
        """
        Pide una tecla al usuario, para configurar controles.
        -
        'accion': El nombre de la acción a cambiar.
        """

        _, alto = get_surface().get_size()
        controles_dict = self.juego_handler.controles.controles
        btn_agregar = self.widgets_controles[accion][AGREGAR]
        mensaje = ""

        while True:
            ev = ev_wait(timeout=5000)
            if ev.type == KEYDOWN:
                if ev.key != K_ESCAPE:
                    nombre_tecla = key_name(ev.key)
                    if self.juego_handler.controles.esta_repetido(nombre_tecla):
                        mensaje = (f"ERROR:\tLa tecla '{nombre_tecla}' está "
                                   "repetida.   Elige otra.")

                    else:
                        controles_dict[accion].append(nombre_tecla)

                break

            elif ev.type == NOEVENT:
                break

        btn_agregar.set_title(AGREGAR_BTN)
        btn_agregar.update_font({"name": FuenteMinecraftia(tam=int(alto * 0.04))})
        self.refrescar_descripcion(mensaje)
        self._actualizar_botones_y_teclas(accion)


    def get_super_kwargs(self) -> "KwargsDict":
        "Devuelve el diccionario de argumentos a usar en la clase madre."

        ancho, alto = get_surface().get_size()
        cant_acciones = len(TiposAccion)

        return dict(title="Controles",
                    width=ancho,
                    height=alto * 0.8,
                    columns=self.cantidad_columnas,
                    rows=cant_acciones,
                    column_max_width=None,
                    menu_id="menu_controls",
                    position=(0, alto * 0.1, False),
                    theme=TemaFresh(tam_widget=int(alto * 0.04),
                                    widget_offset_x=0.0))


    def update(self, events: "EventVectorType") -> bool:
        """
        Actualiza el menú actual.
        -
        'events': Los eventos con los que actualizar el menú.
        """

        for ev in events:
            if ev.type == USEREVENT and (hasattr(ev, "custom_type")
                                         and ev.custom_type == EventosJuego.PEDIR_INPUT_TECLA):
                self.pedir_tecla(ev.accion)

        return super().update(events)
