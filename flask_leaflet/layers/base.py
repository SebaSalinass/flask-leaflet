from uuid import UUID, uuid4
import typing as t
from ..mixins import BaseMixin


class Layer(BaseMixin):
    __not_options__ = BaseMixin.__not_options__ + ["map"]

    attribution: str = None
    pane: str = "overlayPane"
    map: t.Any = None

    def __init__(self, id: UUID = None, attribution: str = None, pane: str = "overlayPane") -> None:
        self.id = id or uuid4()
        self.attribution = attribution
        self.pane = pane


class InteractiveLayer(Layer):
    interactive: bool = True
    bubbling_mouse_events: bool = True

    def __init__(self, interactive: bool = True, bubbling_mouse_events: bool = True, **kwargs) -> None:
        super().__init__(**kwargs)
        self.interactive = interactive
        self.bubbling_mouse_events = bubbling_mouse_events


class HasLayers:
    _layers: list[Layer] = None

    def __init__(self, _layers: list[Layer] = None) -> None:
        self._layers = _layers or []

    def add_layers(self, *layers: Layer) -> None:
        self._layers.extend(layers)
