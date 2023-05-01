from PyQt5.QtWidgets import QComboBox, QWidget
from typing import Iterable, Any

from ..extensions import ContextObjectExt
from ..utils import Icon


class Selector(ContextObjectExt, QComboBox):
    class Item:
        def __init__(self, text: str, icon: Icon = None, data: Any = None):
            self.params = []
            if icon:
                self.params.append(icon)
            self.params.append(str(text))
            if data:
                self.params.append(data)

    def __init__(self, parent: QWidget, name: str, visible: bool = True):
        QComboBox.__init__(self)
        ContextObjectExt.__init__(self, parent, name, visible)

    def init(
            self, *,
            items: Iterable[Item] = (), indexchanged: callable = None, textchanged: callable = None
    ) -> 'Selector':
        for item in items:
            self.addItem(*item.params)
        if indexchanged:
            self.currentIndexChanged.connect(indexchanged)
        if textchanged:
            self.currentTextChanged.connect(textchanged)
        return self
