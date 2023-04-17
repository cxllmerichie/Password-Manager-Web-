from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLayoutItem, QSpacerItem, QHBoxLayout
from PyQt5.QtCore import Qt, QObject
from typing import Iterable, Union
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
    CenterCenter = Qt.AlignHCenter | Qt.AlignVCenter

    @classmethod
    def horizontal(cls, parent: QWidget = None, name: str = None) -> 'HLayout':
        return HLayout(parent, name)

    @classmethod
    def vertical(cls, parent: QWidget = None, name: str = None) -> 'VLayout':
        return VLayout(parent, name)

    @classmethod
    def oriented(cls, orientation: Qt.Orientation, parent: QWidget = None, name: str = None) -> Union['VLayout', 'HLayout']:
        if orientation is Layout.Vertical:
            return Layout.vertical(parent, name)
        else:
            return Layout.horizontal(parent, name)


class QLayoutExtension:
    def init(
            self, *,
            margins: tuple[int, ...] = (0, 0, 0, 0), spacing: int = 0, alignment: Qt.Alignment = None,
            items: Iterable[QObject] = ()
    ) -> 'QLayoutExtension':
        self.setContentsMargins(*margins)
        self.setSpacing(spacing)
        if alignment:
            self.setAlignment(alignment)
        for item in items:
            self.add(item)
        return self

    def add(self, obj: QObject, alignment: Qt.Alignment = None) -> QObject:
        if isinstance(obj, QWidget):
            if alignment:
                self.addWidget(obj, alignment)
            else:
                self.addWidget(obj)
        elif isinstance(obj, QLayoutItem):
            self.addLayout(obj)
        elif isinstance(obj, QSpacerItem):
            self.addSpacerItem(obj)
        else:
            raise TypeError(f'Can not add object to {self} because {obj} has unsupported type {type(obj)}')
        return obj

    def clear(self):
        for i in reversed(range(self.count())):
            self.itemAt(i).widget().setParent(None)


class VLayout(QLayoutExtension, QVBoxLayout, Wrapper):
    def __init__(self, parent: QWidget = None, name: str = None):
        QVBoxLayout.__init__(self, parent)
        Wrapper.__init__(self, parent, name, True)


class HLayout(QLayoutExtension, QHBoxLayout, Wrapper):
    def __init__(self, parent: QWidget = None, name: str = None):
        QHBoxLayout.__init__(self, parent)
        Wrapper.__init__(self, parent, name, True)
