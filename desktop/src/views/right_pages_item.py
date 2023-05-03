from qcontextapi.widgets import Button, LineInput, Layout, Label, TextInput, Frame, ScrollArea, Selector
from qcontextapi.customs import FavouriteButton, ImageButton, DateTimePicker, ErrorLabel
from qcontextapi.misc import Icon
from qcontextapi import CONTEXT
from PyQt5.QtWidgets import QWidget, QFrame, QFileDialog
from PyQt5.QtCore import pyqtSlot
from typing import Any

from ..misc import ICONS, API
from ..components import RightPagesItemField
from .. import css


class RightPagesItem(Frame):
    def __init__(self, parent: QWidget):
        super().__init__(parent, self.__class__.__name__,
                         stylesheet=css.right_pages_item.css +
                                    css.components.scroll +
                                    css.components.image_button +
                                    css.components.favourite_button +
                                    css.components.date_time_picker
                         )

    def init(self) -> 'RightPagesItem':
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
                Frame(self, 'CreatedFrame', False).init(
                    layout=Layout.horizontal().init(
                        items=[
                            Label(self, 'CreatedHintLbl').init(
                                text='Created:'
                            ),
                            Label(self, 'CreatedLbl')
                        ]
                    )
                ),
                Frame(self, 'ModifiedFrame', False).init(
                    layout=Layout.horizontal().init(
                        items=[
                            Label(self, 'ModifiedHintLbl').init(
                                text='Modified:'
                            ),
                            Label(self, 'ModifiedLbl')
                        ]
                    )
                ),
                Frame(self, 'ExpiresFrame', False).init(
                    layout=Layout.horizontal().init(
                        alignment=Layout.Top,
                        items=[
                            Label(self, 'ExpiresHintLbl').init(
                                text='Expires:'
                            ), Layout.Top,
                            Layout.vertical().init(
                                alignment=Layout.Top, spacing=5,
                                items=[
                                    Selector(self, 'ExpiresSelector').init(
                                        textchanged=lambda: self.DateTimePicker.setVisible(self.ExpiresSelector.currentText() == 'Yes'),
                                        items=[
                                            Selector.Item(text='No'),
                                            Selector.Item(text='Yes'),
                                        ]
                                    ),
                                    Label(self, 'ExpiresLbl'),
                                    DateTimePicker(self, visible=False).init(
                                        spacing=5
                                    )
                                ]
                            )
                        ]
                    )
                ),
                TextInput(self, 'DescriptionInput').init(
                    placeholder='description (optional)'
                ), Layout.Top,
                Frame(self, 'AddBtnsFrame').init(
                    layout=Layout.horizontal().init(
                        items=[
                            Button(self, 'AddDocumentBtn').init(
                                text='Add document', icon=ICONS.PLUS, slot=self.add_document
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
                ErrorLabel(self, 'ErrorLbl').init(
                    wrap=True, alignment=Layout.Center
                ), Layout.Center,
                Button(self, 'ExportBtn', False).init(
                    text='Export to file', icon=ICONS.EXPORT, slot=self.export_item
                ),
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
    def export_item(self):
        filepath, _ = QFileDialog.getSaveFileName(self, 'Choose a file to export', '', 'JSON Files (*.json)')
        if filepath:
            API.export_item(filepath)

    @pyqtSlot()
    def add_field(self, field: dict[str, Any] = None):
        if self.HintLbl2.isVisible():
            self.HintLbl2.setVisible(False)
        layout = self.FieldScrollArea.widget().layout()
        layout.addWidget(RightPagesItemField(self, field).init())

    @pyqtSlot()
    def add_document(self):
        filepath, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'All files (*.txt, *.jpg)')
        if filepath:
            API.add_attachment(filepath)

    @pyqtSlot()
    def execute_edit(self):
        self.ExportBtn.setVisible(False)
        self.CreatedFrame.setVisible(False)
        self.ModifiedFrame.setVisible(False)
        self.ExpiresFrame.setVisible(True)
        self.ExpiresLbl.setVisible(False)
        self.ExpiresSelector.setVisible(True)
        if expires_at := API.item['expires_at']:
            self.DateTimePicker.set_datetime(expires_at)
            self.DateTimePicker.setVisible(True)
            self.ExpiresSelector.setCurrentText('Yes')
        else:
            self.ExpiresSelector.setCurrentText('No')
            self.DateTimePicker.setVisible(False)
            self.DateTimePicker.set_datetime(DateTimePicker.now)
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
        updated = API.set_item_favourite(API.item['id'], self.FavouriteButton.is_favourite).get('id')
        if updated:
            CONTEXT.LeftMenu.refresh_categories()
            CONTEXT.CentralItems.refresh_items()
            return True
        self.ErrorLbl.setText('Internal error, please try again')
        return False

    @pyqtSlot()
    def execute_save(self):
        title = self.TitleInput.text()
        if not len(title):
            return self.ErrorLbl.setText('Title can not be empty')
        expires_at = None
        if self.ExpiresSelector.currentText() == 'Yes':
            expires_at = str(self.DateTimePicker.get_datetime(tz=True))
        updated = API.update_item(API.item['id'], {
            'icon': self.ImageButton.image_bytes_str, 'title': title, 'description': self.DescriptionInput.toPlainText(),
            'is_favourite': self.FavouriteButton.is_favourite, 'expires_at': expires_at
        }).get('id')
        if updated:
            self.execute_cancel()
            CONTEXT.LeftMenu.refresh_categories()
            CONTEXT.CentralItems.refresh_items()
            self.show_item(API.item)
        else:
            self.ErrorLbl.setText('Internal error, please try again')

    @pyqtSlot()
    def execute_cancel(self):
        self.ExportBtn.setVisible(True)
        self.ModifiedFrame.setVisible(API.item and API.item['modified_at'])
        self.ExpiresFrame.setVisible(API.item and API.item['expires_at'])
        self.CreatedFrame.setVisible(True)
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

        self.ExportBtn.setVisible(False)
        self.CreatedFrame.setVisible(False)
        self.ModifiedFrame.setVisible(False)
        self.ExpiresFrame.setVisible(True)
        self.DeleteBtn.setVisible(False)
        self.ImageButton.setIcon(ICONS.ITEM.icon)
        self.ImageButton.image_bytes = None
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

        self.ExportBtn.setVisible(True)

        self.CreatedFrame.setVisible(True)
        created_at = DateTimePicker.parse(item['created_at']).strftime(DateTimePicker.default_format)
        self.CreatedLbl.setText(created_at)

        if modified_at := item['modified_at']:
            modified_at = DateTimePicker.parse(modified_at).strftime(DateTimePicker.default_format)
            self.ModifiedLbl.setText(modified_at)
        self.ModifiedFrame.setVisible(modified_at is not None)

        if expires_at := item['expires_at']:
            expires_at = DateTimePicker.parse(expires_at).strftime(DateTimePicker.default_format)
            self.ExpiresLbl.setText(expires_at)
            self.ExpiresLbl.setVisible(True)
            self.ExpiresSelector.setVisible(False)
            self.DateTimePicker.setVisible(False)
            self.DateTimePicker.set_datetime(expires_at)
        else:
            self.ExpiresSelector.setCurrentText('No')
        self.ExpiresFrame.setVisible(expires_at is not None)

        self.FavouriteButton.set(API.item['is_favourite'])
        self.TitleInput.setText(API.item['title'])
        self.TitleInput.setEnabled(False)
        self.ImageButton.setIcon(Icon(API.item['icon']).icon)
        self.ImageButton.setDisabled(True)
        self.DescriptionInput.setText(API.item['description'])
        self.DescriptionInput.setDisabled(True)
        self.ErrorLbl.setText('')
        self.SaveCancelFrame.setVisible(False)
        self.DeleteBtn.setVisible(False)
        self.EditBtn.setVisible(True)
        self.CreateBtn.setVisible(False)

        self.FieldScrollArea.clear([self.HintLbl2])
        for field in API.item['fields']:
            self.add_field(field)
        self.HintLbl2.setVisible(not len(API.item['fields']))

        CONTEXT.RightPages.setCurrentWidget(CONTEXT.RightPagesItem)
        CONTEXT.RightPages.expand()

    @pyqtSlot()
    def execute_create(self):
        if not len(title := self.TitleInput.text()):
            return self.ErrorLbl.setText('Title can not be empty')
        created_item = API.create_item(API.category['id'], {
            'icon': self.ImageButton.image_bytes_str, 'description': self.DescriptionInput.toPlainText(),
            'title': title, 'is_favourite': self.FavouriteButton.is_favourite
        })
        if item_id := created_item.get('id'):
            for identifier in API.field_identifiers:
                field = self.findChild(QFrame, f'Field{identifier}')
                API.add_field(item_id, {'name': field.FieldNameInput.text(), 'value': field.FieldValueInput.text()})
            self.ImageButton.setIcon(Icon(API.item['icon']).icon)
            self.CreateBtn.setVisible(False)
            CONTEXT.LeftMenu.refresh_categories()
            CONTEXT.CentralItems.refresh_items()
            self.show_item(API.item)
        else:
            self.ErrorLbl.setText('Internal error, please try again')

    @pyqtSlot()
    def execute_delete(self):
        deleted_item = API.delete_item(API.item['id'])
        if item_id := deleted_item.get('id'):
            self.execute_cancel()
            self.show_create()
            CONTEXT.LeftMenu.refresh_categories()
            CONTEXT.CentralItems.refresh_items()
            self.show_create()
        else:
            self.ErrorLbl.setText('Internal error, please try again')
