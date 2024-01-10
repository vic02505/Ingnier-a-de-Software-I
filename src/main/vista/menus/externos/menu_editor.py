"""
Menú para el editor de niveles.
"""

from typing import TYPE_CHECKING, Any

from pygame.display import get_surface
from pygame_menu._types import Optional
from pygame_menu.locals import INPUT_TEXT

from ....controlador.editor import PosicionesMensajesEditor
from ...fuentes import FuenteMinecraftia
from ...temas import TemaEditor
from ..supermenu import SuperMenu

if TYPE_CHECKING:
    from os import PathLike

    from pygame import Surface
    from pygame_menu.menu import Menu
    from pygame_menu.widgets import Button, Label, Selector, TextInput

    from ....controlador.estado import JuegoHandler
    from ..supermenu import KwargsDict

COLOR_MENSAJE: str = "#ffffff"
COLOR_FLECHAS: str = "#eeeeee"
COLOR_INVISIBLE: str = (0, 0, 0, 0)


class MenuEditor(SuperMenu):
    "Clase para el menú de editar y crear niveles."

    def __init__(self, juego_handler: "JuegoHandler") -> None:
        """
        Incializa el menú principal.
        -
        'juego_handler': Una instancia de controlador del juego. El mismo debería estar ya
                         inicializado, y por lo tanto, contener una instancia del juego dentro.
        """

        super().__init__(juego_handler)

        self.nombre_nivel: str = "Nivel de Prueba"

        ancho, alto = get_surface().get_size()

        tam_mensajes = int(alto * 0.015)
        borde_izq_dif = -(ancho * 0.1)

        self.mensaje_click_izq: "Label" = self.add.label(
            title="CLICK IZQUIERDO para colocar la celda.",
            label_id="click_izq_msg",
            float=True,
            float_origin_position=True,
            font_name=FuenteMinecraftia(tam=tam_mensajes)
        ).translate(borde_izq_dif, -(alto * 0.1))
        self.mensaje_click_der: "Label" = self.add.label(
            title="CLICK DERECHO para borrar la celda.",
            label_id="click_der_msg",
            float=True,
            float_origin_position=True,
            font_name=FuenteMinecraftia(tam=tam_mensajes)
        ).translate(borde_izq_dif, -(alto * 0.08))
        self.mensaje_click_mid: "Label" = self.add.label(
            title="CLICK MEDIO para cambiar el ángulo (anti-horario).",
            label_id="click_mid_msg",
            float=True,
            float_origin_position=True,
            font_name=FuenteMinecraftia(tam=tam_mensajes)
        ).translate(borde_izq_dif, -(alto * 0.06))
        self.mensaje_rueda: "Label" = self.add.label(
            title="RUEDA ARRIBA/ABAJO para alternar los distintos tipos de celdas.",
            label_id="wheel_msg",
            float=True,
            float_origin_position=True,
            font_name=FuenteMinecraftia(tam=tam_mensajes)
        ).translate(borde_izq_dif, -(alto * 0.04))
        self.mensaje_tecla_v: "Label" = self.add.label(
            title="TECLA 'V' para alternar visibilidad de la celda.",
            label_id="vis_msg",
            float=True,
            float_origin_position=True,
            font_name=FuenteMinecraftia(tam=tam_mensajes)
        ).translate(borde_izq_dif, -(alto * 0.02))
        self.mensaje_tecla_ids: "Label" = self.add.label(
            title="'-'/'+' para disminuir/aumentar el ID de la celda.",
            label_id="ids_msg",
            float=True,
            float_origin_position=True,
            font_name=FuenteMinecraftia(tam=tam_mensajes)
        ).translate(borde_izq_dif, alto * 0.0)
        self.mensaje_escape: "Label" = self.add.label(
            title="TECLA 'ESCAPE' para salir.",
            label_id="ids_escape",
            float=True,
            float_origin_position=True,
            font_name=FuenteMinecraftia(tam=tam_mensajes)
        ).translate(borde_izq_dif, (alto * 0.02))

        col, fil = self.juego_handler.editor_handler.editor.forma
        margen_col_fil = int(ancho * 0.01)

        self.sel_columnas: "Selector" = self.add.selector(
            title="Columnas",
            items=[(str(i), i) for i in range(ancho // 10)],
            selector_id="selector_col",
            style="fancy", # la otra es "classic"
            style_fancy_arrow_color=COLOR_FLECHAS,
            style_fancy_bgcolor=COLOR_INVISIBLE,
            style_fancy_bordercolor=COLOR_INVISIBLE,
            style_fancy_borderwidth=0,
            style_fancy_arrow_margin=(margen_col_fil, margen_col_fil, 0),
            style_fancy_box_margin=(ancho * 0.01, 0),
            onchange=self._procesar_cambio_columnas,
            float=True,
            float_origin_position=True,
            font_name=FuenteMinecraftia(tam=int(alto * 0.025))
        ).translate(ancho * 0.285, -(alto * 0.085))
        self.sel_columnas.set_default_value(col).reset_value()

        self.sel_filas: "Selector" = self.add.selector(
            title="Filas",
            items=[(str(i), i) for i in range(alto // 10)],
            selector_id="selector_fil",
            style="fancy", # la otra es "classic"
            style_fancy_arrow_color=COLOR_FLECHAS,
            style_fancy_bgcolor=COLOR_INVISIBLE,
            style_fancy_bordercolor=COLOR_INVISIBLE,
            style_fancy_borderwidth=0,
            style_fancy_arrow_margin=(margen_col_fil, margen_col_fil, 0),
            style_fancy_box_margin=(ancho * 0.05, 0),
            onchange=self._procesar_cambio_filas,
            float=True,
            float_origin_position=True,
            font_name=FuenteMinecraftia(tam=int(alto * 0.025)),
        ).translate(ancho * 0.285, -(alto * 0.025))
        self.sel_filas.set_default_value(fil).reset_value()

        self.caja_nombre: "TextInput" = self.add.text_input(
            title="Nombre del Nivel:\t",
            default=self.nombre_nivel,
            input_type=INPUT_TEXT,
            onchange=self._cambiar_nombre_nivel,
            float=True,
            float_origin_position=True,
            font_name=FuenteMinecraftia(tam=int(alto * 0.023))
        ).translate(ancho * 0.5, -(alto * 0.085))

        self.btn_importar: "Button" = self.add.button(
            title="Importar",
            action=self._importar_nivel,
            float=True,
            float_origin_position=True,
            font_name=FuenteMinecraftia(tam=int(alto * 0.025))
        ).translate(ancho * 0.68, -(alto * 0.009))

        self.btn_exportar: "Button" = self.add.button(
            title="Exportar",
            action=self._exportar_nivel,
            float=True,
            float_origin_position=True,
            font_name=FuenteMinecraftia(tam=int(alto * 0.025))
        ).translate(ancho * 0.79, -(alto * 0.009))


    def _procesar_cambio_columnas(self, item: Any, _indice: int, *_args, **_kwargs) -> None:
        """
        Procesa el callback del selector de cambio de columnas.
        -
        'item': El ítem seleccionado actualmente.

        'indice': El índice del ítem seleccionado.

        '*args': Argumentos asociados.

        '**kwargs': Todos los argumentos keyword desconocidos que llegan al callback.
        """

        self.juego_handler.editor_handler.set_ancho(item[1])


    def _procesar_cambio_filas(self, item: Any, _indice: int, *_args, **_kwargs) -> None:
        """
        Procesa el callback del selector de cambio de filas.
        -
        'item': El ítem seleccionado actualmente.

        'indice': El índice del ítem seleccionado.

        '*args': Argumentos asociados.

        '**kwargs': Todos los argumentos keyword desconocidos que llegan al callback.
        """

        self.juego_handler.editor_handler.set_alto(item[1])


    def _cambiar_nombre_nivel(self, nuevo_titulo: str, **_kwargs) -> None:
        """
        Cambia el título del nivel por el texto que hay en el widget correspondiente.
        -
        'nuevo_titulo': El contenido del nuevo nombre.

        '**kwargs': Argumentos desconocidos que entraron en el callback.
        """

        self.nombre_nivel = nuevo_titulo


    def _importar_nivel(self) -> "PathLike":
        "Trata de importar un nivel con el nombre actual."

        try:
            datos_nivel = self.juego_handler.editor_handler.importar(self.nombre_nivel)
            self.nombre_nivel = datos_nivel["titulo"]
        except FileNotFoundError:
            self.juego_handler.editor_handler.refrescar_mensaje("No se encontró el archivo con "
                f"nombre '{'_'.join(self.nombre_nivel.lower().split())}' en la carpeta "
                "de niveles",
                PosicionesMensajesEditor.INFO_ARRIBA
            )


    def _exportar_nivel(self) -> None:
        "Exporta el nivel actual."

        self.juego_handler.editor_handler.exportar(self.nombre_nivel)


    def get_super_kwargs(self) -> "KwargsDict":
        "Devuelve el diccionario de argumentos a usar en la clase madre."

        pantalla = get_surface()
        ancho, alto = pantalla.get_size()

        return dict(title="",
                    width=ancho,
                    height=alto,
                    column_max_width=None,
                    menu_id="menu_editor",
                    position=(0, 0, False),
                    theme=TemaEditor())


    def dibujar_mensajes(self, superficie: "Surface") -> None:
        """
        Dibuja los mensajes del editor.
        -
        'superficie': La superficie sobre la que dibujar.
        """

        ancho, alto = get_surface().get_size()
        mx, my = self.juego_handler.editor_handler.mouse
        fuente = FuenteMinecraftia(tam=int(alto * 0.02))
        fuente_grande = FuenteMinecraftia(tam=int(alto * 0.025))
        sucede_adentro = self.juego_handler.editor_handler.esta_en_area()

        for iden, (mens, temp) in self.juego_handler.editor_handler.mensajes.items():
            if not temp.esta_contando() or iden not in PosicionesMensajesEditor:
                continue

            fuente_img = fuente.render(mens, False, COLOR_MENSAJE)
            fuente_grande_img = fuente_grande.render(mens, False, COLOR_MENSAJE)
            ancho_img, alto_img = fuente_img.get_size()

            if iden == PosicionesMensajesEditor.CURSOR_ARRIBA and sucede_adentro:
                superficie.blit(fuente_img, (mx - (ancho_img * 0.5), my - (alto * 0.06)))

            elif iden == PosicionesMensajesEditor.CURSOR_IZQUIERDA and sucede_adentro:
                superficie.blit(fuente_img, (mx - (ancho * 0.12), my - (alto_img * 0.5)))

            elif iden == PosicionesMensajesEditor.CURSOR_DERECHA and sucede_adentro:
                superficie.blit(fuente_img, (mx + (ancho * 0.035), my - (alto_img * 0.5)))

            elif iden == PosicionesMensajesEditor.CURSOR_ABAJO and sucede_adentro:
                superficie.blit(fuente_img, (mx - (ancho_img * 0.5), my + (alto * 0.06)))

            elif iden == PosicionesMensajesEditor.INFO_ARRIBA:
                superficie.blit(fuente_grande_img, (ancho * 0.15, alto * 0.2))


    def draw(self, surface: Optional["Surface"]=None, clear_surface: bool=False) -> "Menu":
        """
        Dibuja el menú del editor.
        -
        'surface': La superficie sobre la que dibujar.

        'clear_surface': Si refrescar la superficie cada vez.
        """

        self.dibujar_mensajes(surface)
        return super().draw(surface, clear_surface)
