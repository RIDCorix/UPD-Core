from typing import Any

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
        self.value = default
        self.default = default

    def to_str(self):
        return str(self.value)

class ColorOption(Option, ColorPicker):
    def to_str(self):
        return str(self.value.toTuple())

class FontOption(Option):
    pass
