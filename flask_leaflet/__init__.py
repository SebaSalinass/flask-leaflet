from typing import Optional

from flask import Flask, Blueprint, Markup, render_template
from .map import Map
from .layers.raster import TileLayer
from .layers.ui import Marker

__all__ = ("Leaflet", "Map", "Marker")


class Leaflet:
    app: Optional[Flask]
    css_local_path: Optional[str] = None
    js_local_path: Optional[str] = None

    config: Optional[dict] = None
    default_tile_layer: TileLayer | None = None

    default_icon_marker_url: str = None
    default_icon_marker_shadow_url: str = None

    def __init__(self, app: Optional[Flask] = None) -> None:
        if app is not None:
            self.init_app(app)

    def __register_blueprint(self, app: Flask) -> Blueprint:
        blueprint = Blueprint(
            "leaflet",
            __name__,
            template_folder="templates",
            static_folder="static",
            static_url_path="/leaflet/static",
        )
        app.register_blueprint(blueprint)

    def init_app(self, app: Flask) -> None:
        if not hasattr(app, "extensions"):
            app.extensions = {}
        app.extensions["leaflet"] = self
        self.app = app

        self.__register_blueprint(self.app)

        self.csp_nonce_callback = self.app.config.get("LEAFLET_NONCE_CALLBACK")
        self.css_local_path = self.app.config.get("LEAFLET_CSS_LOCAL_PATH")
        self.js_local_path = self.app.config.get("LEAFLET_JS_LOCAL_PATH")
        self.default_icon_marker_url = app.config.get("LEAFLET_MARKER_ICON_URL")
        self.default_icon_marker_shadow_url = app.config.get(
            "LEAFLET_MARKER_ICON_SHADOW_URL"
        )

        if url_template := app.config.get("LEAFLET_DEFAULT_RASTER_TILE_URL_TEMPLATE"):
            tile_options = app.config.get("LEAFLET_DEFAULT_RASTER_TILE_OPTIONS")
            self.default_tile_layer = TileLayer(url_template, **tile_options)

        @app.context_processor
        def inject_context_variables() -> dict:
            return dict(leaflet=self)

    def load(self) -> Markup:
        return Markup(
            render_template(
                "load.html",
                css_local_path=self.css_local_path,
                js_local_path=self.js_local_path,
                css_version="1.9.3",
                js_version="1.9.3",
            )
        )

    def render_map(
        self, map: Map, *, class_: str = "", nonce_: str = None, **kwargs
    ) -> Markup:
        for key, val in kwargs.items():
            if hasattr(map, key):
                setattr(map, key, val)

        if not map.has_any_raster_layer() and self.default_tile_layer is not None:
            map.layers.append(self.default_tile_layer)
            self.default_tile_layer.owner = map

        html_string = map.__render_html__(class_)
        nonce_tag = f" nonce={nonce_}" if nonce_ else ""
        js_string = Markup(f"<script{nonce_tag}>{str(map.__render_js__())}</script>")
        return html_string + js_string
