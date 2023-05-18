import inspect
import typing as t
from uuid import UUID

from flask import render_template
from markupsafe import Markup


class BaseMixin:
    __not_options__ = ["id", "binded_to", "var_name"]
    __factory__ = []
    __bind_str__ = "addTo"
    __call_as_obj__ = []
    __call_args__ = []
    __binded_str__ = ""
    __binded_attr__ = ""

    id: UUID | str
    binded_to: list = []

    @property
    def var_name(self) -> str:
        return f"{self.__class__.__name__.lower()}_{str(self.id).replace('-','_')}"

    def bind(self, obj: t.Any) -> None:
        if not self.binded_to:
            self.binded_to = []
        self.binded_to.append(obj)

    def __to_camel_case(self, string: str) -> str:
        words = string.split("_")
        if len(words) > 1:
            for i, word in enumerate(words[1:], 1):
                words[i] = word.capitalize()
                if words[i].startswith("3"):
                    words[i] = word.upper()
        return "".join(words)

    def _options(self) -> dict:
        options = {}

        for i in inspect.getmembers(self):
            if (
                not i[0].startswith("_")
                and not inspect.ismethod(i[1])
                and i[0] not in self.__not_options__
                and getattr(self, i[0]) is not None
            ):
                options[self.__to_camel_case(i[0])] = (
                    i[1] if i[0] not in self.__call_as_obj__ else (i[1].as_obj() if i[1] is not None else None)
                )

        return options

    def _args(self) -> list[t.Any]:
        return [getattr(self, name).as_obj() if name in self.__call_as_obj__ else getattr(self, name) for name in self.__call_args__]

    def _binded_attr(self) -> t.Any:
        return (
            getattr(self, self.__binded_attr__).as_obj()
            if self.__binded_attr__ in self.__call_as_obj__
            else getattr(self, self.__binded_attr__)
        )

    def __call__(self, **kwargs) -> Markup:
        for key, val in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, val)

        html = render_template("factory.html", layer=self)
        return Markup(html)
