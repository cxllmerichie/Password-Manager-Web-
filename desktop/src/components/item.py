from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QFrame, QPushButton, QFileDialog, QVBoxLayout, QScrollArea
)
from PyQt5.QtCore import pyqtSlot
from uuid import uuid4
from typing import Any

from ..widgets import Button, VLayout, LInput, HLayout, Label, TInput, Spacer, Frame, ScrollArea
from ..misc import Icons, api, Colors
from ..css import item, components


class Field(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.identifier = str(uuid4())
        self.setObjectName(f'Field{self.identifier}')
        self.setStyleSheet(item.field + f'''
            #Field{self.identifier} {{
                background-color: {Colors.GRAY};
                border-radius: 5px;
            }}
        ''')

    def init(self, field: dict[str, Any]) -> 'Field':
        layout = HLayout(self, f'FieldLayout').init(spacing=5)
        layout.addWidget(name_input := LInput(self, f'InputFieldName').init(
            placeholder='name', alignment=VLayout.Right
        ))
        layout.addWidget(value_input := LInput(self, f'InputFieldValue').init(
            placeholder='value'
        ))
        layout.addWidget(value_input_hide_btn := Button(self, 'InputFieldValueHideBtn').init(
            icon=Icons.EYE, slot=lambda: value_input.toggle_echo()
        ))
        layout.addWidget(value_input_copy_btn := Button(self, 'InputFieldValueCopyBtn').init(
            icon=Icons.COPY
        ))
        layout.addWidget(edit_field_btn := Button(self, f'EditInputFieldBtn').init(
            icon=Icons.EDIT.adjusted(size=Icons.SAVE.size), slot=self.edit_field
        ))
        layout.addWidget(save_field_btn := Button(self, f'SaveInputFieldBtn').init(
            icon=Icons.SAVE, slot=self.save_field
        ))
        layout.addWidget(remove_field_btn := Button(self, f'RemoveInputFieldBtn').init(
            icon=Icons.CROSS_CIRCLE, slot=self.remove_field
        ))
        self.setLayout(layout)

        remove_field_btn.setVisible(False)
        if field:
            name_input.setText(field['name'])
            value_input.setText(field['value'])
            save_field_btn.setVisible(False)
            edit_field_btn.setVisible(True)
            value_input.hide_echo()
            name_input.setDisabled(True)
            value_input.setDisabled(True)
        else:
            edit_field_btn.setVisible(False)
            save_field_btn.setVisible(True)
            value_input_copy_btn.setVisible(False)
            value_input_hide_btn.setVisible(False)
        return self

    def save_field(self):
        name_input = self.findChild(QLineEdit, f'InputFieldName')
        value_input = self.findChild(QLineEdit, f'InputFieldValue')
        print(name_input, value_input)
        response = api.add_field(
            self.property('item')['id'], {'name': name_input.text(), 'value': value_input.text()}, self.app().token()
        )
        # if ok
        self.findChild(QPushButton, 'InputFieldValueCopyBtn').setVisible(True)
        self.findChild(QPushButton, 'InputFieldValueHideBtn').setVisible(True)
        self.findChild(QPushButton, 'SaveInputFieldBtn').setVisible(False)
        self.findChild(QPushButton, 'EditInputFieldBtn').setVisible(True)
        self.findChild(QPushButton, 'RemoveInputFieldBtn').setVisible(False)
        value_input.hide_echo()
        value_input.setDisabled(True)
        name_input.setDisabled(True)

    def remove_field(self):
        self.setVisible(False)
        self.parent().items.remove(self.identifier)

    def edit_field(self):
        self.findChild(QPushButton, 'InputFieldValueCopyBtn').setVisible(False)
        self.findChild(QPushButton, 'InputFieldValueHideBtn').setVisible(False)
        self.findChild(QPushButton, 'SaveInputFieldBtn').setVisible(True)
        self.findChild(QPushButton, 'RemoveInputFieldBtn').setVisible(True)
        self.findChild(QPushButton, 'EditInputFieldBtn').setVisible(False)
        self.findChild(QLineEdit, f'InputFieldName').setDisabled(False)
        value_input = self.findChild(QLineEdit, f'InputFieldValue')
        value_input.setDisabled(False)
        value_input.show_echo()

    def app(self):
        return self.parent().app()


class Item(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(item.css + components.scroll)

        self.field_identifiers = []

    def init(self) -> 'Item':
        vbox = VLayout(name='ItemLayout').init(spacing=20, margins=(0, 0, 0, 20))

        hbox = HLayout().init(margins=(20, 0, 20, 0))
        hbox.addWidget(favourite_btn := Button(self, 'FavouriteBtn').init(
            icon=Icons.STAR.adjusted(size=(30, 30)), slot=self.set_favourite
        ), alignment=VLayout.Left)
        hbox.addWidget(edit_btn := Button(self, 'EditBtn').init(
            icon=Icons.EDIT.adjusted(size=(30, 30)), slot=self.edit_item
        ))
        hbox.addWidget(Button(self, 'CloseBtn').init(
            icon=Icons.CROSS.adjusted(size=(30, 30)), slot=self.close_page
        ), alignment=VLayout.Right)
        vbox.addLayout(hbox)

        hbox = HLayout().init()
        hbox.addWidget(Button(self, 'IconBtn').init(
            icon=Icons.CATEGORY, slot=self.set_icon
        ), alignment=VLayout.HCenterTop)
        title_description_layout = VLayout().init()
        title_description_layout.addWidget(LInput(self, 'TitleInput').init(
            placeholder='title'
        ), alignment=VLayout.HCenterTop)
        title_description_layout.addWidget(TInput(self, 'DescriptionInput').init(
            placeholder='description (optional)'
        ), alignment=VLayout.HCenterTop)
        hbox.addLayout(title_description_layout)
        vbox.addLayout(hbox)

        add_btns_layout = HLayout().init()
        add_btns_layout.addWidget(Button(self, 'AddDocumentBtn').init(
            text='Add document', icon=Icons.PLUS
        ), alignment=VLayout.HCenter)
        add_btns_layout.addWidget(Button(self, 'AddFieldBtn').init(
            text='Add field', icon=Icons.PLUS, slot=self.add_field
        ), alignment=VLayout.HCenter)
        vbox.addWidget(Frame(self, 'AddBtnsFrame').init(
            layout=add_btns_layout
        ))

        vbox.addWidget(ScrollArea(self, 'FieldScrollArea').init(
            layout_t=VLayout, alignment=VLayout.Top, margins=(5, 10, 5, 0), spacing=10
        ), alignment=VLayout.HCenter)
        vbox.addItem(Spacer(False, True))

        vbox.addWidget(Label(self, 'ErrorLbl').init(
            wrap=True, alignment=VLayout.CenterCenter
        ), alignment=VLayout.CenterCenter)
        vbox.addWidget(Button(self, 'CreateBtn').init(
            text='Create item', slot=self.create_item
        ), alignment=VLayout.HCenter)

        frame = Frame(self, 'SaveCancelFrame').init()
        save_cancel_layout = HLayout(frame).init(spacing=50)
        save_cancel_layout.addWidget(Button(self, 'SaveBtn').init(
            text='Save'
        ), alignment=VLayout.Left)
        save_cancel_layout.addWidget(Button(self, 'CancelBtn').init(
            text='Cancel'
        ), alignment=VLayout.Right)
        vbox.addWidget(frame, alignment=VLayout.HCenter)
        self.setLayout(vbox)

        edit_btn.setVisible(False)
        frame.setVisible(False)
        favourite_btn.setProperty('is_favourite', False)
        return self

    @pyqtSlot()
    def show_create_item(self):
        return

    @pyqtSlot()
    def add_field(self, field: dict[str, Any] = None):
        layout = self.findChild(QScrollArea, 'FieldScrollArea').widget().layout()
        layout.addWidget(f := Field(self).init(field))
        self.field_identifiers.append(f.identifier)

    @pyqtSlot()
    def add_document(self):
        ...

    @pyqtSlot()
    def close_page(self):
        self.parent().shrink()

    @pyqtSlot()
    def edit_item(self):
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
            self.setProperty('category', response)
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
    def set_icon(self):
        dialog = QFileDialog()
        filepath, _ = dialog.getOpenFileName(None, 'Choose image', '', 'Images (*.jpg)', options=dialog.Options())
        if filepath:
            with open(filepath, 'rb') as file:
                icon_bytes = file.read()
                btn = self.findChild(QPushButton, 'IconBtn')
                btn.setProperty('icon_bytes', icon_bytes)
                btn.setIcon(Icons.from_bytes(icon_bytes).icon)

    def show_item(self, item_: dict[str, Any]):
        self.setProperty('item', item_)
        title_input = self.findChild(QLineEdit, 'TitleInput')
        description_input = self.findChild(QTextEdit, 'DescriptionInput')
        icon_btn = self.findChild(QPushButton, 'IconBtn')

        title_input.setText(item_['title'])
        description_input.setText(item_['description'])
        icon_btn.setIcon(Icons.from_bytes(item_['icon']).icon)
        favourite_btn = self.findChild(QPushButton, 'FavouriteBtn')
        if (not item_['is_favourite'] and favourite_btn.property('is_favourite')) or \
                item_['is_favourite'] and not favourite_btn.property('is_favourite'):
            favourite_btn.click()
        title_input.setEnabled(False)
        icon_btn.setDisabled(True)
        description_input.setDisabled(True)
        self.findChild(QLabel, 'ErrorLbl').setText('')
        self.findChild(QFrame, 'SaveCancelFrame').setVisible(False)

        self.findChild(QScrollArea, 'FieldScrollArea').clear()
        for field in item_['fields']:
            self.add_field(field)

    @pyqtSlot()
    def set_favourite(self):
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
    def create_item(self):
        icon_btn = self.findChild(QPushButton, 'IconBtn')
        title_input = self.findChild(QLineEdit, 'TitleInput')
        description_input = self.findChild(QTextEdit, 'DescriptionInput')
        error_lbl = self.findChild(QLabel, 'ErrorLbl')

        icon = icon_btn.property('icon_bytes')
        title = title_input.text()
        description = description_input.toPlainText()
        is_favourite = self.findChild(QPushButton, 'FavouriteBtn').property('is_favourite')
        if not len(title):
            return error_lbl.setText('Name can not be empty')

        fields = [self.findChild(QFrame, f'Field{identifier}') for identifier in self.field_identifiers]
        fields = [{
            'name': field.findChild(QLineEdit, 'InputFieldName').text(),
            'value': field.findChild(QLineEdit, 'InputFieldValue').text()
        } for field in fields]
        body = {'icon': icon, 'title': title, 'description': description, 'is_favourite': is_favourite}
        response = api.create_item(self.property('category_id'), body, fields, self.app().token())

        if response.get('id', None):
            icon_btn.setIcon(Icons.from_bytes(response['icon']).icon)
            self.show_item(response)
        else:
            error_lbl.setText('Internal error, please try again')
