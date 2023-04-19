from PyQt5.QtWidgets import QWidget, QPushButton, QFileDialog
from PyQt5.QtCore import pyqtSlot
from typing import Any

from ..widgets import Button, LineInput, Layout, Label, TextInput, Spacer, Frame
from ..misc import Icons, api
from .. import css


class Category(Frame):
    def __init__(self, parent: QWidget):
        super().__init__(parent, self.__class__.__name__, stylesheet=css.rp_category.css)
        self.category = None

    def init(self) -> 'Category':
        self.setLayout(Layout.vertical().init(
            spacing=20, margins=(0, 0, 0, 20),
            items=[
                Layout.horizontal().init(
                    margins=(20, 0, 20, 0),
                    items=[
                        Button(self, 'FavouriteBtn').init(
                            icon=Icons.STAR.adjusted(size=(30, 30)), slot=self.set_favourite
                        ), Layout.Left,
                        Button(self, 'EditBtn', False).init(
                            icon=Icons.EDIT.adjusted(size=(30, 30)), slot=self.edit_category
                        ),
                        Button(self, 'RemoveBtn', False).init(
                            icon=Icons.TRASH.adjusted(size=(30, 30)), slot=self.delete_category
                        ),
                        Button(self, 'CloseBtn').init(
                            icon=Icons.CROSS.adjusted(size=(30, 30)), slot=self.close_page
                        ), Layout.Right
                    ]
                ),
                Button(self, 'IconBtn').init(
                    icon=Icons.CATEGORY, slot=self.set_icon
                ), Layout.TopCenter,
                LineInput(self, 'TitleInput').init(
                    placeholder='title'
                ), Layout.TopCenter,
                TextInput(self, 'DescriptionInput').init(
                    placeholder='description (optional)'
                ), Layout.TopCenter,
                Spacer(False, True),
                Label(self, 'ErrorLbl').init(
                    wrap=True, alignment=Layout.Center
                ), Layout.Center,
                Button(self, 'CreateBtn').init(
                    text='Create category', slot=self.create_category
                ), Layout.HCenter,
                Frame(self, 'SaveCancelFrame', False).init(
                    layout=Layout.horizontal().init(
                        spacing=50,
                        items=[
                            Button(self, 'SaveBtn').init(
                                text='Save', slot=self.save
                            ), Layout.Left,
                            Button(self, 'CancelBtn').init(
                                text='Cancel', slot=self.cancel
                            ), Layout.Right
                        ]
                    )
                ), Layout.HCenter,
                Button(self, 'AddItemBtn', False).init(
                    text='Add item', icon=Icons.PLUS, slot=self.add_item
                ), Layout.HCenter
            ]
        ))
        self.FavouriteBtn.setProperty('is_favourite', False)
        return self

    def add_item(self):
        RightPages = self.parent()
        Item = RightPages.Item
        Item.category_id = self.category['id']
        RightPages.setCurrentWidget(Item)
        Item.show_create_item()

    @pyqtSlot()
    def close_page(self):
        self.parent().shrink()

    def show_create_category(self):
        self.CreateBtn.setVisible(True)
        self.EditBtn.setVisible(False)
        self.SaveCancelFrame.setVisible(False)
        self.AddItemBtn.setVisible(False)
        self.IconBtn.setDisabled(False)
        self.IconBtn.setIcon(Icons.CATEGORY.icon)
        if self.FavouriteBtn.property('is_favourite'):
            self.FavouriteBtn.click()
        self.TitleInput.setEnabled(True)
        self.TitleInput.setText('')
        self.DescriptionInput.setDisabled(False)
        self.DescriptionInput.setText('')

    @pyqtSlot()
    def delete_category(self):
        category = api.delete_category(self.category['id'])
        self.category = None
        self.TitleInput.setText('')
        self.DescriptionInput.setText('')
        self.RemoveBtn.setVisible(False)
        self.show_create_category()
        self.refresh_categories()

    @pyqtSlot()
    def edit_category(self):
        self.CreateBtn.setVisible(False)
        self.SaveCancelFrame.setVisible(True)
        self.AddItemBtn.setVisible(False)
        self.IconBtn.setDisabled(False)
        self.EditBtn.setVisible(False)
        self.TitleInput.setEnabled(True)
        self.DescriptionInput.setDisabled(False)
        self.RemoveBtn.setVisible(True)

    @pyqtSlot()
    def save(self):
        icon = self.IconBtn.property('icon_bytes')
        title = self.TitleInput.text()
        description = self.DescriptionInput.toPlainText()
        is_favourite = self.findChild(QPushButton, 'FavouriteBtn').property('is_favourite')
        if not len(title):
            return self.ErrorLbl.setText('Title can not be empty')
        category = {'icon': icon, 'title': title, 'description': description, 'is_favourite': is_favourite}
        category = api.update_category(self.category['id'], category)
        if category.get('id', None):
            self.cancel()
            self.category = category
        else:
            self.ErrorLbl.setText('Internal error, please try again')
        self.EditBtn.setVisible(True)
        self.RemoveBtn.setVisible(False)
        self.refresh_categories()

    @pyqtSlot()
    def cancel(self):
        self.ErrorLbl.setText('')
        self.TitleInput.setEnabled(False)
        self.IconBtn.setDisabled(True)
        self.DescriptionInput.setDisabled(True)
        self.SaveCancelFrame.setVisible(False)
        self.AddItemBtn.setVisible(True)
        self.RemoveBtn.setVisible(False)
        self.EditBtn.setVisible(True)

    @pyqtSlot()
    def set_icon(self):
        dialog = QFileDialog()
        filepath, _ = dialog.getOpenFileName(None, 'Choose image', '', 'Images (*.jpg)', options=dialog.Options())
        if filepath:
            with open(filepath, 'rb') as file:
                icon_bytes = file.read()
                self.IconBtn.setProperty('icon_bytes', icon_bytes)
                self.IconBtn.setIcon(Icons.from_bytes(icon_bytes).icon)

    def show_category(self, category: dict[str, Any]):
        self.category = category
        if (not category['is_favourite'] and self.FavouriteBtn.property('is_favourite')) or \
                category['is_favourite'] and not self.FavouriteBtn.property('is_favourite'):
            self.FavouriteBtn.click()
        self.TitleInput.setEnabled(False)
        self.TitleInput.setText(category['title'])
        self.IconBtn.setDisabled(True)
        self.IconBtn.setIcon(Icons.from_bytes(category['icon']).icon)
        self.DescriptionInput.setText(category['description'])
        self.DescriptionInput.setDisabled(True)
        self.ErrorLbl.setText('')
        self.SaveCancelFrame.setVisible(False)
        self.AddItemBtn.setVisible(True)
        self.CreateBtn.setVisible(False)
        self.EditBtn.setVisible(True)

    @pyqtSlot()
    def set_favourite(self):
        is_favourite = self.FavouriteBtn.property('is_favourite')
        self.FavouriteBtn.setProperty('is_favourite', is_favourite := not is_favourite)
        if is_favourite:
            self.FavouriteBtn.setIcon(Icons.STAR_FILL.icon)
        else:
            self.FavouriteBtn.setIcon(Icons.STAR.icon)
        if not self.category:
            return
        self.save()
        self.refresh_categories()

    @pyqtSlot()
    def create_category(self):
        icon = self.IconBtn.property('icon_bytes')
        name = self.TitleInput.text()
        description = self.DescriptionInput.toPlainText()
        is_favourite = self.FavouriteBtn.property('is_favourite')
        if not len(name):
            return self.ErrorLbl.setText('Name can not be empty')
        category = {'icon': icon, 'title': name, 'description': description, 'is_favourite': is_favourite}
        if (category := api.create_category(category)).get('id'):
            self.category = category
            self.TitleInput.setText(category['title'])
            self.IconBtn.setIcon(Icons.from_bytes(category['icon']).icon)
            self.IconBtn.setDisabled(True)
            self.ErrorLbl.setText('')
            self.TitleInput.setEnabled(False)
            self.DescriptionInput.setDisabled(True)
            self.AddItemBtn.setVisible(True)
            self.CreateBtn.setVisible(False)
            self.EditBtn.setVisible(True)
        else:
            self.ErrorLbl.setText('Internal error, please try again')
        self.refresh_categories()

    def refresh_categories(self):
        parent = self.parent().parent().parent().parent()
        LeftMenu = parent.findChild(QWidget, 'LeftMenu')
        categories = api.categories()
        LeftMenu.show_categories(categories)
