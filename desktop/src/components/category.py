from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QTextEdit, QFrame, QPushButton, QFileDialog
from PyQt5.QtCore import pyqtSlot
from typing import Any

from ..widgets import Button, VLayout, LInput, HLayout, Label, TInput, Spacer, Frame
from ..misc import Icons, api
from .. import css


class Category(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(css.category.css)
        self.category = None

    def init(self) -> 'Category':
        vbox = VLayout().init(spacing=20, margins=(0, 0, 0, 20))

        hbox = HLayout().init(margins=(20, 0, 20, 0))
        hbox.addWidget(favourite_btn := Button(self, 'FavouriteBtn').init(
            icon=Icons.STAR.adjusted(size=(30, 30)), slot=self.set_favourite
        ), alignment=VLayout.Left)
        hbox.addWidget(edit_btn := Button(self, 'EditBtn').init(
            icon=Icons.EDIT.adjusted(size=(30, 30)), slot=self.edit_category, visible=False
        ))
        hbox.addWidget(remove_btn := Button(self, 'RemoveBtn').init(
            icon=Icons.TRASH.adjusted(size=(30, 30)), slot=self.delete_category, visible=False
        ))
        hbox.addWidget(Button(self, 'CloseBtn').init(
            icon=Icons.CROSS.adjusted(size=(30, 30)), slot=self.close_page
        ), alignment=VLayout.Right)
        vbox.addLayout(hbox)

        vbox.addWidget(Button(self, 'IconBtn').init(
            icon=Icons.CATEGORY, slot=self.set_icon
        ), alignment=VLayout.HCenterTop)
        vbox.addWidget(LInput(self, 'TitleInput').init(
            placeholder='title'
        ), alignment=VLayout.HCenterTop)
        vbox.addWidget(TInput(self, 'DescriptionInput').init(
            placeholder='description (optional)'
        ), alignment=VLayout.HCenterTop)
        vbox.addItem(Spacer(False, True))

        vbox.addWidget(Label(self, 'ErrorLbl').init(
            wrap=True, alignment=VLayout.CenterCenter
        ), alignment=VLayout.CenterCenter)
        vbox.addWidget(Button(self, 'CreateBtn').init(
            text='Create category', slot=self.create_category
        ), alignment=VLayout.HCenter)

        save_cancel_layout = HLayout().init(spacing=50)
        save_cancel_layout.addWidget(Button(self, 'SaveBtn').init(
            text='Save', slot=self.save
        ), alignment=VLayout.Left)
        save_cancel_layout.addWidget(Button(self, 'CancelBtn').init(
            text='Cancel', slot=self.cancel
        ), alignment=VLayout.Right)
        vbox.addWidget(Frame(self, 'SaveCancelFrame').init(
            visible=False, layout=save_cancel_layout
        ), alignment=VLayout.HCenter)

        vbox.addWidget(add_item_btn := Button(self, 'AddItemBtn').init(
            text='Add item', icon=Icons.PLUS, slot=self.add_item, visible=False
        ), alignment=VLayout.HCenter)
        self.setLayout(vbox)

        favourite_btn.setProperty('is_favourite', False)
        return self

    def add_item(self):
        (right_pages := self.parent()).setCurrentIndex(1)
        right_pages.findChild(QFrame, 'Item').show_create_item()

    @pyqtSlot()
    def close_page(self):
        self.parent().shrink()

    def show_create_category(self):
        self.findChild(QPushButton, 'CreateBtn').setVisible(True)
        self.findChild(QPushButton, 'EditBtn').setVisible(False)
        self.findChild(QFrame, 'SaveCancelFrame').setVisible(False)
        self.findChild(QPushButton, 'AddItemBtn').setVisible(False)
        icon_btn = self.findChild(QPushButton, 'IconBtn')
        icon_btn.setDisabled(False)
        icon_btn.setIcon(Icons.CATEGORY.icon)
        favourite_btn = self.findChild(QPushButton, 'FavouriteBtn')
        if favourite_btn.property('is_favourite'):
            favourite_btn.click()
        title_input = self.findChild(QLineEdit, 'TitleInput')
        title_input.setEnabled(True)
        title_input.setText('')
        description_input = self.findChild(QTextEdit, 'DescriptionInput')
        description_input.setDisabled(False)
        description_input.setText('')

    @pyqtSlot()
    def delete_category(self):
        category = api.delete_category(self.category['id'])
        self.findChild(QLineEdit, 'TitleInput').setText('')
        self.findChild(QTextEdit, 'DescriptionInput').setText('')
        self.show_create_category()

    @pyqtSlot()
    def edit_category(self):
        self.findChild(QPushButton, 'CreateBtn').setVisible(False)
        self.findChild(QFrame, 'SaveCancelFrame').setVisible(True)
        self.findChild(QPushButton, 'AddItemBtn').setVisible(False)
        self.findChild(QPushButton, 'IconBtn').setDisabled(False)
        self.findChild(QPushButton, 'EditBtn').setVisible(False)
        self.findChild(QLineEdit, 'TitleInput').setEnabled(True)
        self.findChild(QTextEdit, 'DescriptionInput').setDisabled(False)
        self.findChild(QPushButton, 'RemoveBtn').setVisible(True)

    @pyqtSlot()
    def save(self):
        icon_btn = self.findChild(QPushButton, 'IconBtn')
        title_input = self.findChild(QLineEdit, 'TitleInput')
        description_input = self.findChild(QTextEdit, 'DescriptionInput')
        error_lbl = self.findChild(QLabel, 'ErrorLbl')

        icon = icon_btn.property('icon_bytes')
        title = title_input.text()
        description = description_input.toPlainText()
        is_favourite = self.findChild(QPushButton, 'FavouriteBtn').property('is_favourite')
        if not len(title):
            return error_lbl.setText('Title can not be empty')
        category = {'icon': icon, 'title': title, 'description': description, 'is_favourite': is_favourite}
        category = api.update_category(self.category['id'], category)
        if category.get('id', None):
            self.cancel()
            self.category = category
        else:
            error_lbl.setText('Internal error, please try again')
        self.findChild(QPushButton, 'EditBtn').setVisible(True)
        self.findChild(QPushButton, 'RemoveBtn').setVisible(False)

    @pyqtSlot()
    def cancel(self):
        self.findChild(QLabel, 'ErrorLbl').setText('')
        self.findChild(QLineEdit, 'TitleInput').setEnabled(False)
        self.findChild(QPushButton, 'IconBtn').setDisabled(True)
        self.findChild(QTextEdit, 'DescriptionInput').setDisabled(True)
        self.findChild(QFrame, 'SaveCancelFrame').setVisible(False)
        self.findChild(QPushButton, 'AddItemBtn').setVisible(True)
        self.findChild(QPushButton, 'RemoveBtn').setVisible(False)
        self.findChild(QPushButton, 'EditBtn').setVisible(True)

    @pyqtSlot()
    def set_icon(self):
        dialog = QFileDialog()
        filepath, _ = dialog.getOpenFileName(None, 'Choose image', '', 'Images (*.jpg)', options=dialog.Options())
        if filepath:
            with open(filepath, 'rb') as file:
                icon_bytes = file.read()
                btn = self.findChild(QPushButton, 'IconBtn')
                btn.setProperty('icon_bytes', icon_bytes)
                btn.setIcon(Icons.from_bytes(icon_bytes).icon)

    def show_category(self, category: dict[str, Any]):
        self.category = category
        title_input = self.findChild(QLineEdit, 'TitleInput')
        description_input = self.findChild(QTextEdit, 'DescriptionInput')
        icon_btn = self.findChild(QPushButton, 'IconBtn')

        title_input.setText(category['title'])
        description_input.setText(category['description'])
        icon_btn.setIcon(Icons.from_bytes(category['icon']).icon)
        favourite_btn = self.findChild(QPushButton, 'FavouriteBtn')
        if (not category['is_favourite'] and favourite_btn.property('is_favourite')) or \
                category['is_favourite'] and not favourite_btn.property('is_favourite'):
            favourite_btn.click()
        title_input.setEnabled(False)
        icon_btn.setDisabled(True)
        description_input.setDisabled(True)
        self.findChild(QLabel, 'ErrorLbl').setText('')
        self.findChild(QFrame, 'SaveCancelFrame').setVisible(False)
        self.findChild(QPushButton, 'AddItemBtn').setVisible(True)
        self.findChild(QPushButton, 'CreateBtn').setVisible(False)
        self.findChild(QPushButton, 'EditBtn').setVisible(True)

    @pyqtSlot()
    def set_favourite(self):
        btn = self.findChild(QPushButton, 'FavouriteBtn')
        is_favourite = btn.property('is_favourite')
        btn.setProperty('is_favourite', is_favourite := not is_favourite)
        if is_favourite:
            btn.setIcon(Icons.STAR_FILL.icon)
        else:
            btn.setIcon(Icons.STAR.icon)

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
        category = {'icon': icon, 'title': name, 'description': description, 'is_favourite': is_favourite}
        response = api.create_category(category)
        if response.get('id', None):
            self.category = response
            icon_btn.setIcon(Icons.from_bytes(response['icon']).icon)
            error_lbl.setText('')

            name_input.setEnabled(False)
            icon_btn.setDisabled(True)
            description_input.setDisabled(True)
            self.findChild(QPushButton, 'AddItemBtn').setVisible(True)
            self.findChild(QPushButton, 'CreateBtn').setVisible(False)
            self.findChild(QPushButton, 'EditBtn').setVisible(True)
        else:
            error_lbl.setText('Internal error, please try again')
