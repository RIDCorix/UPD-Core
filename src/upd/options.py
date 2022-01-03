from typing import Any

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QComboBox

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

    def real_time_init(self, *args, **kwargs):
        pass

class ColorOption(Option, ColorPicker):
    def to_str(self):
        return str(self.value.toTuple())

    @property
    def value(self):
        return QColor.fromRgb(self._value.rgba())


class FontOption(Option, ColorPicker):
    pass


class DurationOption(Option, ColorPicker):
    pass

class ChoiceOption(Option, QComboBox):
    def choice(self, args=None, **kwargs):
        if args:
            for arg in args:
                self.addItem('bruh')