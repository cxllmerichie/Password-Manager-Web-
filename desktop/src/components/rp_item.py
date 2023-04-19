from PyQt5.QtWidgets import QWidget, QFrame
from PyQt5.QtCore import pyqtSlot
from uuid import uuid4
from typing import Any

from ..widgets import Button, LineInput, Layout, Label, TextInput, Spacer, Frame, ScrollArea, ui
from ..custom import FavouriteButton, ImageButton
from ..misc import Icons, api, Colors
from .. import css


class Field(Frame):
    def __init__(self, parent: QWidget, item_id: int, field: dict[str, Any] = None):
        self.identifier = str(uuid4())

        super().__init__(parent, f'Field{self.identifier}', stylesheet=css.rp_item.field + f'''
            #Field{self.identifier} {{
                background-color: {Colors.GRAY};
                border-radius: 5px;
            }}
        ''')

        self.item_id = item_id
        self.field = field

    def init(self) -> 'Field':
        self.setLayout(Layout.horizontal(self, f'FieldLayout').init(
            spacing=5,
            items=[
                LineInput(self, f'InputFieldName').init(
                    placeholder='name', alignment=Layout.Right
                ),
                LineInput(self, f'InputFieldValue').init(
                    placeholder='value'
                ),
                Button(self, 'InputFieldValueHideBtn').init(
                    icon=Icons.EYE, slot=self.InputFieldValue.toggle_echo
                ),
                Button(self, 'InputFieldValueCopyBtn').init(
                    icon=Icons.COPY
                ),
                Button(self, f'EditInputFieldBtn').init(
                    icon=Icons.EDIT.adjusted(size=Icons.SAVE.size), slot=self.execute_edit
                ),
                Button(self, f'SaveInputFieldBtn').init(
                    icon=Icons.SAVE, slot=self.execute_save
                ),
                Button(self, f'RemoveInputFieldBtn').init(
                    icon=Icons.CROSS_CIRCLE, slot=self.execute_delete
                )
            ]
        ))

        if self.field:
            self.RemoveInputFieldBtn.setVisible(False)
            self.InputFieldName.setText(self.field['name'])
            self.InputFieldName.setDisabled(True)
            self.InputFieldValue.setText(self.field['value'])
            self.InputFieldValue.hide_echo()
            self.InputFieldValue.setDisabled(True)
            self.SaveInputFieldBtn.setVisible(False)
            self.EditInputFieldBtn.setVisible(True)
        else:
            self.EditInputFieldBtn.setVisible(False)
            self.SaveInputFieldBtn.setVisible(True)
            self.InputFieldValueCopyBtn.setVisible(False)
            self.InputFieldValueHideBtn.setVisible(False)
            self.SaveInputFieldBtn.setVisible(False)
        return self

    @pyqtSlot()
    def execute_save(self):
        field = {'name': self.InputFieldName.text(), 'value': self.InputFieldValue.text()}
        if self.field:
            response = api.update_field(self.field['id'], field)
        else:
            response = api.add_field(self.item_id, field)
        if response.get('id'):
            self.InputFieldValueCopyBtn.setVisible(True)
            self.InputFieldValueHideBtn.setVisible(True)
            self.SaveInputFieldBtn.setVisible(False)
            self.EditInputFieldBtn.setVisible(True)
            self.RemoveInputFieldBtn.setVisible(False)
            self.InputFieldValue.hide_echo()
            self.InputFieldValue.setDisabled(True)
            self.InputFieldName.setDisabled(True)
            self.field = response
        else:
            self.setVisible(False)
            self.deleteLater()

    @pyqtSlot()
    def execute_delete(self):
        self.setVisible(False)
        self.RP_Item.remove(self.identifier)
        if self.field:
            api.remove_field(self.field['id'])

    @pyqtSlot()
    def execute_edit(self):
        self.InputFieldValueCopyBtn.setVisible(False)
        self.InputFieldValueHideBtn.setVisible(False)
        self.SaveInputFieldBtn.setVisible(True)
        self.RemoveInputFieldBtn.setVisible(True)
        self.EditInputFieldBtn.setVisible(False)
        self.InputFieldName.setDisabled(False)
        self.InputFieldValue.setDisabled(False)
        self.InputFieldValue.show_echo()


