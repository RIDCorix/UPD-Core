from typing import List, Dict

from PySide6.QtGui import QColor

from upd.options import Optionable, Option, FontOption, ColorOption

class SettingsCategory(Optionable):
    def __getattr__(self, attr):
        return self.options[attr].value

class Configuration:
    def __init__(self, *args, **kwargs):
        self.categories = {}

    def add_category(self, name: str, **settings: Dict[str, Option]):
        self.categories[name] = SettingsCategory(**settings)

    def __getattr__(self, attr):
        try:
            return self.categories[attr]
        except:
            for name, category in self.categories.items():
                return category.options[attr].value

    def to_dict(self):
        settings_map = {}
        for name, category in self.categories.items():
            for setting_name, option in category.options.items():
                settings_map[setting_name] = option.to_str()
        return settings_map

settings = Configuration()

settings.add_category('preference',
    TEXT_COLOR=ColorOption('Text Color', QColor(255, 255, 255)),
    THEME_COLOR=ColorOption('Theme Color', QColor(255, 255, 255)),
    PANEL_COLOR=ColorOption('Panel Color', QColor(0, 0, 0, 100)),
    BORDER_COLOR=ColorOption('Border Color', QColor(255, 255, 255)),
    FONT_MONO=FontOption('Font (mono)', 'Share Tech Mono'),
    FONT_NORMAL=FontOption('Font (normal)', 'caveat'),
    FONT_HANDWRITING=FontOption('Font (handwriting)', 'caveat'),
)
