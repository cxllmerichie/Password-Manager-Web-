from qcontextapi.widgets import Button, LineInput, Layout, Frame
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import pyqtSlot
from uuid import uuid4
from typing import Any

from ..misc import ICONS, API
from .. import css


class RightPagesItemField(Frame):
    def __init__(self, parent: QWidget, field: dict[str, Any]):
        self.identifier = str(uuid4())
        name = f'Field{self.identifier}'
        super().__init__(parent, name, stylesheet=css.right_pages_item_field.field(name))

        self.field = field

    def init(self) -> 'RightPagesItemField':
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
                self.RightPagesItem.ErrorLbl.setText('Internal error, please try again')
        if self.RightPagesItem.FieldScrollArea.widget().layout().count() == 2:  # one of them is `HintLbl2`, another `self`
            self.RightPagesItem.HintLbl2.setVisible(True)
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
