from typing import Any

from PySide6.QtGui import QColor

from .ui import ColorPicker


class Optionable:
    def __init__(self, **options):
        self.options = options

    def add_options(self, **options):
        self.options.update(options)

class Option:
    def __init__(self, name: str, default: Any, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self._value = default
        self.default = default

    @property
    def value(self):
        return self._value

    def to_str(self):
        return str(self.value)

class ColorOption(Option):
    def to_str(self):
        return str(self.value.toTuple())

    @property
    def value(self):
        return QColor.fromRgb(self._value.rgba())


class FontOption(Option):
    pass


class DurationOption(Option):
    pass