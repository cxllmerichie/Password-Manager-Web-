from qcontextapi.widgets import Button, LineInput, Layout, Label, TextInput, Frame, ScrollArea, Spacer
from qcontextapi.customs import FavouriteButton, ImageButton
from qcontextapi.utils import Icon
from qcontextapi import CONTEXT
from PyQt5.QtWidgets import QWidget, QFrame, QApplication
from PyQt5.QtCore import pyqtSlot
from uuid import uuid4
from typing import Any

from ..misc import ICONS, API
from .. import css


class Field(Frame):
    def __init__(self, parent: QWidget, field: dict[str, Any]):
        self.identifier = str(uuid4())
        name = f'Field{self.identifier}'
        super().__init__(parent, name, stylesheet=css.rp_item.field(name))

        self.field = field

    def init(self) -> 'Field':
        self.setLayout(Layout.horizontal(self, f'FieldLayout').init(
            spacing=5,
            items=[
                LineInput(self, f'FieldNameInput').init(
                    placeholder='name', alignment=Layout.Right
                ),
                LineInput(self, f'FieldValueInput').init(
                    placeholder='value'
                ),
                Button(self, 'FieldHideBtn').init(
                    icon=ICONS.EYE, slot=self.FieldValueInput.toggle_echo
                ),
                Button(self, 'FieldCopyBtn').init(
                    icon=ICONS.COPY, slot=lambda: QApplication.clipboard().setText(self.FieldValueInput.text())
                ),
                Button(self, f'FieldEditBtn').init(
                    icon=ICONS.EDIT.adjusted(size=ICONS.SAVE.size), slot=self.execute_edit
                ),
                Button(self, f'FieldSaveBtn').init(
                    icon=ICONS.SAVE, slot=self.execute_save
                ),
                Button(self, f'FieldDeleteBtn').init(
                    icon=ICONS.CROSS_CIRCLE, slot=self.execute_delete
                )
            ]
        ))

        if self.field and API.item:  # add field to existing item
            self.FieldDeleteBtn.setVisible(False)
            self.FieldNameInput.setText(self.field['name'])
            self.FieldNameInput.setDisabled(True)
            self.FieldValueInput.setText(self.field['value'])
            self.FieldValueInput.hide_echo()
            self.FieldValueInput.setDisabled(True)
            self.FieldSaveBtn.setVisible(False)
            self.FieldEditBtn.setVisible(True)
        elif API.item:  # creating field for existing item
            self.FieldDeleteBtn.setVisible(True)
            self.FieldSaveBtn.setVisible(True)
            self.FieldEditBtn.setVisible(False)
            self.FieldCopyBtn.setVisible(False)
            self.FieldHideBtn.setVisible(False)
        else:  # creating field while creating item
            self.FieldEditBtn.setVisible(False)
            self.FieldSaveBtn.setVisible(True)
            self.FieldCopyBtn.setVisible(False)
            self.FieldHideBtn.setVisible(False)
            self.FieldSaveBtn.setVisible(False)
        return self

    @pyqtSlot()
    def execute_save(self):
        field = {'name': self.FieldNameInput.text(), 'value': self.FieldValueInput.text()}
        if self.field:
            response = API.update_field(self.field['id'], field)
        else:
            response = API.add_field(API.item['id'], field)
        if response.get('id'):
            self.field = response
            self.FieldCopyBtn.setVisible(True)
            self.FieldHideBtn.setVisible(True)
            self.FieldSaveBtn.setVisible(False)
            self.FieldEditBtn.setVisible(True)
            self.FieldDeleteBtn.setVisible(False)
            self.FieldValueInput.hide_echo()
            self.FieldValueInput.setDisabled(True)
            self.FieldNameInput.setDisabled(True)
        else:
            self.setVisible(False)
            self.deleteLater()

    @pyqtSlot()
    def execute_delete(self):
        def delete_ui_field():
            if self.identifier in API.field_identifiers:
                API.field_identifiers.remove(self.identifier)
            self.setVisible(False)
            self.deleteLater()
        if self.field:
            if deleted := API.remove_field(self.field['id']).get('id'):
                delete_ui_field()
            else:
                self.RP_Item.ErrorLbl.setText('Internal error, please try again')
        if self.RP_Item.FieldScrollArea.widget().layout().count() == 2:  # one of them is `HintLbl2`, another `self`
            self.RP_Item.HintLbl2.setVisible(True)
        delete_ui_field()

    @pyqtSlot()
    def execute_edit(self):
        self.FieldCopyBtn.setVisible(False)
        self.FieldHideBtn.setVisible(False)
        self.FieldSaveBtn.setVisible(True)
        self.FieldDeleteBtn.setVisible(True)
        self.FieldEditBtn.setVisible(False)
        self.FieldNameInput.setDisabled(False)
        self.FieldValueInput.setDisabled(False)
        self.FieldValueInput.show_echo()


