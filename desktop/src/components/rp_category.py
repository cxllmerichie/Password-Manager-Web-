from qcontextapi.widgets import Button, LineInput, Layout, Label, TextInput, Spacer, Frame
from qcontextapi.customs import FavouriteButton, ImageButton
from qcontextapi.utils import Icon
from qcontextapi import CONTEXT
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot
from typing import Any

from ..misc import ICONS, API
from .. import css


class RP_Category(Frame):
    def __init__(self, parent: QWidget):
        super().__init__(parent, self.__class__.__name__,
                         stylesheet=css.rp_category.css + css.components.fav_btn + css.components.img_btn)

    def init(self) -> 'RP_Category':
        self.setLayout(Layout.vertical().init(
            spacing=20, margins=(25, 10, 25, 20),
            items=[
                Layout.horizontal().init(
                    margins=(0, 0, 0, 20),
                    items=[
                        FavouriteButton(self).init(
                            pre_slot=self.toggle_favourite
                        ), Layout.Left,
                        Button(self, 'EditBtn', False).init(
                            icon=ICONS.EDIT.adjusted(size=(30, 30)), slot=self.execute_edit
                        ),
                        Button(self, 'DeleteBtn', False).init(
                            icon=ICONS.TRASH.adjusted(size=(30, 30)), slot=self.execute_delete
                        ),
                        Button(self, 'CloseBtn').init(
                            icon=ICONS.CROSS.adjusted(size=(30, 30)), slot=CONTEXT.RightPages.shrink
                        ), Layout.Right
                    ]
                ),
                ImageButton(self).init(
                    icon=ICONS.CATEGORY
                ), Layout.TopCenter,
                LineInput(self, 'TitleInput').init(
                    placeholder='title'
                ), Layout.Top,
                TextInput(self, 'DescriptionInput').init(
                    placeholder='description (optional)'
                ), Layout.Top,
                Label(self, 'HintLbl1', False).init(
                    wrap=True, alignment=Layout.Center, text='Hint: Create category like "Social Media" to store '
                                                             'your Twitter, Facebook or Instagram personal data',
                    policy=(Layout.Expanding, Layout.Expanding)
                ),
                Spacer(False, True),
                Label(self, 'ErrorLbl').init(
                    wrap=True, alignment=Layout.Center
                ), Layout.Center,
                Button(self, 'CreateBtn').init(
                    text='Create', slot=self.execute_create
                ),
                Frame(self, 'SaveCancelFrame', False).init(
                    layout=Layout.horizontal().init(
                        spacing=20,
                        items=[
                            Button(self, 'SaveBtn').init(
                                text='Save', slot=self.execute_save
                            ),
                            Button(self, 'CancelBtn').init(
                                text='Cancel', slot=self.execute_cancel
                            )
                        ]
                    )
                ),
                Button(self, 'AddItemBtn', False).init(
                    text='Add item', icon=ICONS.PLUS, slot=self.add_item
                )
            ]
        ))
        return self

    @pyqtSlot()
    def toggle_favourite(self):
        if not API.category:
            return True
        updated = API.update_category(API.category['id'], {
            'title': self.TitleInput.text(), 'is_favourite': self.FavouriteButton.is_favourite
        }).get('id')
        if updated:
            CONTEXT.LeftMenu.refresh_categories()
            return True
        self.ErrorLbl.setText('Internal error, please try again')
        return False

    @pyqtSlot()
    def add_item(self):
        Item = self.RightPages.RP_Item
        self.RightPages.setCurrentWidget(Item)
        Item.show_create()

    def show_create(self):
        API.category = None
        self.HintLbl1.setVisible(True)
        self.CreateBtn.setVisible(True)
        self.EditBtn.setVisible(False)
        self.SaveCancelFrame.setVisible(False)
        self.AddItemBtn.setVisible(False)
        self.ImageButton.setDisabled(False)
        self.ImageButton.setIcon(ICONS.CATEGORY.icon)
        self.FavouriteButton.unset_favourite()
        self.TitleInput.setEnabled(True)
        self.TitleInput.setText('')
        self.DescriptionInput.setDisabled(False)
        self.DescriptionInput.setText('')

        CONTEXT.CP_Items.refresh_items([])
        CONTEXT.RightPages.setCurrentWidget(CONTEXT.RP_Category)
        CONTEXT.RightPages.expand()

    @pyqtSlot()
    def execute_delete(self):
        if API.delete_category(API.category['id']).get('id'):
            self.TitleInput.setText('')
            self.DescriptionInput.setText('')
            self.DeleteBtn.setVisible(False)
            self.show_create()
            CONTEXT.LeftMenu.refresh_categories()
        else:
            self.ErrorLbl.setText('Internal error, please try again')

    @pyqtSlot()
    def execute_edit(self):
        self.CreateBtn.setVisible(False)
        self.SaveCancelFrame.setVisible(True)
        self.AddItemBtn.setVisible(False)
        self.ImageButton.setDisabled(False)
        self.EditBtn.setVisible(False)
        self.TitleInput.setEnabled(True)
        self.DescriptionInput.setDisabled(False)
        self.DeleteBtn.setVisible(True)

    @pyqtSlot()
    def execute_save(self):
        if not len(title := self.TitleInput.text()):
            return self.ErrorLbl.setText('Title can not be empty')
        API.update_category(API.category['id'], {
            'icon': self.ImageButton.icon_bytes, 'title': title,
            'description': self.DescriptionInput.toPlainText(), 'is_favourite': self.FavouriteButton.is_favourite
        })
        if API.category:
            self.execute_cancel()
        else:
            self.ErrorLbl.setText('Internal error, please try again')
        self.EditBtn.setVisible(True)
        self.DeleteBtn.setVisible(False)
        CONTEXT.LeftMenu.refresh_categories()

    @pyqtSlot()
    def execute_cancel(self):
        self.ErrorLbl.setText('')
        self.TitleInput.setEnabled(False)
        self.ImageButton.setDisabled(True)
        self.DescriptionInput.setDisabled(True)
        self.SaveCancelFrame.setVisible(False)
        self.AddItemBtn.setVisible(True)
        self.DeleteBtn.setVisible(False)
        self.EditBtn.setVisible(True)

    def show_category(self, category: dict[str, Any]):
        API.category = category
        self.FavouriteButton.set(API.category['is_favourite'])
        self.TitleInput.setEnabled(False)
        self.TitleInput.setText(API.category['title'])
        self.ImageButton.setDisabled(True)
        self.ImageButton.setIcon(Icon(API.category['icon']).icon)
        self.DescriptionInput.setText(API.category['description'])
        self.DescriptionInput.setDisabled(True)
        self.ErrorLbl.setText('')
        self.SaveCancelFrame.setVisible(False)
        self.AddItemBtn.setVisible(True)
        self.CreateBtn.setVisible(False)
        self.EditBtn.setVisible(True)
        self.DeleteBtn.setVisible(False)
        self.HintLbl1.setVisible(False)

        CONTEXT.RightPages.setCurrentWidget(CONTEXT.RP_Category)
        CONTEXT.RightPages.expand()

        CONTEXT.CentralPages.setCurrentWidget(CONTEXT.CP_Items)
        CONTEXT.CP_Items.refresh_items()

    @pyqtSlot()
    def execute_create(self):
        title = self.TitleInput.text()
        if not len(title):
            return self.ErrorLbl.setText('Title can not be empty')
        API.create_category({
            'icon': self.ImageButton.icon_bytes, 'title': title,
            'description': self.DescriptionInput.toPlainText(), 'is_favourite': self.FavouriteButton.is_favourite
        })
        if API.category:
            self.TitleInput.setText(API.category['title'])
            self.ImageButton.setIcon(Icon(API.category['icon']).icon)
            self.ImageButton.setDisabled(True)
            self.ErrorLbl.setText('')
            self.TitleInput.setEnabled(False)
            self.DescriptionInput.setDisabled(True)
            self.AddItemBtn.setVisible(True)
            self.CreateBtn.setVisible(False)
            self.EditBtn.setVisible(True)
            self.HintLbl1.setVisible(False)
        else:
            self.ErrorLbl.setText('Internal error, please try again')
        CONTEXT.LeftMenu.refresh_categories()
