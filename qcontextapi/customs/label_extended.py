from PyQt5.QtWidgets import QWidget, QSizePolicy
from PyQt5.QtCore import Qt, QSize

from ..widgets import Frame, Layout, Label
from ..utils import Icon


class LabelExtended(Frame):
    def __init__(self, parent: QWidget, name: str, visible: bool = True):
        Frame.__init__(self, parent, f'{name}Frame', visible)
        self.__name = name

    def init(
            self, *,

            text: str = '', inner_alignment: Qt.Alignment = None, wrap: bool = False, size: QSize = None,
            icon: Icon = None, elided: bool = False, policy: tuple[QSizePolicy, QSizePolicy] = None,
            margins: tuple[int, ...] = (0, 0, 0, 0), spacing: int = 0, outer_alignment: Qt.Alignment = None
    ) -> 'LabelExtended':
        super().init(layout=Layout.horizontal().init(
            margins=margins, spacing=spacing, alignment=outer_alignment,
            items=[
                Label(self.parent(), self.__name).init(
                    text=text, alignment=inner_alignment, wrap=wrap, size=size, icon=icon, elided=elided, policy=policy
                )
            ]
        ))
        return self
