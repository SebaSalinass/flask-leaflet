from uuid import UUID, uuid4
from markupsafe import Markup
from .mixins import Renderable, RenderOptions, RendersVarName


class LatLng(Renderable, RendersVarName):
    """Object representing Latitud and Longitud"""

    lat: float
    lng: float
    alt: float = None

    def __init__(self, lat: float, lng: float, alt: float = None, id: str | UUID = None) -> None:
        self.id = id or uuid4()
        self.lat = lat
        self.lng = lng
        self.alt = alt
    
    def __render_html__(self, as_variable: bool = False) -> Markup:
        string = f"[{self.lat}, {self.lng}]"
        if as_variable:
            string = f"var {self.var_name} = L.latlng({string});"
        return Markup(string)


class LatLngBounds(Renderable, RendersVarName):
    corner_1: LatLng
    corner_2: LatLng

    def __init__(self, corner_1: LatLng | list[float], corner_2: LatLng | list[float], id: str | UUID = None) -> None:
        self.id = id or uuid4()
        self.corner_1 = corner_1 if isinstance(corner_1, LatLng) else LatLng(*corner_1)
        self.corner_2 = corner_2 if isinstance(corner_2, LatLng) else LatLng(*corner_2)

    def __render_html__(self, as_variable: bool = False) -> Markup:        
        string = f"[{str(self.corner_1.__render_html__())}, {str(self.corner_2.__render_html__())}]"
        if as_variable:
            string = f"var {self.var_name} = L.latLngBounds({string});"
        return Markup(string)


class Point(Renderable, RendersVarName):
    x: int
    y: int

    def __init__(self, *args, id: str | UUID = None) -> None:
        if isinstance(args[0], self.__class__):
            self.id = args[0].id or (id or uuid4())
            self.x = args[0].x
            self.y = args[0].y
        elif isinstance(args[0], (tuple, list)) and len(args[0]) == 2:
            self.x, self.y = args[0]
        elif isinstance(args[0], (int, float)) and isinstance(args[1], (int, float)) and len(args) == 2:
            self.x, self.y = list(args)
        else:
            raise ValueError(f'Error trying to intialize Point with given args: {args}')

    def __render_html__(self, as_variable: bool = False) -> Markup:        
        string = f"[{self.x}, {self.y}]"
        if as_variable:
            string = f"var {self.var_name} = L.point({string});"
        return Markup(string)


class Icon(Renderable, RendersVarName, RenderOptions):

    __not_render_options__ = ["id"]
    
    icon_url: str = None
    icon_retina_url: str = None
    icon_size: Point = None
    icon_anchor: Point = None
    popup_anchor: Point = [0,0]
    tooltip_anchor: Point = [0,0]
    shadow_url: str = None
    shadow_retina_url = None
    shadow_size: Point = None
    shadow_anchor: Point = None
    class_name: str = ""
    cross_origin: bool | str = False

    def __init__(self,
                 id: str | UUID = None,
                 icon_url: str = None,
                 icon_retina_url: str = None,
                 icon_size: Point | list[int] = None,
                 icon_anchor: Point | list[int] = None,
                 popup_anchor: Point | list[int] = [0,0],
                 tooltip_anchor: Point | list[int] = [0,0],
                 shadow_url: str = None,
                 shadow_retina_url = None,
                 shadow_size: Point | list[int] = None,
                 shadow_anchor: Point | list[int] = None,
                 class_name: str = "",
                 cross_origin: bool | str = False) -> None:
        self.id = id or uuid4()
        self.icon_url = icon_url
        self.icon_retina_url = icon_retina_url
        self.icon_size = Point(icon_size) if icon_size else None
        self.icon_anchor =  Point(icon_anchor) if icon_anchor else None
        self.popup_anchor =  Point(popup_anchor) if popup_anchor else None
        self.tooltip_anchor =  Point(tooltip_anchor) if tooltip_anchor else None
        self.shadow_url =  shadow_url
        self.shadow_retina_url =  shadow_retina_url
        self.shadow_size = Point(shadow_size) if shadow_size else None
        self.shadow_anchor = Point(shadow_anchor)  if shadow_anchor else None
        self.class_name = class_name
        self.cross_origin = cross_origin

    def __render_html__(self, as_variable: bool = False) -> Markup:
        string = f"L.icon({self.render_options()})"
        if as_variable:
            string = f"var {self.var_name} = {string};"
        return Markup(string)


class DivIcon(Icon):
    html: str = ""
    bg_pos: Point = [0,0]


    def __init__(self, html: str = "", bg_pos:  Point | list[int] = [0,0], **kwargs) -> None:
        super().__init__(**kwargs)
        self.html = html
        self.bg_pos = Point(bg_pos) if bg_pos else None


    def __render_html__(self, as_variable: bool = False) -> Markup:
        string = f"L.divIcon({self.render_options()})"
        if as_variable:
            string = f"var {self.var_name} = {string};"
        return Markup(string)
