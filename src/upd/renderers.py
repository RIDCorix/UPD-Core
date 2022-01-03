from PySide6.QtCore import QPoint, QRect
from PySide6.QtGui import QBrush, QColor, QFont, QPainter, QPalette, QPen, QPixmap, QRadialGradient
from .conf import Configuration

renderers = []

class RWidgetRenderer:
    def __init__(self):
        self.name = 'UNDEFINED'
        self.settings = Configuration()

    def apply(self, settings):
        self.settings = settings

    def pre_render(self, widget):
        pass

    def render(self, widget):
        pass

    def post_render(self, widget):
        pass
