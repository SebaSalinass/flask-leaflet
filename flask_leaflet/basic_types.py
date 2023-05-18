from dataclasses import dataclass, field


class LatLng:
    """Object representing Latitud and Longitud"""

    lat: float
    lng: float
    alt: float = None

    def __init__(self, lat: float, lng: float, alt: float = None) -> None:
        self.lat = lat
        self.lng = lng
        self.alt = alt

    def as_obj(self) -> list[float]:
        return [self.lat, self.lng]


class LatLngBounds:
    corner_1: LatLng
    corner_2: LatLng

    def __init__(self, corner_1: LatLng | list[float], corner_2: LatLng | list[float]) -> None:
        self.corner_1 = corner_1 if isinstance(corner_1, LatLng) else LatLng(*corner_1)
        self.corner_2 = corner_2 if isinstance(corner_2, LatLng) else LatLng(*corner_2)

    def as_obj(self) -> list[float]:
        return [self.corner_1.as_obj(), self.corner_2.as_obj()]


@dataclass
class Point:
    x: int
    y: int

    def __str__(self) -> str:
        return [self.x, self.y]

    def as_obj(self) -> list[float]:
        return [self.x, self.y]


@dataclass(kw_only=True)
class Icon:
    icon_url: str = None
    icon_retina_url: str = None
    icon_size: Point = None
    icon_anchor: Point = None
    popupAnchor: Point = field(default_factory=lambda p: Point(0, 0))
    tooltipAnchor: Point = field(default_factory=lambda p: Point(0, 0))
    shadow_url: str = None
    shadow_retina_url = None
    shadow_size: Point = None
    shadow_anchor: Point = None
    class_name: str = ""
    cross_origin: bool | str = False


@dataclass
class DivIcon(Icon):
    html: str = ""
    bgPos: Point = field(default_factory=lambda p: Point(0, 0))
