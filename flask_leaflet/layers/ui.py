from ..basic_types import Icon, Point, LatLng
from .base import Layer, InteractiveLayer


class DivOverlay(InteractiveLayer):
    __call_as_obj__ = ["offset"]
    __binded_attr__ = "content"

    offset: Point = None
    class_name: str = ""
    pane: str = None
    content: str = ""

    def __init__(self, offset: Point = None, class_name: str = "", pane: str = None, content: str = "", **kwargs) -> None:
        super().__init__(pane=pane, **kwargs)
        self.offset = offset or Point(0, 0)
        self.class_name = class_name
        self.content = content


class Popup(DivOverlay):
    __not_options__ = DivOverlay.__not_options__ + ["latlng"]
    __factory__ = "popup"
    __bind_str__ = "openOn"
    __call_args__ = ["latlng"]
    __call_as_obj__ = DivOverlay.__call_as_obj__ + [
        "latlng",
        "auto_pan_padding_top_left",
        "auto_pan_padding_bottom_right",
        "auto_pan_padding",
    ]

    __binded_str__ = "bindPopup"

    latlng: LatLng
    pane: str = "popupPane"
    offset: Point = None
    max_width: int = 300
    min_width: int = 50
    max_height: int = None
    auto_pan: bool = True
    auto_pan_padding_top_left: Point = None
    auto_pan_padding_bottom_right: Point = None
    auto_pan_padding: Point = Point(5, 5)
    keep_in_view: bool = False
    close_button: bool = True
    auto_close: bool = True
    close_on_escape_key: bool = True
    close_on_click: bool = None

    def __init__(
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
    ) -> None:
        offset = Point(*offset) if isinstance(offset, (list, tuple)) else offset
        super().__init__(offset=offset, content=content, pane=pane, **kwargs)
        self.latlng = latlng if isinstance(latlng, LatLng) else LatLng(*latlng)
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
    __not_options__ = ["id", "latlng", "map"]
    __factory__ = "tooltip"
    __bind_str__ = "openOn"
    __call_args__ = ["latlng"]
    __call_as_obj__ = ["latlng", "offset"]
    __binded_str__ = "bindTooltip"

    latlng: LatLng
    pane: str = "tooltipPane"
    offset: Point = Point(0, 0)
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


class Marker(Layer):
    __not_options__ = Layer.__not_options__ + ["latlng"]
    __factory__ = "marker"
    __bind_str__ = "addTo"
    __call_args__ = ["latlng"]
    __call_as_obj__ = ["latlng"]

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

    def bind_tooltip(self, content: str, **kwargs) -> Tooltip:
        tooltip = Tooltip(self.latlng, content, **kwargs)
        self.bind(tooltip)
        return tooltip

    def bind_popup(self, content: str, **kwargs) -> Popup:
        popup = Popup(self.latlng, content, **kwargs)
        self.bind(popup)
        return popup


class HasUILayers:
    _layers: list[Layer]

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
        self._layers.append(marker)
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
        self._layers.append(tooltip)
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
        self._layers.append(popup)
        return popup
