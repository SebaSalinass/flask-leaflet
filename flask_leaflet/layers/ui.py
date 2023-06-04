import typing as t
from ..basic_types import Icon, Point, LatLng
from .base import Layer, InteractiveLayer
from markupsafe import Markup

class DivOverlay(InteractiveLayer):

    offset: Point = None
    class_name: str = ""
    pane: str = None
    content: str = ""

    def __init__(self, offset: Point = None, class_name: str = "", pane: str = None, content: str = "", **kwargs) -> None:
        super().__init__(pane=pane, **kwargs)
        self.offset = Point(*offset) if isinstance(offset, (tuple, list)) else offset
        self.class_name = class_name
        self.content = content


class Popup(DivOverlay):
    __render_args__ = ["latlng"]
    __not_render_options__ = DivOverlay.__not_render_options__ + __render_args__

    latlng: LatLng
    pane: str = "popupPane"
    offset: Point = None
    max_width: int = 300
    min_width: int = 50
    max_height: int = None
    auto_pan: bool = True
    auto_pan_padding_top_left: Point = None
    auto_pan_padding_bottom_right: Point = None
    auto_pan_padding: Point = [5,5]
    keep_in_view: bool = False
    close_button: bool = True
    auto_close: bool = True
    close_on_escape_key: bool = True
    close_on_click: bool = None

    def __init__(
        self,
        latlng: LatLng | list[float, float] = None,
        content: str = "",
        pane: str = "popupPane",
        offset: Point | list[int] = [0, 7],
        max_width: int = 300,
        min_width: int = 50,
        max_height: int = None,
        auto_pan: bool = True,
        auto_pan_padding_top_left: Point | list[int] = None,
        auto_pan_padding_bottom_right: Point | list[int] = None,
        auto_pan_padding: Point | list[int] = [5, 5],
        keep_in_view: bool = False,
        close_button: bool = True,
        auto_close: bool = True,
        close_on_escape_key: bool = True,
        close_on_click: bool = None,
        **kwargs,
    ) -> None:
        super().__init__(offset=offset, content=content, pane=pane, **kwargs)
        self.latlng = LatLng(*latlng) if isinstance(latlng, (tuple, list)) else latlng
        self.max_width = max_width
        self.min_width = min_width
        self.max_height = max_height
        self.auto_pan = auto_pan
        self.auto_pan_padding_top_left = (
            Point(*auto_pan_padding_top_left) if isinstance(auto_pan_padding_top_left, (list, tuple)) else auto_pan_padding_top_left
        )
        self.auto_pan_padding_bottom_right = (
            Point(*auto_pan_padding_bottom_right)
            if isinstance(auto_pan_padding_bottom_right, (list, tuple))
            else auto_pan_padding_bottom_right
        )
        self.auto_pan_padding = Point(*auto_pan_padding) if isinstance(auto_pan_padding, (list, tuple)) else auto_pan_padding
        self.keep_in_view = keep_in_view
        self.close_button = close_button
        self.auto_close = auto_close
        self.close_on_escape_key = close_on_escape_key
        self.close_on_click = close_on_click


class Tooltip(DivOverlay):

    __render_args__ = ["latlng"]
    __not_render_options__ = DivOverlay.__not_render_options__ + __render_args__

    latlng: LatLng
    pane: str = "tooltipPane"
    offset: Point = [0,0]
    direction: str = "auto"
    permanent: bool = False
    opacity: float = 0.9

    def __init__(
        self,
        latlng: list[float, float] | LatLng,
        content: str = "",
        pane: str = "tooltipPane",
        offset: Point = [0, 0],
        direction: str = "auto",
        permanent: bool = False,
        opacity: float = 0.9,
        **kwargs,
    ) -> None:
        offset = Point(*offset) if isinstance(offset, (list, tuple)) else offset
        super().__init__(content=content, pane=pane, offset=offset, **kwargs)
        self.latlng = latlng if isinstance(latlng, LatLng) else LatLng(*latlng)
        self.direction = direction
        self.permanent = permanent
        self.opacity = opacity


class BindsUILayers:
    latlng: LatLng | None
    var_name: str
    ui_layers: list[Tooltip, Popup]

    def add_ui_layer(self, ui_layer: Tooltip | Popup) -> None:
        self.ui_layers.append(ui_layer)

    def new_tooltip(self, content: str = "",
        pane: str = "tooltipPane",
        offset: Point = [0, 0],
        direction: str = "auto",
        permanent: bool = False,
        opacity: float = 0.9,
        **kwargs) -> Tooltip:
        tooltip = Tooltip(self.latlng, content, pane, offset, direction, permanent, opacity, **kwargs)
        self.add_ui_layer(tooltip)
        return tooltip

    def new_popup(self, content: str = "",
        pane: str = "popupPane",
        offset: Point | list[int] = [0, 7],
        max_width: int = 300,
        min_width: int = 50,
        max_height: int = None,
        auto_pan: bool = True,
        auto_pan_padding_top_left: Point | list[int] = None,
        auto_pan_padding_bottom_right: Point | list[int] = None,
        auto_pan_padding: Point | list[int] = [5, 5],
        keep_in_view: bool = False,
        close_button: bool = True,
        auto_close: bool = True,
        close_on_escape_key: bool = True,
        close_on_click: bool = None,
        **kwargs) -> Popup:

        popup = Popup(self.latlng or None,
                     content,
                     pane,
                     offset,
                     max_width,
                     min_width,
                     max_height,
                     auto_pan,
                     auto_pan_padding_top_left,
                     auto_pan_padding_bottom_right,
                     auto_pan_padding,
                     keep_in_view,
                     close_button,
                     auto_close,
                     close_on_escape_key,
                     close_on_click,
                     **kwargs)
        self.add_ui_layer(popup)
        return popup


    def render_ui_layers(self, as_variable: bool = False) -> str:
        string = ""
        if as_variable:
            for ui_layer in self.ui_layers:
                string = ui_layer.__render_html__(as_variable)
                
                string = Markup(f"{string}{self.var_name}.bind{ui_layer.__class__.__name__}({ui_layer.var_name});")
        else:
            for ui_layer in self.ui_layers:
                string += f".bind{ui_layer.__class__.__name__}({ui_layer.__render_html__()})"
        print(string)
        return string


