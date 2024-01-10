"""
Módulo para el tema usado en el editor.
"""

from typing import Optional

from pygame.display import get_surface
from pygame_menu.locals import ALIGN_LEFT
from pygame_menu.themes import Theme
from pygame_menu.widgets import MENUBAR_STYLE_NONE
from pygame_menu.widgets import HighlightSelection

from ..fuentes import FuenteMinecraftia


class TemaEditor(Theme):
    "Clase para el tema del editor de niveles."

    def __init__(self, *,
                 tam_widget: Optional[int]=None,
                 widget_offset_x: float=0.1,
                 widget_offset_y: float=0.0,
                 margin_x: float=0.0,
                 margin_y: float=0.0,
                 **kwargs) -> None:
        """
        Inicializa el tema del editor.
        -
        'tam_widget': El tamaño de los widgets a dibujar.

        'widget_offset_x/widget_offset_y': El offset horizontal y vertical de los widgets.

        'margin_x/margin_y': Los márgenes horizontal/vertical de los widgets del menú.

        '**kwargs': El diccionario de propiedades a mandar a la clase madre. Tan sólo con
                    inicializar esta clase, ya se pobla con lo necesario, pero es posible agregar
                    cosas desde afuera con esto.
        """

        ancho, alto = get_surface().get_size()
        invisible = (255, 255, 255, 0) # Negro con alpha 0.0
        blanco = "#ffffff"
        gris = "#cccccc"
        if tam_widget is None:
            tam_widget = int(alto * 0.06)

        kwargs.update(background_color=invisible,
                      selection_color=blanco,
                      title_background_color=gris,
                      title_bar_style=MENUBAR_STYLE_NONE,
                      title_font=FuenteMinecraftia(tam=int(alto * 0.07)),
                      title_font_shadow=True,
                      title_font_shadow_color="#333333",
                      title_font_shadow_offset=int(alto * 0.006),
                      title_offset=(ancho * 0.01, -alto * 0.02),
                      widget_alignment=ALIGN_LEFT,
                      widget_font=FuenteMinecraftia(tam=tam_widget),
                      widget_font_color=gris,
                      widget_offset=(widget_offset_x, widget_offset_y),
                      widget_margin=(margin_x, margin_y),
                      widget_selection_effect=HighlightSelection())

        super().__init__(**kwargs)
