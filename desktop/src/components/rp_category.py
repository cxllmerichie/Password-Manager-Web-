from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtCore import pyqtSlot
from typing import Any

from ..widgets import Button, LineInput, Layout, Label, TextInput, Spacer, Frame, ui
from ..custom import FavouriteBtn
from ..misc import Icons, api
from .. import css


class RP_Category(Frame):
    def __init__(self, parent: QWidget):
        super().__init__(parent, self.__class__.__name__, stylesheet=css.rp_category.css)
        self.category = None

    def init(self) -> 'RP_Category':
        self.setLayout(Layout.vertical().init(
            spacing=20, margins=(0, 0, 0, 20),
            items=[
                Layout.horizontal().init(
                    margins=(20, 0, 20, 0),
                    items=[
                        FavouriteBtn(self).init(
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
        self.FavouriteBtn.is_favourite = False
        return self

    def set_favourite(self):
        if self.category:
            self.save()
            self.RightPages.MainView
            self.RightPages.MainView.LeftMenu.refresh_categories(api.categories())

    def add_item(self):
        Item = self.RightPages.RP_Item
        Item.category_id = self.category['id']
        self.RightPages.setCurrentWidget(Item)
        Item.show_create_item()

    @pyqtSlot()
    def close_page(self):
        self.parent().shrink()

    def show_create_category(self):
        self.category = None
        self.CreateBtn.setVisible(True)
        self.EditBtn.setVisible(False)
        self.SaveCancelFrame.setVisible(False)
        self.AddItemBtn.setVisible(False)
        self.IconBtn.setDisabled(False)
        self.IconBtn.setIcon(Icons.CATEGORY.icon)
        if self.FavouriteBtn.is_favourite:
            self.FavouriteBtn.click()
        self.TitleInput.setEnabled(True)
        self.TitleInput.setText('')
        self.DescriptionInput.setDisabled(False)
        self.DescriptionInput.setText('')

    @pyqtSlot()
    def delete_category(self):
        category = api.delete_category(self.category['id'])
        if category:
            self.category = None
            self.TitleInput.setText('')
            self.DescriptionInput.setText('')
            self.RemoveBtn.setVisible(False)
            self.show_create_category()
            self.RightPages.MainView.LeftMenu.refresh_categories(api.categories())
        else:
            self.ErrorLbl.setText('Internal error, please try again')

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
        if not len(title := self.TitleInput.text()):
            return self.ErrorLbl.setText('Title can not be empty')
        category = {'icon': self.IconBtn.property('icon_bytes'), 'title': title,
                    'description': self.DescriptionInput.toPlainText(), 'is_favourite': self.FavouriteBtn.is_favourite}
        if (category := api.update_category(self.category['id'], category)).get('id'):
            self.cancel()
            self.category = category
        else:
            self.ErrorLbl.setText('Internal error, please try again')
        self.EditBtn.setVisible(True)
        self.RemoveBtn.setVisible(False)
        self.RightPages.MainView.LeftMenu.refresh_categories(api.categories())

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
        if (not category['is_favourite'] and self.FavouriteBtn.is_favourite) or \
                category['is_favourite'] and not self.FavouriteBtn.is_favourite:
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
    def create_category(self):
        title = self.TitleInput.text()
        if not len(title):
            return self.ErrorLbl.setText('Title can not be empty')
        category = {
            'icon': self.IconBtn.property('icon_bytes'), 'title': title,
            'description': self.DescriptionInput.toPlainText(), 'is_favourite': self.FavouriteBtn.is_favourite
        }
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
        self.RightPages.MainView.LeftMenu.refresh_categories(api.categories())
