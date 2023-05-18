from .mixins import BaseMixin
from .layers.base import Layer, HasLayers
from .layers.raster import HasRasterLayers
from .layers.ui import HasUILayers
from .layers.paths import HasPathsLayers

from .basic_types import LatLng
import typing as t


class Map(HasLayers, HasRasterLayers, HasUILayers, HasPathsLayers, BaseMixin):
    __call_as_obj__ = ["center", "max_bounds"]

    id: str
    prefer_canvas: bool = True

    attribution_control: bool = True
    zoom_control: bool = True

    close_popup_on_click: bool = True
    box_zoom: bool = True
    double_click_zoom: bool | t.Literal["center"] = True
    dragging: bool = True
    zoom_snap: int = 1
    zoom_delta: int = 1
    track_resize: bool = True

    inertia: bool = False
    inertia_deceleration: int = 3000
    inertia_max_speed: float = float("inf")
    ease_linearity: bool = 0.2
    world_copy_jump: bool = False
    max_bounds_viscosity: float = 0.0

    keyboard: bool = True
    keyboard_pan_delta: int = 80

    scroll_wheel_zoom: bool | str = True
    wheel_debounce_time: int = 40
    wheel_px_per_zoom_level: int = 60

    tap_hold: bool = True
    tap_tolerance: int = 15
    touch_zoom: bool | t.Literal["center"] = False
    bounce_at_zoom_limits: bool = True

    center: LatLng = None
    zoom: int = 14
    min_zoom: int = 0
    max_zoom: int = 18

    layers: list[Layer] = None
    max_bounds: list[LatLng] = None

    zoom_animation: bool = True
    zoom_animation_threshold: int = 4
    fade_animation: bool = True
    marker_zoom_animation: bool = True
    transform_3D_Limit: int = 2**23

    def __init__(
        self,
        id: str,
        center: LatLng | list[float, float] = None,
        zoom: int = 13,
        **kwargs,
    ) -> None:
        super().__init__()
        self.id = id
        self.center = LatLng(*center) if isinstance(center, (list, tuple)) else center
        self.zoom = zoom

        for key, val in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, val)

    def lock_interaction(self) -> None:
        self.keyboard = False
        self.scroll_wheel_zoom = False
        self.box_zoom = False
        self.dragging = False
        self.zoom_control = False
        self.double_click_zoom = False
        self.tap_hold = False

    def unlock_interaction(self) -> None:
        self.keyboard = True
        self.scroll_wheel_zoom = True
        self.box_zoom = True
        self.dragging = True
        self.zoom_control = True
        self.double_click_zoom = True
        self.tap_hold = True
