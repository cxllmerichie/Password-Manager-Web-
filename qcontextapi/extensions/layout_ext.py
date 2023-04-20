from PyQt5.QtWidgets import QWidget, QLayoutItem, QSpacerItem
from PyQt5.QtCore import Qt, QObject
from typing import Sequence


class LayoutExt:
    def init(
            self, *,
            margins: tuple[int, ...] = (0, 0, 0, 0), spacing: int = 0, alignment: Qt.Alignment = None,
            items: Sequence[QObject] = ()
    ) -> 'LayoutExt':
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
