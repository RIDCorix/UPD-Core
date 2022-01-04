from PySide6.QtCore import QPoint, QRect
from PySide6.QtGui import QBrush, QColor, QFont, QPainter, QPalette, QPen, QPixmap, QRadialGradient
from .conf import Configuration
from upd.options import Optionable

renderers = {}

class RWidgetRenderer(Optionable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = 'UNDEFINED'

    def pre_render(self, widget, event):
        pass

    def render(self, widget, event):
        pass

    def post_render(self, widget, event):
        pass
