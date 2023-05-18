from .base import Layer
from ..basic_types import LatLng
from .ui import Tooltip, Popup
import typing as t


class Path(Layer):
    stroke: bool = True
    color: str = "#3388ff"
    weight: int = 3
    opacity: float = 1.0
    line_cap: str = "round"
    line_join: str = "round"
    dash_array: str = None
    dash_offset: str = None
    fill: bool = True
    fill_color: str = color
    fill_opacity: float = 0.2
    fill_rule: str = "evenodd"
    bubbling_mouse_events: bool = True
    # renderer
    class_name: str = None

    def __init__(
        self,
        stroke: bool = True,
        color: str = "#3388ff",
        weight: int = 3,
        opacity: float = 1.0,
        line_cap: str = "round",
        line_join: str = "round",
        dash_array: str = None,
        dash_offset: str = None,
        fill: bool = True,
        fill_color: str = color,
        fill_opacity: float = 0.2,
        fill_rule: str = "evenodd",
        bubbling_mouse_events: bool = True,
        class_name: str = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.stroke = stroke
        self.color = color
        self.weight = weight
        self.opacity = opacity
        self.line_cap = line_cap
        self.line_join = line_join
        self.dash_array = dash_array
        self.dash_offset = dash_offset
        self.fill = fill
        self.fill_color = fill_color
        self.fill_opacity = fill_opacity
        self.fill_rule = fill_rule
        self.bubbling_mouse_events = bubbling_mouse_events
        self.class_name = class_name

    def bind_tooltip(self, content: str, **kwargs) -> Tooltip:
        tooltip = Tooltip(self.latlng, content, **kwargs)
        self.bind(tooltip)
        return tooltip

    def bind_popup(self, content: str, **kwargs) -> Popup:
        popup = Popup(self.latlng, content, **kwargs)
        self.bind(popup)
        return popup


class CircleMarker(Path):
    __not_options__ = Path.__not_options__ + ["latlng"]
    __factory__ = "circleMarker"
    __bind_str__ = "addTo"
    __call_args__ = ["latlng"]
    __call_as_obj__ = ["latlng"]

    latlng: LatLng | list[float]
    radius: int = 10

    def __init__(self, latlng: LatLng | list[float], radius: int = 10, **kwargs) -> None:
        super().__init__(**kwargs)
        self.latlng = latlng if isinstance(latlng, LatLng) else LatLng(*latlng)
        self.radius = radius


class Polyline(Path):
    __not_options__ = Path.__not_options__ + ["latlngs"]
    __factory__ = "polyline"
    __bind_str__ = "addTo"
    __call_args__ = ["latlngs"]
    __call_as_obj__ = ["latlngs"]

    latlngs: list[LatLng]

    smooth_factor: float = 1.0
    no_clip: bool = False

    def __init__(self, latlngs: list[LatLng] | list[list[float]], smooth_fator: float = 1.0, no_clip: bool = False, **kwargs) -> None:
        super().__init__(**kwargs)
        self.latlngs = self.__check_latlngs(latlngs)
        self.smooth_factor = smooth_fator
        self.no_clip = no_clip

    def __check_latlngs(self, latlngs: list[LatLng] | list[list[float]]) -> list[LatLng]:
        out_latlngs = []

        for content in latlngs:
            if isinstance(content, (tuple, list, t.Iterable)):
                if len(content) > 2:
                    out_latlngs.append(self.__check_latlngs(content))
                else:
                    out_latlngs.append(LatLng(*content))

            elif isinstance(content, LatLng):
                out_latlngs.append(content)

        return out_latlngs


class Polygon(Polyline):
    __factory__ = "polygon"

    def __init__(self, latlngs: list[LatLng] | list[list[float]], **kwargs) -> None:
        super().__init__(latlngs, **kwargs)


class Rectangle(Polygon):
    __factory__ = "rectangle"

    def __init__(self, latlngs: list[LatLng] | list[list[float]], **kwargs) -> None:
        super().__init__(latlngs, **kwargs)


class Circle(CircleMarker):
    __factory__ = "circle"

    def __init__(self, latlng: LatLng | list[float], radius: int = 10, **kwargs) -> None:
        super().__init__(latlng, radius, **kwargs)


class HasPathsLayers:
    _layers: list[Layer]

    def new_polyline(
        self, latlngs: list[LatLng] | list[list[float]], smooth_fator: float = 1.0, no_clip: bool = False, **kwargs
    ) -> Polyline:
        polyline = Polyline(latlngs, smooth_fator, no_clip, **kwargs)
        self._layers.append(polyline)
        return polyline

    def new_polygon(self, latlngs: list[LatLng] | list[list[float]], **kwargs) -> Polygon:
        polygon = Polygon(latlngs, **kwargs)
        self._layers.append(polygon)
        return polygon

    def new_rectangle(self, latlngs: list[LatLng] | list[list[float]], **kwargs) -> Rectangle:
        rectangle = Rectangle(latlngs, **kwargs)
        self._layers.append(rectangle)
        return rectangle

    def new_circle(self, latlng: LatLng | list[float], radius: int = 10, **kwargs) -> Circle:
        circle = Circle(latlng, radius, **kwargs)
        self._layers.append(circle)
        return circle
