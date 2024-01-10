"""
Módulo de menú de opciones.
"""

from typing import TYPE_CHECKING, Optional

from pygame.display import get_surface
from pygame_menu import BaseImage

from ...fuentes import FuenteMinecraftia
from ...temas import TemaFresh
from ..supermenu import MENUS_IMG, SuperMenu

if TYPE_CHECKING:
    from os import PathLike

    from pygame_menu.widgets import Button, RangeSlider, ToggleSwitch

    from ....controlador.estado import JuegoHandler
    from ..supermenu import KwargsDict

AUDIO_ON_PATH: "PathLike" = f"{MENUS_IMG}/audio_available.png"
AUDIO_OFF_PATH: "PathLike" = f"{MENUS_IMG}/audio_muted.png"
VOL_ON_PATH: "PathLike" = f"{MENUS_IMG}/vol_available.png"
VOL_OFF_PATH: "PathLike" = f"{MENUS_IMG}/vol_muted.png"
CONTROLS_PATH: "PathLike" = f"{MENUS_IMG}/control.png"
BACK_IMG_PATH: "PathLike" = f"{MENUS_IMG}/back_arrow.png"

COLOR_OFF: str = "#cc0000"
COLOR_ON : str = "#88ff00"


class MenuOpciones(SuperMenu):
    "Clase del menú de opciones."


    def __init__(self, juego_handler: "JuegoHandler") -> None:
        """
        Incializa el menú de opciones.
        -
        'juego_handler': Una instancia de controlador del juego. El mismo debería estar ya
                         inicializado, y por lo tanto, contener una instancia del juego dentro.
        """

        super().__init__(juego_handler)

        ancho, alto = get_surface().get_size()
        min_slid, max_slid = (0, 100)

        blanco = "#ffffff"

        self.vol_slider: "RangeSlider" = self.add.range_slider(
            title="Volumen",
            default=self.juego_handler.get_volumen(),
            range_values=(min_slid, max_slid),
            increment=1.0,
            range_line_color="#cccccc",
            range_line_height=int(alto / 360),
            range_margin=(int(ancho * 0.05), 0),
            range_text_value_enabled=False,
            range_text_value_tick_color="#dddddd",
            range_text_value_tick_hfactor=0.2,
            range_text_value_tick_number=int(max_slid / 10),
            range_text_value_tick_thick=int(alto / 720),
            onchange=self._cambiar_volumen,
            slider_text_value_enabled=True,
            slider_text_value_font=FuenteMinecraftia(tam=int(alto * 0.028)),
            slider_height_factor=0.4,
            slider_sel_highlight_color=blanco,
            slider_selected_color=blanco,
            slider_text_value_bgcolor=(0, 0, 0, 0),
            slider_text_value_color=blanco,
            slider_text_value_margin_f=0.65,
            slider_thickness=int(ancho * 0.01),
            value_format=(lambda val: (f"{val:.1f}%"
                                       if not f"{val:.1f}".endswith(".0")
                                       else f"{int(val)}%")),
            width=int(ancho * 0.3)
        )
        self.audio_switch: "ToggleSwitch" = self.add.toggle_switch(
            title="SFX",
            default=self.juego_handler.hay_audio(),
            state_text=("OFF", "ON"),
            onchange=self._cambiar_audio,
            slider_thickness=int(ancho * 0.01),
            state_color=(COLOR_OFF, COLOR_ON),
            state_text_font=FuenteMinecraftia(tam=int(ancho * 0.025)),
            switch_border_width=0,
            switch_margin=(int(ancho * 0.235), 0),
            width=int(ancho * 0.1)
        )
        self.conservar_vidas: "ToggleSwitch" = self.add.toggle_switch(
            title="Conservar vidas",
            default=self.juego_handler.conservar_vidas,
            state_text=("NO", "SÍ"),
            onchange=self._alternar_conservar_vidas,
            slider_thickness=int(ancho * 0.01),
            state_color=(COLOR_OFF, COLOR_ON),
            state_text_font=FuenteMinecraftia(tam=int(ancho * 0.025)),
            switch_border_width=0,
            switch_margin=(int(ancho * 0.05), 0),
            width=int(ancho * 0.1)
        )
        self.btn_controles: "Button" = self.add.button(
            title="Controles",
            action=self.juego_handler.cambiar_a_controles
        )
        self.btn_volver: "Button" = self.add.button(
            title="Volver",
            action=self.juego_handler.cambiar_a_principal
        )

        self._sfx_img_id: str = ""
        self._vol_img_id: str = ""
        self._actualizar_audio_img()
        self._actualizar_vol_img()
        self._actualizar_controles_img()
        self._actualizar_volver_img()


    def get_super_kwargs(self) -> "KwargsDict":
        "Devuelve el diccionario de argumentos a usar en la clase madre."

        ancho, alto = get_surface().get_size()

        return dict(title="Opciones",
                    width=ancho,
                    height=alto * 0.75,
                    column_max_width=None,
                    menu_id="menu_options",
                    position=(0, alto * 0.2, False),
                    theme=TemaFresh())


    def _actualizar_audio_img(self, estado: Optional[bool]=None) -> None:
        """
        Actualiza la imagen del botón de audio.
        -
        'estado': Un booleano que indica si debe haber o no audio. Si no hay un valor
                  utiliza el que encuentra en el controlador del juego.
        """

        ancho, alto = get_surface().get_size()
        tam_icon = alto * 0.075
        dec_audio = self.audio_switch.get_decorator()

        if estado is None:
            estado = self.juego_handler.hay_audio()

        if self._sfx_img_id:
            dec_audio.remove(self._sfx_img_id)

        self._sfx_img_id = dec_audio.add_baseimage(
            -(ancho * 0.236), 0,
            BaseImage(AUDIO_ON_PATH if estado
                      else AUDIO_OFF_PATH).resize(tam_icon, tam_icon),
            centered=True
        )


    def _cambiar_audio(self, estado: bool) -> bool:
        """
        Intenta cambiar el estado de si hay sonido o no.
        -
        'estado': Un booleano que indica si debe haber o no audio.
        """

        self._actualizar_audio_img(estado)
        return self.juego_handler.cambiar_audio(estado)


    def _alternar_conservar_vidas(self, estado: bool) -> bool:
        """
        Intenta cambiar el estado de si se convervan vidas o no.
        -
        'estado': Un booleano que indica si se deben conservar las vidas entre niveles o no.
        """

        self.juego_handler.conservar_vidas = estado


    def _actualizar_vol_img(self, nuevo_vol: Optional[float]=None) -> None:
        """
        Actualiza la imagen del botón de audio.
        -
        'nuevo_vol': El nuevo valor del volumen a aplicar. Si no hay un valor dado, utiliza el
                     que encuentra en el controlador del juego.
        """

        ancho, alto = get_surface().get_size()
        tam_icon = alto * 0.075
        dec_vol = self.vol_slider.get_decorator()

        if nuevo_vol is None:
            nuevo_vol = self.juego_handler.get_volumen()

        if self._vol_img_id:
            dec_vol.remove(self._vol_img_id)

        self._vol_img_id = dec_vol.add_baseimage(
            -(ancho * 0.29), 0,
            BaseImage(VOL_ON_PATH if nuevo_vol > 0.0
                      else VOL_OFF_PATH).resize(tam_icon, tam_icon),
            centered=True
        )


    def _cambiar_volumen(self, nuevo_vol: float) -> bool:
        """
        Intenta cambiar el estado de si hay sonido o no.
        -
        'nuevo_vol': El nuevo valor del volumen a aplicar.
        """

        self._actualizar_vol_img(nuevo_vol)
        return self.juego_handler.cambiar_volumen(nuevo_vol)


    def _actualizar_controles_img(self) -> None:
        "Actualiza la imagen para abrir el menú de controles."

        ancho, alto = get_surface().get_size()
        tam_icon = alto * 0.07
        dec_controles = self.btn_controles.get_decorator()

        dec_controles.add_baseimage(-(ancho * 0.135), (alto * 0.007),
                                 BaseImage(CONTROLS_PATH).resize(tam_icon * 1.3, tam_icon),
                                 centered=True)


    def _actualizar_volver_img(self) -> None:
        "Actualiza la imagen para volver del menú."

        ancho, alto = get_surface().get_size()
        tam_icon = alto * 0.075
        dec_volver = self.btn_volver.get_decorator()

        dec_volver.add_baseimage(-(ancho * 0.1), (alto * 0.007),
                                 BaseImage(BACK_IMG_PATH).resize(tam_icon, tam_icon),
                                 centered=True)
