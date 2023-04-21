from PyQt5.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt
from typing import Union
from abc import ABC

from ..extensions import ContextObjectExt
from ..extensions import LayoutExt


class Layout(ABC):
    Expanding = QSizePolicy.Expanding
    Minimum = QSizePolicy.Minimum
    Maximum = QSizePolicy.Maximum
    MinimumExpanding = QSizePolicy.MinimumExpanding

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


class VLayout(ContextObjectExt, LayoutExt, QVBoxLayout):
    def __init__(self, parent: QWidget = None, name: str = None):
        QVBoxLayout.__init__(self, parent)
        ContextObjectExt.__init__(self, parent, name, True)


class HLayout(ContextObjectExt, LayoutExt, QHBoxLayout):
    def __init__(self, parent: QWidget = None, name: str = None):
        QHBoxLayout.__init__(self, parent)
        ContextObjectExt.__init__(self, parent, name, True)
