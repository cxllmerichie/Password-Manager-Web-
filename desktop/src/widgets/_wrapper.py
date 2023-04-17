from PyQt5.QtWidgets import QWidget
import re


class Wrapper:
    def __init__(self, parent: QWidget = None, name: str = None, visible: bool = True):
        if parent and name:
            setattr(parent, self.__snake_case(name), self)
            self.setObjectName(name)
        self.setVisible(visible)

    @staticmethod
    def __snake_case(name: str) -> str:
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
        return name.lower()