class RP_Item(Frame):
    def __init__(self, parent: QWidget):
        super().__init__(
            parent, self.__class__.__name__,
            stylesheet=css.rp_item.css + css.components.scroll + css.components.img_btn + css.components.fav_btn
        )

    def init(self) -> 'RP_Item':
        self.setLayout(Layout.vertical().init(
            spacing=20, margins=(25, 10, 25, 20),
            items=[
                Layout.horizontal().init(
                    margins=(0, 0, 0, 20),
                    items=[
                        FavouriteButton(self).init(
                            pre_slot=self.toggle_favourite
                        ), Layout.Left,
                        Button(self, 'EditBtn').init(
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
                    icon=ICONS.ITEM
                ), Layout.TopCenter,
                LineInput(self, 'TitleInput').init(
                    placeholder='title'
                ), Layout.Top,
                TextInput(self, 'DescriptionInput').init(
                    placeholder='description (optional)'
                ), Layout.Top,
                Frame(self, 'AddBtnsFrame').init(
                    layout=Layout.horizontal().init(
                        items=[
                            Button(self, 'AddDocumentBtn').init(
                                text='Add document', icon=ICONS.PLUS
                            ),
                            Button(self, 'AddFieldBtn').init(
                                text='Add field', icon=ICONS.PLUS, slot=self.add_field
                            )
                        ]
                    )
                ),
                ScrollArea(self, 'FieldScrollArea').init(
                    orientation=Layout.Vertical, alignment=Layout.Top, margins=(5, 10, 5, 0), spacing=10,
                    items=[
                        Label(self, 'HintLbl2').init(
                            wrap=True, alignment=Layout.Center,
                            text='Add new field with name "password" or "username" and it\'s value'
                        ), Layout.Center
                    ]
                ),
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
                )
            ]
        ))
        return self

    @pyqtSlot()
    def add_field(self, field: dict[str, Any] = None):
        if self.HintLbl2.isVisible():
            self.HintLbl2.setVisible(False)
        layout = self.FieldScrollArea.widget().layout()
        layout.addWidget(field := Field(self, field).init())
        API.field_identifiers.append(field.identifier)

    @pyqtSlot()
    def add_document(self):
        ...

    @pyqtSlot()
    def execute_edit(self):
        self.CreateBtn.setVisible(False)
        self.EditBtn.setVisible(False)
        self.DeleteBtn.setVisible(True)
        self.SaveCancelFrame.setVisible(True)
        self.TitleInput.setDisabled(False)
        self.DescriptionInput.setDisabled(False)
        self.ImageButton.setDisabled(False)
        self.AddFieldBtn.setVisible(False)
        self.AddDocumentBtn.setVisible(False)
        self.FieldScrollArea.setVisible(False)

    @pyqtSlot()
    def toggle_favourite(self) -> bool:
        if not API.item:
            return True
        updated = API.update_item(API.item['id'], {
            'title': self.TitleInput.text(), 'is_favourite': self.FavouriteButton.is_favourite
        }).get('id')
        if updated:
            category = API.get_category(API.item['category_id'])
            CONTEXT.LeftMenu.refresh_categories()
            CONTEXT.CP_Items.refresh_items()
            return True
        self.ErrorLbl.setText('Internal error, please try again')
        return False

    @pyqtSlot()
    def execute_save(self):
        title = self.TitleInput.text()
        if not len(title):
            return self.ErrorLbl.setText('Title can not be empty')
        updated = API.update_item(API.item['id'], {
            'icon': self.ImageButton.icon_bytes, 'title': title, 'description': self.DescriptionInput.toPlainText(),
            'is_favourite': self.FavouriteButton.is_favourite
        }).get('id')
        if updated:
            self.execute_cancel()
            CONTEXT.LeftMenu.refresh_categories()
            CONTEXT.CP_Items.refresh_items()
        else:
            self.ErrorLbl.setText('Internal error, please try again')

    @pyqtSlot()
    def execute_cancel(self):
        self.ErrorLbl.setText('')
        self.EditBtn.setVisible(True)
        self.DeleteBtn.setVisible(False)
        self.SaveCancelFrame.setVisible(False)
        self.TitleInput.setDisabled(True)
        self.DescriptionInput.setDisabled(True)
        self.ImageButton.setDisabled(True)
        self.AddFieldBtn.setVisible(True)
        self.AddDocumentBtn.setVisible(True)
        self.FieldScrollArea.setVisible(True)

    def show_create(self):
        API.item = None
        self.DeleteBtn.setVisible(False)
        self.ImageButton.setIcon(ICONS.ITEM.icon)
        self.ImageButton.setEnabled(True)
        self.EditBtn.setVisible(False)
        self.TitleInput.setEnabled(True)
        self.TitleInput.setText('')
        self.DescriptionInput.setEnabled(True)
        self.DescriptionInput.setText('')
        self.FieldScrollArea.clear([self.HintLbl2])
        self.CreateBtn.setVisible(True)
        self.FavouriteButton.setVisible(True)
        self.FavouriteButton.click()
        self.FavouriteButton.click()
        self.HintLbl2.setVisible(True)

    def show_item(self, item: dict[str, Any]):
        API.item = item
        self.FavouriteButton.set(API.item['is_favourite'])
        self.TitleInput.setText(API.item['title'])
        self.TitleInput.setEnabled(False)
        self.ImageButton.setIcon(Icon(API.item['icon']).icon)
        self.ImageButton.setDisabled(True)
        self.DescriptionInput.setText(API.item['description'])
        self.DescriptionInput.setDisabled(True)
        self.ErrorLbl.setText('')
        self.SaveCancelFrame.setVisible(False)
        self.EditBtn.setVisible(True)
        self.CreateBtn.setVisible(False)

        self.FieldScrollArea.clear([self.HintLbl2])
        for field in API.item['fields']:
            self.add_field(field)
        self.HintLbl2.setVisible(not len(API.item['fields']))

        CONTEXT.RightPages.setCurrentWidget(CONTEXT.RP_Item)
        CONTEXT.RightPages.expand()

    @pyqtSlot()
    def execute_create(self):
        if not len(title := self.TitleInput.text()):
            return self.ErrorLbl.setText('Title can not be empty')
        created = API.create_item(
            API.category['id'],
            item={'icon': self.ImageButton.icon_bytes, 'description': self.DescriptionInput.toPlainText(),
                  'title': title, 'is_favourite': self.FavouriteButton.is_favourite},
            fields=[{'name': f.FieldNameInput.text(), 'value': f.FieldValueInput.text()
                     } for f in [self.findChild(QFrame, f'Field{identifier}') for identifier in API.field_identifiers]]
        ).get('id')
        if created:
            self.ImageButton.setIcon(Icon(API.item['icon']).icon)
            self.CreateBtn.setVisible(False)
            self.show_item(API.item)
            category = API.get_category(API.item['category_id'])
            CONTEXT.LeftMenu.refresh_categories()
            CONTEXT.CP_Items.refresh_items()
        else:
            self.ErrorLbl.setText('Internal error, please try again')

    @pyqtSlot()
    def execute_delete(self):
        category_id = API.item['category_id']
        deleted = API.delete_item(API.item['id']).get('id')
        if deleted:
            self.execute_cancel()
            self.show_create()
            category = API.get_category(category_id)
            CONTEXT.LeftMenu.refresh_categories()
            CONTEXT.CP_Items.refresh_items()
        else:
            self.ErrorLbl.setText('Internal error, please try again')