class RP_Item(Frame):
    def __init__(self, parent: QWidget):
        super().__init__(parent, self.__class__.__name__, stylesheet=css.rp_item.css + css.components.scroll)

        self.item = None
        self.category_id = None
        self.field_identifiers = []

    def init(self) -> 'RP_Item':
        self.setLayout(Layout.vertical(name='ItemLayout').init(
            spacing=20, margins=(0, 0, 0, 20),
            items=[
                Layout.horizontal().init(
                    margins=(20, 0, 20, 0),
                    items=[
                        FavouriteButton(self).init(
                            icon=Icons.STAR.adjusted(size=(30, 30))
                        ), Layout.Left,
                        Button(self, 'EditBtn').init(
                            icon=Icons.EDIT.adjusted(size=(30, 30)), slot=self.execute_edit
                        ),
                        Button(self, 'RemoveBtn', False).init(
                            icon=Icons.TRASH.adjusted(size=(30, 30)), slot=self.execute_edit
                        ),
                        Button(self, 'CloseBtn').init(
                            icon=Icons.CROSS.adjusted(size=(30, 30)), slot=ui.RightPages.shrink
                        ), Layout.Right
                    ]
                ),
                Layout.horizontal().init(
                    items=[
                        ImageButton(self).init(
                            icon=Icons.CATEGORY
                        ), Layout.TopCenter,
                        Layout.vertical().init(
                            items=[
                                LineInput(self, 'TitleInput').init(
                                    placeholder='title'
                                ), Layout.TopCenter,
                                TextInput(self, 'DescriptionInput').init(
                                    placeholder='description (optional)'
                                ), Layout.TopCenter
                            ]
                        )
                    ]
                ),
                Frame(self, 'AddBtnsFrame').init(
                    layout=Layout.horizontal().init(
                        items=[
                            Button(self, 'AddDocumentBtn').init(
                                text='Add document', icon=Icons.PLUS
                            ), Layout.HCenter,
                            Button(self, 'AddFieldBtn').init(
                                text='Add field', icon=Icons.PLUS, slot=self.add_field
                            ), Layout.HCenter
                        ]
                    )
                ),
                ScrollArea(self, 'FieldScrollArea').init(
                    orientation=Layout.Vertical, alignment=Layout.Top, margins=(5, 10, 5, 0), spacing=10
                ), Layout.HCenter,
                Spacer(False, True),
                Label(self, 'ErrorLbl').init(
                    wrap=True, alignment=Layout.Center
                ), Layout.Center,
                Button(self, 'CreateBtn').init(
                    text='Create item', slot=self.execute_create
                ), Layout.HCenter,
                Frame(self, 'SaveCancelFrame', False).init(
                    layout=Layout.horizontal().init(
                        spacing=50,
                        items=[
                            Button(self, 'SaveBtn').init(
                                text='Save', slot=self.execute_save
                            ), Layout.Left,
                            Button(self, 'CancelBtn').init(
                                text='Cancel', slot=self.execute_cancel
                            ), Layout.Right
                        ]
                    )
                ), Layout.HCenter
            ]
        ))
        return self

    @pyqtSlot()
    def add_field(self, field: dict[str, Any] = None):
        layout = self.FieldScrollArea.widget().layout()
        item_id, field = (self.item['id'], field) if field else (None, None)
        layout.addWidget(field := Field(self, item_id, field).init())
        self.field_identifiers.append(field.identifier)

    @pyqtSlot()
    def add_document(self):
        ...

    @pyqtSlot()
    def execute_edit(self):
        self.CreateBtn.setVisible(False)
        self.EditBtn.setVisible(False)
        self.RemoveBtn.setVisible(True)
        self.SaveCancelFrame.setVisible(True)
        self.TitleInput.setDisabled(False)
        self.DescriptionInput.setDisabled(False)
        self.ImageButton.setDisabled(False)
        self.AddFieldBtn.setVisible(False)
        self.AddDocumentBtn.setVisible(False)

    @pyqtSlot()
    def execute_save(self):
        icon = self.ImageButton.icon_bytes
        title = self.TitleInput.text()
        description = self.DescriptionInput.toPlainText()
        is_favourite = self.FavouriteBtn.is_favourite
        if not len(title):
            return self.ErrorLbl.setText('Title can not be empty')
        item = {'icon': icon, 'title': title, 'description': description, 'is_favourite': is_favourite}
        item = api.update_item(self.item['id'], item)
        if item.get('id', None):
            self.execute_cancel()
            self.item = item
        else:
            self.ErrorLbl.setText('Internal error, please try again')

    @pyqtSlot()
    def execute_cancel(self):
        self.ErrorLbl.setText('')
        self.EditBtn.setVisible(True)
        self.RemoveBtn.setVisible(False)
        self.SaveCancelFrame.setVisible(False)
        self.TitleInput.setDisabled(True)
        self.DescriptionInput.setDisabled(True)
        self.ImageButton.setDisabled(True)
        self.AddFieldBtn.setVisible(True)
        self.AddDocumentBtn.setVisible(True)

    def show_create(self):
        self.EditBtn.setVisible(False)

    def show_item(self, item: dict[str, Any]):
        if item_id := item.get('id', None):
            item = api.get_item(item_id)
        self.item = item
        if (not item['is_favourite'] and self.FavouriteBtn.is_favourite) or \
                item['is_favourite'] and not self.FavouriteBtn.is_favourite:
            self.FavouriteBtn.click()
        self.TitleInput.setText(item['title'])
        self.TitleInput.setEnabled(False)
        self.ImageButton.setIcon(Icons.from_bytes(item['icon']).icon)
        self.ImageButton.setDisabled(True)
        self.DescriptionInput.setText(item['description'])
        self.DescriptionInput.setDisabled(True)
        self.ErrorLbl.setText('')
        self.SaveCancelFrame.setVisible(False)

        self.FieldScrollArea.clear()
        for field in item['fields']:
            self.add_field(field)

        ui.RightPages.setCurrentWidget(ui.RP_Item)
        ui.RightPages.expand()

    @pyqtSlot()
    def execute_create(self):
        if not len(title := self.TitleInput.text()):
            return self.ErrorLbl.setText('Title can not be empty')
        fields = [self.findChild(QFrame, f'Field{identifier}') for identifier in self.field_identifiers]
        fields = [{'name': field.InputFieldName.text(), 'value': field.InputFieldValue.text()} for field in fields]
        item = {'icon': self.ImageButton.icon_bytes, 'title': title, 'description': self.DescriptionInput.toPlainText(),
                'is_favourite': self.FavouriteBtn.is_favourite}
        if (item := api.create_item(self.category_id, item, fields)).get('id'):
            self.ImageButton.setIcon(Icons.from_bytes(item['icon']).icon)
            self.show_item(item)
        else:
            self.ErrorLbl.setText('Internal error, please try again')
