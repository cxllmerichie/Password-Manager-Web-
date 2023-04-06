from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QTextEdit, QFrame, QPushButton, QFileDialog

from ..widgets import Button, VLayout, LInput, HLayout, Label, TInput, Spacer
from ..misc import Icons, api
from ..css import category


class Category(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(category.css)

    async def init(self) -> 'Category':
        vbox = await VLayout().init(spacing=20, margins=(0, 0, 0, 20))

        hbox = await HLayout().init(margins=(20, 0, 20, 0))
        hbox.addWidget(await Button(self, 'FavouriteBtn').init(
            icon=Icons.STAR.adjusted(size=(30, 30)), slot=self.favourite
        ), alignment=VLayout.Left)
        hbox.addWidget(await Button(self, 'CloseBtn').init(
            icon=Icons.CROSS.adjusted(size=(30, 30))
        ), alignment=VLayout.Right)
        vbox.addLayout(hbox)

        vbox.addWidget(await Button(self, 'IconBtn').init(
            icon=Icons.CATEGORY, slot=self.change_icon
        ), alignment=VLayout.HCenterTop)
        vbox.addWidget(await LInput(self, 'NameInput').init(
            placeholder='category name'
        ), alignment=VLayout.HCenterTop)
        vbox.addWidget(await TInput(self, 'DescriptionInput').init(
            placeholder='category description (optional)'
        ), alignment=VLayout.HCenterTop)
        vbox.addItem(Spacer(False, True))

        vbox.addWidget(await Label(self, 'ErrorLbl').init(wrap=True), alignment=VLayout.CenterCenter)
        vbox.addWidget(await Button(self, 'MainBtn').init(
            text='Create category', slot=self.create_category
        ), alignment=VLayout.HCenter)

        self.findChild(QPushButton, 'FavouriteBtn').setProperty('is_favourite', False)
        self.setLayout(vbox)
        return self

    def change_icon(self):
        dialog = QFileDialog()
        filepath, _ = dialog.getOpenFileName(None, 'Choose image', '', 'Images (*.jpg)', options=dialog.Options())
        if filepath:
            with open(filepath, 'rb') as file:
                icon_bytes = file.read()
                btn = self.findChild(QPushButton, 'IconBtn')
                btn.setProperty('icon', icon_bytes)
                btn.setIcon(Icons.from_bytes(icon_bytes))

    def favourite(self):
        btn = self.findChild(QPushButton, 'FavouriteBtn')
        is_favourite = btn.property('is_favourite')
        if is_favourite:
            btn.setIcon(Icons.STAR.icon)
        else:
            btn.setIcon(Icons.STAR_FILL.icon)
        btn.setIconSize(Icons.STAR.size)
        btn.setProperty('is_favourite', not is_favourite)

    @property
    def app(self):
        parent = self.parent().parent().parent().parent()
        print(parent)
        return parent

    def create_category(self):
        icon = self.findChild(QPushButton, 'IconBtn').property('icon')
        name = self.findChild(QLineEdit, 'NameInput').text()
        if not len(name):
            return self.findChild(QLabel, 'ErrorLbl').setText('Name can not be empty')
        description = self.findChild(QTextEdit, 'DescriptionInput').text()
        is_favourite = self.findChild(QPushButton, 'FavouriteBtn').property('is_favourite')
        body = {'icon': icon, 'name': name, 'description': description, 'is_favourite': is_favourite}
        token = self.app.settings().value('token')
        response = api.create_category(body, token)
