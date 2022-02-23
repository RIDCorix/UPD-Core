from typing import Any, Callable, Dict, Hashable, List, Optional, Type

from contextlib import contextmanager
from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6 import QtGui

from PySide6.QtGui import QBrush, QColor, QFont, QPainter, QPalette, QPen, QPixmap, QRadialGradient
from PySide6.QtCore import Property, QEasingCurve, QParallelAnimationGroup, QPoint, QPointF, QPropertyAnimation, QRect, QSize, Qt, Signal, Slot
from PySide6.QtWidgets import QCompleter, QGridLayout, QHBoxLayout, QLineEdit, QPlainTextEdit, QScrollArea, QTabWidget, QTextEdit, QWidget, QVBoxLayout, QPushButton, QLabel, QColorDialog

from .models import RBaseModel


class Renderable:
    def paintEvent(self, e):
        from upd.conf import settings
        renderer = settings.RENDERER

        try:
            getattr(renderer, f'pre_render_{self.widget_type}')(self, e)
        except:
            renderer.pre_render(self, e)

        try:
            getattr(renderer, f'render_{self.widget_type}')(self, e)
        except:
            renderer.render(self, e)

        try:
            getattr(renderer, f'post_render_{self.widget_type}')(self, e)
        except:
            renderer.post_render(self, e)


class Slidable:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.anims = []
        self._slide_running = {}
        self.from_value = None
        self.to_value = None
        self._slide_signal.connect(self._slide)
        self._slide_att = ''
        self._slide_from = 0
        self._slide_to = 1
        self._slide_duration = 500
        self._slide_callback = None
        self._easing = QEasingCurve.OutCubic

    def _slide(self):
        anim = QPropertyAnimation(self, self._slide_att.encode())
        self.anims.append(anim)
        anim.setStartValue(self._slide_from)
        anim.setEndValue(self._slide_to)
        anim.setDuration(self._slide_duration)
        anim.setEasingCurve(self._easing)
        if self._slide_callback:
            callback = self._slide_callback
            anim.finished.connect(lambda :callback())

        anim.start()

    _slide_signal = Signal()

    @Slot()
    def slide(self, att: str, from_value: Any=None, to_value: Any=None, duration: int=500, callback: Optional[str]=None, easing=QEasingCurve.OutCubic):
        self._slide_att = att
        self._slide_from = from_value
        if from_value is None:
            try:
                self._slide_from = getattr(self, att)()
            except:
                self._slide_from = getattr(self, att)

        self._slide_to = to_value
        self._slide_duration = duration
        self._slide_callback = callback
        self._easing = easing
        self._slide_signal.emit()
