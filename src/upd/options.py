from typing import Any, List

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QComboBox

from .ui import ColorPicker


class Optionable:
    def __init__(self, **options):
        self.options = options

    def add_options(self, **options):
        self.options.update(options)

    def set_option(self, key: str, value: Any):
        self.options[key] = value

    def get_option(self, key: str) -> Any:
        return self.options[key].value

    def get_options(self, *keys: List[str]) -> Any:
        return [self.get_option(key) for key in keys]


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