class Marker(BindsUILayers, Layer):
    __render_args__ = ["latlng"]
    __not_render_options__ = Layer.__not_render_options__ + __render_args__ + ["ui_layers"]

    latlng: LatLng
    icon: Icon = None
    keyboard: bool = True
    title: str = ""
    alt: str = "Marker"
    z_index_offset: int = 0
    opacity: float = 1.0
    rise_on_hover: bool = False
    rise_offset: int = 250
    pane: str = "markerPane"
    shadow_pane: str = "shadowPane"
    bubbling_mouse_events: bool = False
    auto_pan_on_focus: bool = True

    def __init__(
        self,
        latlng: list[float, float] | LatLng,
        icon: Icon = None,
        keyboard: bool = True,
        title: str = "",
        alt: str = "Marker",
        z_index_offset: int = 0,
        opacity: float = 1.0,
        rise_on_hover: bool = False,
        rise_offset: int = 250,
        pane: str = "markerPane",
        shadow_pane: str = "shadowPane",
        bubbling_mouse_events: bool = False,
        auto_pan_on_focus: bool = True,
        ui_layers: list[Layer] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.latlng = latlng if isinstance(latlng, LatLng) else LatLng(*latlng)
        self.icon = icon or r"%leaflet_default_icon"
        self.keyboard = keyboard
        self.title = title
        self.alt = alt
        self.z_index_offset = z_index_offset
        self.opacity = opacity
        self.rise_on_hover = rise_on_hover
        self.rise_offset = rise_offset
        self.pane = pane
        self.shadow_pane = shadow_pane
        self.bubbling_mouse_events = bubbling_mouse_events
        self.auto_pan_on_focus = auto_pan_on_focus
        self.ui_layers = ui_layers or []

    def __render_html__(self, as_variable: bool = False) -> Markup:
        string = super().__render_html__(as_variable=as_variable)
        string = string + self.render_ui_layers(as_variable=as_variable)
        return string


class CreatesUILayers:
    layers: list[Layer]

    def new_marker(
        self,
        latlng: list[float, float] | LatLng,
        icon: Icon = None,
        keyboard: bool = True,
        title: str = "",
        alt: str = "Marker",
        z_index_offset: int = 0,
        opacity: float = 1.0,
        rise_on_hover: bool = False,
        rise_offset: int = 250,
        pane: str = "markerPane",
        shadow_pane: str = "shadowPane",
        bubbling_mouse_events: bool = False,
        auto_pan_on_focus: bool = True,
        **kwargs,
    ) -> Marker:
        marker = Marker(
            latlng,
            icon,
            keyboard,
            title,
            alt,
            z_index_offset,
            opacity,
            rise_on_hover,
            rise_offset,
            pane,
            shadow_pane,
            bubbling_mouse_events,
            auto_pan_on_focus,
            **kwargs,
        )
        self.layers.append(marker)
        marker.owner = self
        return marker

    def new_tooltip(
        self,
        latlng: list[float, float] | LatLng,
        content: str = "",
        pane: str = "tooltipPane",
        offset: Point = [0, 0],
        direction: str = "auto",
        permanent: bool = False,
        opacity: float = 0.9,
        **kwargs,
    ) -> Tooltip:
        tooltip = Tooltip(latlng, content, pane, offset, direction, permanent, opacity, **kwargs)
        self.layers.append(tooltip)
        tooltip.owner = self
        return tooltip

    def new_popup(
        self,
        latlng: LatLng | list[float, float],
        content: str = "",
        pane: str = "popupPane",
        offset: Point | list[int] = [0, 7],
        max_width: int = 300,
        min_width: int = 50,
        max_height: int = None,
        auto_pan: bool = True,
        auto_pan_padding_top_left: Point | list[int] = None,
        auto_pan_padding_bottom_right: Point | list[int] = None,
        auto_pan_padding: Point | list[int] = [5, 5],
        keep_in_view: bool = False,
        close_button: bool = True,
        auto_close: bool = True,
        close_on_escape_key: bool = True,
        close_on_click: bool = None,
        **kwargs,
    ) -> Popup:
        popup = Popup(
            latlng,
            content,
            pane,
            offset,
            max_width,
            min_width,
            max_height,
            auto_pan,
            auto_pan_padding_top_left,
            auto_pan_padding_bottom_right,
            auto_pan_padding,
            keep_in_view,
            close_button,
            auto_close,
            close_on_escape_key,
            close_on_click,
            **kwargs,
        )
        self.layers.append(popup)
        popup.owner = self
        return popup
