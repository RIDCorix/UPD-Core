from typing import Any, Hashable, Optional

import datetime

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


class RTabWidget(Renderable, Slidable, QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget_type = 'main_panel'

class RWidget(Renderable, Slidable, QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class RButton(Renderable, Slidable, QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget_type = 'button'


class RLineEdit(Renderable, Slidable, QLineEdit):
    def get_focus_rate(self):
        return self._focus_rate

    def set_focus_rate(self,val):
        self._focus_rate = val
        self.update()

    focus_rate = Property(float, get_focus_rate, set_focus_rate)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget_type = 'line_edit'
        self._focus_rate = 0

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.slide('focus_rate', 0, 1)

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.slide('focus_rate', self.focus_rate, 0)


class MainPanel(RWidget):
    def get_drop_rate(self):
        return self._drop_rate

    def set_drop_rate(self,val):
        self._drop_rate = val
        self.update()

    drop_rate = Property(float, get_drop_rate, set_drop_rate)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._drop_rate = 0.0
        self.widget_type = 'main_panel'
        self.setProperty('type', 'panel')
        self.slide('drop_rate', 0.0, 1.0)
        self.shrink = QPoint(0, 0)


class ConsoleBlock:
    def __init__(self, root=None, parent=None, text='', auto_update=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if root is None:
            self.root = self
        else:
            self.root = root

        self._text = text
        self.parent = parent
        self.blocks = []

        self.auto_update = False
        self._index = 0
        self._title = ''
        self._total = 1

    def finish(self):
        self.console.finish_block(self.block_id)

    def line(self, text:str):
        self.out(str(text))
        self.root.update()

    def progress(self, title:str, done: int, total: int):
        self._title = title
        self._total = total
        self.replace(f'Loading... ({done} of {total}) | {done*100/total} %')

    def done(self):
        self.replace(f'{self._title} ({self._total} of {self._total}) | <font color="green">Done</font>', flush=True)


    def out(self, text: str):
        self.blocks.append(ConsoleBlock(self.root, self, str(text)))
        self.root.update()

    def replace(self, text: str, **kwargs):
        self._text = text
        self.root.update(**kwargs)

    @contextmanager
    def block(self, temp=False):
        block = ConsoleBlock(self.root, self)
        self.blocks.append(block)
        yield block
        if temp:
            del block


    def get_text(self, depth=0, anim=True, flush=False):
        if flush:
            self._index = len(self._text)

        if self._text:
            if anim:
                _text = self._text[:int(self._index)]
            else:
                _text = self._text

            self._index += (len(self._text) - self._index) / 4 + 1

            if self.blocks:
                text = '| . ' * depth + 'o ' + _text + '<br>'
            else:
                text = '| . ' * depth + _text + '<br>'
        else:
            text = ''
            depth -= 1

        for block in self.blocks:
            text += block.get_text(depth+1, anim=anim, flush=flush)
        return text


class Console(QLabel, ConsoleBlock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ConsoleBlock.__init__(self)

    def update(self, *args, **kwargs):
        self.setText(self.get_text(**kwargs))
        super().update()


class ColorPicker(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        self.button = QPushButton()
        self.button.clicked.connect(self.on_clicked)
        layout.addWidget(self.button)

    def on_clicked(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.button.setStyleSheet(f'QPushButton{{color: rgba{color.toTuple()};}}')


class Navigator(MainPanel):
    def get_expand_rate(self):
        return self._focus_rate

    def set_expand_rate(self,val):
        self._focus_rate = val
        self.update()

    expand_rate = Property(float, get_expand_rate, set_expand_rate)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._expand_rate = 0
        self._slide()
        self._parent = self.parent()

        layout = QVBoxLayout()
        self.setLayout(layout)

        head_widget = QWidget()
        head_layout = QHBoxLayout()
        layout.addWidget(head_widget)

        head_widget.setLayout(head_layout)
        head_layout.addWidget(QLabel('Tools'))
        head_layout.addWidget(QPushButton('+'))

    def paintEvent(self, e):
        super().paintEvent(e)

    def on_select(self, callback):
        self.callback_on_select = callback

    def add_option(self, icon, name, data=None):
        option = QPushButton(icon, name)
        option.setProperty('data', data)
        option.clicked.connect(lambda: self.option_selected(data))
        self.layout().addWidget(option)

    def option_selected(self, data):
        self.callback_on_select(data)


class RItem(RButton):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._focus_rate = 0
        self.widget_type = 'item'
        self.label = QLabel(name, self)
        self.label.setAlignment(Qt.AlignCenter | Qt.AlignCenter)

    def get_focus_rate(self):
        return self._focus_rate

    def set_focus_rate(self,val):
        self._focus_rate = val
        self.update()

    focus_rate = Property(float, get_focus_rate, set_focus_rate)

    def enterEvent(self, event):
        super().enterEvent(event)
        self.slide('focus_rate', to_value=1)

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.slide('focus_rate', to_value=0)


class RGridView(RWidget):
    ID_ADD = '__ID_ADD_R_ITEM__'
    _refresh_signal = Signal()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        self.searchbox = RLineEdit()
        self.widget_type = 'grid_view'
        layout.addWidget(self.searchbox)
        self.searchbox.setFont(QFont('Share Tech Mono', 20))

        self.widget = QWidget()
        self.scroll = QScrollArea()
        self.scroll.setProperty('hidden', 'True')
        self.scroll.setStyleSheet('background-color:transparent;')
        self.scroll.setAutoFillBackground(False)
        # self.scroll.background
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidget(self.widget)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)

        layout.addWidget(self.scroll)

        self.index = 0
        self.column_count = 5

        self.model = RBaseModel()

        self.completer = QCompleter(['some', 'words', 'in', 'my', 'dictionary'])
        self.searchbox.setCompleter(self.completer)

        self.model = None
        self.name = None
        self.description = None
        self.add_button = RItem('+', self.widget)
        self.add_button.clicked.connect(self._create)
        self.items = {}

        self.data = []
        self._refresh_signal.connect(self._refresh)
        self.refresh()

    def bind_model(self, model: RBaseModel, name=None, description=None):
        self.model = model
        self.name_attr = name
        self.description = description
        self.refresh_data()

    def get_data(self):
        return self.model.select(getattr(self.model, self.name_attr), self.model.id).dicts()


    @Slot()
    def _refresh(self):
        size = (self.width() / self.column_count * 2/3, 80)
        items_to_remove = list(self.items.keys())
        data = [item for item in self.data if self.searchbox.text() in f'untitled drawer{item["id"]}']
        for i, item in enumerate(data):
            name = item[self.name_attr]
            item_id = item['id']
            name = f'untitled drawer{item_id}'
            if item_id not in self.items:
                r_item = RItem(name, self.widget)
                self.items[item_id] = r_item
                r_item.clicked.connect(lambda:self._select(item))
                r_item.move(self.get_position(0))
                r_item.show()
            try:
                items_to_remove.remove(item_id)
            except:
                pass
            self.items[item_id].slide('size', to_value=QSize(*size))
            self.items[item_id].slide('pos', to_value=self.get_position(i))


        self.add_button.slide('pos', to_value=self.get_position(len(data))+QPoint(*size)/2 - self.add_button.rect().center())


        for item in items_to_remove:
            self.items[item].slide('size', to_value=QSize(0, 0))

        self.widget.setMinimumHeight(self.get_position(len(self.items.keys())+self.column_count).y())

    def refresh_data(self):
        self.data = self.get_data()
        self.completer.setModel(QtCore.QStringListModel([f'untitled drawer{item["id"]}' for item in self.data]))
        self.completer.setFilterMode(Qt.MatchContains)
        self.refresh()

    def refresh(self):
        self._refresh_signal.emit()

    def get_position(self, index):
        x = index % self.column_count
        y = int(index / self.column_count)
        x *= self.width() / self.column_count
        y *= 100
        return QPoint(x, y)

    def on_create(self, function):
        self.callback_on_create = function

    def _create(self):
        self.callback_on_create()
        self.refresh_data()

    def on_select(self, function):
        self.callback_on_select = function

    def _select(self, data):
        self.callback_on_select(data)

    def paintEvent(self, event) -> None:
        self.refresh()
        return super().paintEvent(event)


class RTextEdit(RWidget):
    class _TextEdit(QPlainTextEdit):
        def focusInEvent(self, event):
            super().focusInEvent(event)
            self.parent().slide('focus_rate', 0, 1)

        def focusOutEvent(self, event):
            super().focusOutEvent(event)
            self.parent().slide('focus_rate', self.parent().focus_rate, 0)

    def get_focus_rate(self):
        return self._focus_rate

    def set_focus_rate(self,val):
        self._focus_rate = val
        self.update()

    focus_rate = Property(float, get_focus_rate, set_focus_rate)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_edit = RTextEdit._TextEdit(self)
        self.text_edit.setTabChangesFocus(True)
        self.widget_type = 'text_edit'
        self._focus_rate = 0

    def paintEvent(self, event):
        self.text_edit.resize(self.size())
        super().paintEvent(event)
