from PyQt5.QtWidgets import QWidget, QLineEdit, QScrollArea, QVBoxLayout, QCompleter, QTextEdit, QShortcut, QPushButton
from PyQt5.QtCore import Qt, QMargins
from PyQt5.QtGui import QKeySequence
from json import load, dump

from .item import Item


class Application(QWidget):
    def __init__(self, path: str = '../data.json'):
        super().__init__()
        self.setWindowTitle('Password Manager')
        self.setObjectName('Application')

        self.scrollbar_widget_layout = QVBoxLayout()

        self.scrollbar_widget = QWidget()
        self.scrollbar_widget.setObjectName('SearchBarWidget')
        self.scrollbar_widget.setLayout(self.scrollbar_widget_layout)

        self.data = self.__data(path)
        self.widgets = self.__widgets()

        self.searchbar = self.__searchbar()
        self.scroll = self.__scroll()

        self.setLayout(self.__layout())

        self.__shortcuts()

    def __scroll(self):
        scroll = QScrollArea()
        scroll.setObjectName('ScrollArea')
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.scrollbar_widget)
        return scroll

    def __layout(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(QMargins(0, 0, 0, 0))
        layout.addWidget(self.searchbar)
        layout.addWidget(self.__add())
        layout.addWidget(self.scroll)
        return layout

    def __widgets(self):
        widgets = []
        for key, value in self.data.items():
            item = Item(key, value)
            self.scrollbar_widget_layout.addWidget(item)
            widgets.append(item)
        return widgets

    def __data(self, path: str):
        with open(path, 'r') as file:
            return load(file)

    def __searchbar(self):
        search = QLineEdit()
        search.setPlaceholderText('Search with key:')
        search.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        search.setObjectName('SearchBar')
        search.textChanged.connect(self.__update)
        search.setCompleter(self.__completer())
        return search

    def __completer(self):
        completer = QCompleter(list(self.data.keys()))
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        return completer

    def __update(self, text):
        for widget in self.widgets:
            if isinstance(widget, QPushButton):
                continue
            if text.lower() in widget.objectName().lower():
                widget.show()
            else:
                widget.hide()

    def __shortcut(self, keys: str, function) -> QShortcut:
        shortcut = QShortcut(QKeySequence(keys), self)
        shortcut.activated.connect(function)
        return shortcut

    def __save(self):
        data = {}
        for item in self.widgets:
            key = item.findChild(QTextEdit, 'Key').toPlainText()
            value = item.findChild(QTextEdit, 'Value').toPlainText()
            data[key] = value
        with open('../data.json', 'w') as file:
            dump(data, file, indent=4)

    def __find(self):
        self.findChild(QLineEdit, 'SearchBar').setFocus()

    def __shortcuts(self):
        self.__shortcut('Ctrl+S', self.__save)
        self.__shortcut('Ctrl+F', self.__find)
        self.__shortcut('Ctrl+N', self.__new)
        self.__shortcut('Ctrl+Q', self.close)

    def __new(self):
        item = Item('', '')
        self.scrollbar_widget_layout.addWidget(item)
        self.widgets.append(item)

    def __add(self):
        btn = QPushButton()
        btn.setObjectName('PushButton')
        btn.setText('+')
        btn.clicked.connect(self.__new)
        return btn
