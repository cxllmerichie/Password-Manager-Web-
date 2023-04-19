from PyQt5.QtWidgets import QWidget, QFrame, QFileDialog
from PyQt5.QtCore import pyqtSlot
from uuid import uuid4
from typing import Any

from ..widgets import Button, LineInput, Layout, Label, TextInput, Spacer, Frame, ScrollArea
from ..misc import Icons, api, Colors
from .. import css


class Field(QFrame):
    def __init__(self, parent: QWidget, item_id: int, field: dict[str, Any] = None):
        super().__init__(parent)
        self.identifier = str(uuid4())
        self.item_id = item_id
        self.field = field

        self.setObjectName(f'Field{self.identifier}')
        self.setStyleSheet(css.item.field + f'''
            #Field{self.identifier} {{
                background-color: {Colors.GRAY};
                border-radius: 5px;
            }}
        ''')

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
                    icon=Icons.EDIT.adjusted(size=Icons.SAVE.size), slot=self.edit_field
                ),
                Button(self, f'SaveInputFieldBtn').init(
                    icon=Icons.SAVE, slot=self.save_field
                ),
                Button(self, f'RemoveInputFieldBtn').init(
                    icon=Icons.CROSS_CIRCLE, slot=self.remove_field
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
        return self

    @pyqtSlot()
    def save_field(self):
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
    def remove_field(self):
        self.setVisible(False)
        self.parent().parent().parent().parent().field_identifiers.remove(self.identifier)
        if self.field:
            api.remove_field(self.field['id'])

    @pyqtSlot()
    def edit_field(self):
        self.InputFieldValueCopyBtn.setVisible(False)
        self.InputFieldValueHideBtn.setVisible(False)
        self.SaveInputFieldBtn.setVisible(True)
        self.RemoveInputFieldBtn.setVisible(True)
        self.EditInputFieldBtn.setVisible(False)
        self.InputFieldName.setDisabled(False)
        self.InputFieldValue.setDisabled(False)
        self.InputFieldValue.show_echo()


class Item(Frame):
    def __init__(self, parent: QWidget):
        super().__init__(parent, self.__class__.__name__, stylesheet=css.rp_item.css + css.components.scroll)

        self.item = None
        self.category_id = None
        self.field_identifiers = []

    def init(self) -> 'Item':
        self.setLayout(Layout.vertical(name='ItemLayout').init(
            spacing=20, margins=(0, 0, 0, 20),
            items=[
                Layout.horizontal().init(
                    margins=(20, 0, 20, 0),
                    items=[
                        Button(self, 'FavouriteBtn').init(
                            icon=Icons.STAR.adjusted(size=(30, 30)), slot=self.set_favourite
                        ), Layout.Left,
                        Button(self, 'EditBtn').init(
                            icon=Icons.EDIT.adjusted(size=(30, 30)), slot=self.edit_item
                        ),
                        Button(self, 'RemoveBtn', False).init(
                            icon=Icons.TRASH.adjusted(size=(30, 30)), slot=self.edit_item
                        ),
                        Button(self, 'CloseBtn').init(
                            icon=Icons.CROSS.adjusted(size=(30, 30)), slot=self.close_page
                        ), Layout.Right
                    ]
                ),
                Layout.horizontal().init(
                    items=[
                        Button(self, 'IconBtn').init(
                            icon=Icons.CATEGORY, slot=self.set_icon
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
                    text='Create item', slot=self.create_item
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
                ), Layout.HCenter
            ]
        ))
        self.FavouriteBtn.setProperty('is_favourite', False)
        return self

    @pyqtSlot()
    def add_field(self, field: dict[str, Any] = None):
        layout = self.FieldScrollArea.widget().layout()
        layout.addWidget(f := Field(self, self.item['id'], field).init())
        self.field_identifiers.append(f.identifier)

    @pyqtSlot()
    def add_document(self):
        ...

    @pyqtSlot()
    def close_page(self):
        self.parent().shrink()

    @pyqtSlot()
    def edit_item(self):
        self.CreateBtn.setVisible(False)
        self.EditBtn.setVisible(False)
        self.RemoveBtn.setVisible(True)
        self.SaveCancelFrame.setVisible(True)
        self.TitleInput.setDisabled(False)
        self.DescriptionInput.setDisabled(False)
        self.IconBtn.setDisabled(False)
        self.AddFieldBtn.setVisible(False)
        self.AddDocumentBtn.setVisible(False)

    @pyqtSlot()
    def save(self):
        icon = self.IconBtn.property('icon_bytes')
        title = self.TitleInput.text()
        description = self.DescriptionInput.toPlainText()
        is_favourite = self.FavouriteBtn.property('is_favourite')
        if not len(title):
            return self.ErrorLbl.setText('Name can not be empty')
        item = {'icon': icon, 'title': title, 'description': description, 'is_favourite': is_favourite}
        item = api.update_item(self.item['id'], item)
        if item.get('id', None):
            self.cancel()
            self.item = item
        else:
            self.ErrorLbl.setText('Internal error, please try again')

    @pyqtSlot()
    def cancel(self):
        self.ErrorLbl.setText('')
        self.EditBtn.setVisible(True)
        self.RemoveBtn.setVisible(False)
        self.SaveCancelFrame.setVisible(False)
        self.TitleInput.setDisabled(True)
        self.DescriptionInput.setDisabled(True)
        self.IconBtn.setDisabled(True)
        self.AddFieldBtn.setVisible(True)
        self.AddDocumentBtn.setVisible(True)

    @pyqtSlot()
    def set_icon(self):
        dialog = QFileDialog()
        filepath, _ = dialog.getOpenFileName(None, 'Choose image', '', 'Images (*.jpg)', options=dialog.Options())
        if filepath:
            with open(filepath, 'rb') as file:
                icon_bytes = file.read()
                self.IconBtn.setProperty('icon_bytes', icon_bytes)
                self.IconBtn.setIcon(Icons.from_bytes(icon_bytes).icon)

    # def show_create_item(self):
    #     self.EditBtn.setVisible(False)
    #     print('callsed')

    def show_item(self, item: dict[str, Any]):
        if item_id := item.get('id', None):
            item = api.get_item(item_id)
        self.item = item
        if (not item['is_favourite'] and self.FavouriteBtn.property('is_favourite')) or \
                item['is_favourite'] and not self.FavouriteBtn.property('is_favourite'):
            self.FavouriteBtn.click()
        self.TitleInput.setText(item['title'])
        self.TitleInput.setEnabled(False)
        self.IconBtn.setIcon(Icons.from_bytes(item['icon']).icon)
        self.IconBtn.setDisabled(True)
        self.DescriptionInput.setText(item['description'])
        self.DescriptionInput.setDisabled(True)
        self.ErrorLbl.setText('')
        self.SaveCancelFrame.setVisible(False)

        self.FieldScrollArea.clear()
        for field in item['fields']:
            self.add_field(field)

    @pyqtSlot()
    def set_favourite(self):
        btn = self.FavouriteBtn
        is_favourite = btn.property('is_favourite')
        btn.setProperty('is_favourite', is_favourite := not is_favourite)
        if is_favourite:
            btn.setIcon(Icons.STAR_FILL.icon)
        else:
            btn.setIcon(Icons.STAR.icon)

    @pyqtSlot()
    def create_item(self):
        icon = self.IconBtn.property('icon_bytes')
        title = self.TitleInput.text()
        description = self.DescriptionInput.toPlainText()
        is_favourite = self.FavouriteBtn.property('is_favourite')
        if not len(title):
            return self.ErrorLbl.setText('Name can not be empty')

        fields = [self.findChild(QFrame, f'Field{identifier}') for identifier in self.field_identifiers]
        fields = [{
            'name': field.InputFieldName.text(),
            'value': field.InputFieldValue.text()
        } for field in fields]
        item = {'icon': icon, 'title': title, 'description': description, 'is_favourite': is_favourite}
        item = api.create_item(self.property('category_id'), item, fields)

        if item.get('id'):
            self.IconBtn.setIcon(Icons.from_bytes(item['icon']).icon)
            self.show_item(item)
        else:
            self.ErrorLbl.setText('Internal error, please try again')
