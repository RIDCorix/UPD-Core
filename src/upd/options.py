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

class ColorOption(Option):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.editor = ColorPicker

    def to_str(self):
        return str(self.value.toTuple())

    @property
    def value(self):
        return QColor.fromRgb(self._value.rgba())

    def init_ui(self, picker):
        picker.button.setText(self.name)

class FontOption(Option):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.editor = ColorPicker

    def init_ui(self, picker):
        picker.button.setText(self.name)



class DurationOption(Option):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.editor = ColorPicker

    def init_ui(self, picker):
        picker.button.setText(self.name)

class ChoiceOption(Option):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.editor = QComboBox
        self.choices = []

    def choice(self, choices):
        self.choices = choices

    def init_ui(self, combobox):
        index = 0
        for i, choice in enumerate(self.choices):
            if choice['name'] == self._value:
                index = i
            combobox.addItem(choice['name'])

        combobox.setCurrentIndex(index)
        combobox.currentIndexChanged.connect(lambda x: self.change(x))

    def change(self, value):
        self._value = self.choices[value]['name']
