from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLayoutItem, QSpacerItem, QHBoxLayout
from PyQt5.QtCore import Qt, QObject
from typing import Sequence, Union
from abc import ABC

from ._wrapper import Wrapper


class Layout(ABC):
    Horizontal = Qt.Horizontal
    Vertical = Qt.Vertical

    Left = Qt.AlignLeft
    LeftTop = Qt.AlignLeft | Qt.AlignTop
    LeftCenter = Qt.AlignLeft | Qt.AlignVCenter
    LeftBottom = Qt.AlignLeft | Qt.AlignBottom
    Right = Qt.AlignRight
    RightTop = Qt.AlignRight | Qt.AlignTop
    RightCenter = Qt.AlignRight | Qt.AlignVCenter
    RightBottom = Qt.AlignRight | Qt.AlignBottom
    VCenter = Qt.AlignVCenter
    HCenter = Qt.AlignHCenter
    Top = Qt.AlignTop
    TopCenter = Qt.AlignHCenter | Qt.AlignTop
    Bottom = Qt.AlignBottom
    BottomCenter = Qt.AlignHCenter | Qt.AlignBottom
    Center = Qt.AlignHCenter | Qt.AlignVCenter

    @classmethod
    def horizontal(cls, parent: QWidget = None, name: str = None) -> 'HLayout':
        return HLayout(parent, name)

    @classmethod
    def vertical(cls, parent: QWidget = None, name: str = None) -> 'VLayout':
        return VLayout(parent, name)

    @classmethod
    def oriented(cls, orientation: Qt.Orientation, parent: QWidget = None, name: str = None) -> Union['VLayout', 'HLayout']:
        return Layout.vertical(parent, name) if orientation is Layout.Vertical else Layout.horizontal(parent, name)


# class QLayoutExtension(ABC):  # TypeError: metaclass conflict: the metaclass of a derived class must be a (non-strict) subclass of the metaclasses of all its bases
class QLayoutExtension:
    def init(
            self, *,
            margins: tuple[int, ...] = (0, 0, 0, 0), spacing: int = 0, alignment: Qt.Alignment = None,
            items: Sequence[QObject] = ()
    ) -> 'QLayoutExtension':
        self.setContentsMargins(*margins)
        self.setSpacing(spacing)
        if alignment:
            self.setAlignment(alignment)
        self.add_items(items)
        return self

    def add(self, obj: QObject, alignment: Qt.AlignmentFlag = None) -> QObject:
        if isinstance(obj, QWidget):
            if alignment:
                self.addWidget(obj, alignment=alignment)
            else:
                self.addWidget(obj)
        elif isinstance(obj, QSpacerItem):
            self.addSpacerItem(obj)
        elif isinstance(obj, QLayoutItem):
            self.addLayout(obj)
        else:
            raise TypeError(f'Can not add object to {self} because {obj} has unsupported type {type(obj)}')
        return obj

    def add_items(self, items: Sequence[QObject]):
        i = 0
        while i < len(items):
            if i + 1 < len(items) and isinstance(items[i + 1], (Qt.AlignmentFlag, Qt.Alignment)):
                self.add(items[i], items[i + 1])
                i += 1
            else:
                self.add(items[i])
            i += 1

    def clear(self):
        for i in reversed(range(self.count())):
            self.itemAt(i).widget().setParent(None)


class VLayout(Wrapper, QLayoutExtension, QVBoxLayout):
    def __init__(self, parent: QWidget = None, name: str = None):
        QVBoxLayout.__init__(self, parent)
        Wrapper.__init__(self, parent, name, True)


class HLayout(Wrapper, QLayoutExtension, QHBoxLayout):
    def __init__(self, parent: QWidget = None, name: str = None):
        QHBoxLayout.__init__(self, parent)
        Wrapper.__init__(self, parent, name, True)
