from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QTextEdit, QFrame, QPushButton, QFileDialog
from PyQt5.QtCore import pyqtSlot

from ..widgets import Button, VLayout, LInput, HLayout, Label, TInput, Spacer, Frame
from ..misc import Icons, api
from ..css import item


class Item(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(item.css)

    def init(self) -> 'Item':
        vbox = VLayout().init(spacing=20, margins=(0, 0, 0, 20))

        hbox = HLayout().init(margins=(20, 0, 20, 0))
        favourite_btn = Button(self, 'FavouriteBtn').init(
            icon=Icons.STAR.adjusted(size=(30, 30)), slot=self.favourite
        )
        hbox.addWidget(favourite_btn, alignment=VLayout.Left)
        edit_btn = Button(self, 'EditBtn').init(
            icon=Icons.EDIT.adjusted(size=(30, 30)), slot=self.edit_category
        )
        hbox.addWidget(edit_btn)
        hbox.addWidget(Button(self, 'CloseBtn').init(
            icon=Icons.CROSS.adjusted(size=(30, 30)), slot=self.close_page
        ), alignment=VLayout.Right)
        vbox.addLayout(hbox)

        vbox.addWidget(Button(self, 'IconBtn').init(
            icon=Icons.CATEGORY, slot=self.change_icon
        ), alignment=VLayout.HCenterTop)
        vbox.addWidget(LInput(self, 'TitleInput').init(
            placeholder='category name'
        ), alignment=VLayout.HCenterTop)
        vbox.addWidget(TInput(self, 'DescriptionInput').init(
            placeholder='category description (optional)'
        ), alignment=VLayout.HCenterTop)
        vbox.addItem(Spacer(False, True))

        vbox.addWidget(Label(self, 'ErrorLbl').init(
            wrap=True, alignment=VLayout.CenterCenter
        ), alignment=VLayout.CenterCenter)
        vbox.addWidget(Button(self, 'CreateBtn').init(
            text='Create category', slot=self.create_category
        ), alignment=VLayout.HCenter)

        frame = Frame(self, 'SaveCancelFrame').init()
        ctrl_layout = HLayout(frame).init(spacing=50)
        ctrl_layout.addWidget(Button(self, 'SaveBtn').init(
            text='Save', slot=self.save
        ), alignment=VLayout.Left)
        ctrl_layout.addWidget(Button(self, 'CancelBtn').init(
            text='Cancel', slot=self.cancel
        ), alignment=VLayout.Right)
        vbox.addWidget(frame, alignment=VLayout.HCenter)

        add_item_btn = Button(self, 'AddItemBtn').init(
            text='Add item', icon=Icons.PLUS, slot=self.add_item
        )
        vbox.addWidget(add_item_btn, alignment=VLayout.HCenter)
        self.setLayout(vbox)

        add_item_btn.setVisible(False)
        edit_btn.setVisible(False)
        frame.setVisible(False)
        favourite_btn.setProperty('is_favourite', False)
        return self

    @pyqtSlot()
    def add_item(self):
        ...

    @pyqtSlot()
    def close_page(self):
        self.parent().shrink()

    @pyqtSlot()
    def edit_category(self):
        self.findChild(QPushButton, 'CreateBtn').setVisible(False)
        self.findChild(QFrame, 'SaveCancelFrame').setVisible(True)
        self.findChild(QPushButton, 'AddItemBtn').setVisible(False)
        self.findChild(QLineEdit, 'TitleInput').setEnabled(True)
        self.findChild(QPushButton, 'IconBtn').setDisabled(False)
        self.findChild(QTextEdit, 'DescriptionInput').setDisabled(False)

    @pyqtSlot()
    def save(self):
        icon_btn = self.findChild(QPushButton, 'IconBtn')
        name_input = self.findChild(QLineEdit, 'TitleInput')
        description_input = self.findChild(QTextEdit, 'DescriptionInput')
        error_lbl = self.findChild(QLabel, 'ErrorLbl')

        icon = icon_btn.property('icon_bytes')
        name = name_input.text()
        description = description_input.toPlainText()
        is_favourite = self.findChild(QPushButton, 'FavouriteBtn').property('is_favourite')
        if not len(name):
            return error_lbl.setText('Name can not be empty')
        body = {'icon': icon, 'name': name, 'description': description, 'is_favourite': is_favourite}
        response = api.update_category(self.property('category')['id'], body, self.app().token())
        if response.get('id', None):
            self.cancel()
            self.setProperty('category', category)
        else:
            error_lbl.setText('Internal error, please try again')

    @pyqtSlot()
    def cancel(self):
        self.findChild(QLabel, 'ErrorLbl').setText('')
        self.findChild(QLineEdit, 'TitleInput').setEnabled(False)
        self.findChild(QPushButton, 'IconBtn').setDisabled(True)
        self.findChild(QTextEdit, 'DescriptionInput').setDisabled(True)
        self.findChild(QFrame, 'SaveCancelFrame').setVisible(False)
        self.findChild(QPushButton, 'AddItemBtn').setVisible(True)

    @pyqtSlot()
    def change_icon(self):
        dialog = QFileDialog()
        filepath, _ = dialog.getOpenFileName(None, 'Choose image', '', 'Images (*.jpg)', options=dialog.Options())
        if filepath:
            with open(filepath, 'rb') as file:
                icon_bytes = file.read()
                btn = self.findChild(QPushButton, 'IconBtn')
                btn.setProperty('icon_bytes', icon_bytes)
                btn.setIcon(Icons.from_bytes(icon_bytes))

    def set_category(self, c):
        self.setProperty('category', c)
        name_input = self.findChild(QLineEdit, 'TitleInput')
        description_input = self.findChild(QTextEdit, 'DescriptionInput')
        icon_btn = self.findChild(QPushButton, 'IconBtn')

        name_input.setText(c['name'])
        description_input.setText(c['description'])
        icon_btn.setIcon(Icons.from_bytes(c['icon'].encode()))
        favourite_btn = self.findChild(QPushButton, 'FavouriteBtn')
        if (not c['is_favourite'] and favourite_btn.property('is_favourite')) or \
                c['is_favourite'] and not favourite_btn.property('is_favourite'):
            favourite_btn.click()
        name_input.setEnabled(False)
        icon_btn.setDisabled(True)
        description_input.setDisabled(True)
        self.findChild(QLabel, 'ErrorLbl').setText('')
        self.findChild(QFrame, 'SaveCancelFrame').setVisible(False)
        self.findChild(QPushButton, 'AddItemBtn').setVisible(True)
        self.findChild(QPushButton, 'CreateBtn').setVisible(False)
        self.findChild(QPushButton, 'EditBtn').setVisible(True)

    @pyqtSlot()
    def favourite(self):
        btn = self.findChild(QPushButton, 'FavouriteBtn')
        is_favourite = btn.property('is_favourite')
        btn.setProperty('is_favourite', is_favourite := not is_favourite)
        if is_favourite:
            btn.setIcon(Icons.STAR_FILL.icon)
        else:
            btn.setIcon(Icons.STAR.icon)

    def app(self):
        return self.parent().parent().parent().parent().parent()

    @pyqtSlot()
    def create_category(self):
        icon_btn = self.findChild(QPushButton, 'IconBtn')
        name_input = self.findChild(QLineEdit, 'TitleInput')
        description_input = self.findChild(QTextEdit, 'DescriptionInput')
        error_lbl = self.findChild(QLabel, 'ErrorLbl')

        icon = icon_btn.property('icon_bytes')
        name = name_input.text()
        description = description_input.toPlainText()
        is_favourite = self.findChild(QPushButton, 'FavouriteBtn').property('is_favourite')
        if not len(name):
            return error_lbl.setText('Name can not be empty')
        body = {'icon': icon, 'name': name, 'description': description, 'is_favourite': is_favourite}
        response = api.create_category(body, self.app().token())

        if response.get('id', None):
            self.setProperty('category', response)
            icon_btn.setIcon(Icons.from_bytes(response['icon'].encode()))
            error_lbl.setText('')

            name_input.setEnabled(False)
            icon_btn.setDisabled(True)
            description_input.setDisabled(True)
            self.findChild(QPushButton, 'AddItemBtn').setVisible(True)
            self.findChild(QPushButton, 'CreateBtn').setVisible(False)
            self.findChild(QPushButton, 'EditBtn').setVisible(True)
        else:
            error_lbl.setText('Internal error, please try again')
