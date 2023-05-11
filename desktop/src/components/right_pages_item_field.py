from qcontext.widgets import Button, LineInput, Layout, Frame, Popup
from qcontext.widgets.custom import FavouriteButton
from qcontext.qasyncio import asyncSlot
from PyQt5.QtWidgets import QWidget, QApplication
from uuid import uuid4
from typing import Any

from ..misc import ICONS, API
from .. import stylesheets


class RightPagesItemField(Frame):
    def __init__(self, parent: QWidget, field: dict[str, Any]):
        self.identifier = str(uuid4())
        name = f'Field{self.identifier}'
        super().__init__(parent, name, stylesheet=stylesheets.right_pages_item_field.field(name))

        self.field = field
        API.field_identifiers.append(self.identifier)

    async def init(self) -> 'RightPagesItemField':
        self.setLayout(await Layout.horizontal().init(
            spacing=5,
            items=[
                await LineInput(self, f'FieldNameInput').init(
                    placeholder='name', alignment=Layout.Right
                ),
                await LineInput(self, f'FieldValueInput').init(
                    placeholder='value'
                ),
                await FavouriteButton(self, 'FieldHideBtn').init(
                    if_set_icon=ICONS.EYE, if_unset_icon=ICONS.EYE_OFF, pre_slot=self.hide_value
                ),
                await Button(self, 'FieldCopyBtn').init(
                    icon=ICONS.COPY, slot=lambda: QApplication.clipboard().setText(self.FieldValueInput.text())
                ),
                await Button(self, f'FieldEditBtn').init(
                    icon=ICONS.EDIT.adjusted(size=ICONS.SAVE.size), slot=self.show_edit
                ),
                await Button(self, f'FieldSaveBtn').init(
                    icon=ICONS.SAVE, slot=self.execute_save
                ),
                await Button(self, f'FieldDeleteBtn').init(
                    icon=ICONS.CROSS_CIRCLE,
                    slot=lambda: Popup(self.core, stylesheet=stylesheets.components.popup).display(
                        message=f'Delete attachment\n"{self.FieldNameInput.text()}"?',
                        on_success=self.execute_delete
                    )
                )
            ]
        ))
        await self.show_field()
        return self

    @asyncSlot()
    async def show_field(self):
        if self.field and API.item:  # add field to existing item
            self.FieldHideBtn.setVisible(True)
            self.FieldCopyBtn.setVisible(True)
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

    @asyncSlot()
    async def hide_value(self):
        self.FieldValueInput.toggle_echo()
        return True

    @asyncSlot()
    async def execute_save(self):
        field = {'name': self.FieldNameInput.text(), 'value': self.FieldValueInput.text()}
        if self.field:
            response = await API.update_field(self.field['id'], field)
        else:
            response = await API.add_field(API.item['id'], field)
        if response.get('id'):
            self.field = response
            await self.show_field()
        else:
            if not self.field:
                self.setVisible(False)
                self.deleteLater()
            else:
                await self.show_field()

    @asyncSlot()
    async def execute_delete(self):
        def delete_ui_field():
            if self.identifier in API.field_identifiers:
                API.field_identifiers.remove(self.identifier)
            self.setVisible(False)
            self.deleteLater()
        if self.field:
            deleted_field = await API.delete_field(self.field['id'])
            if field_id := deleted_field.get('id'):
                delete_ui_field()
            else:
                self.RightPagesItem.ErrorLbl.setText('Internal error, please try again')
        if self.RightPagesItem.FieldScrollArea.widget().layout().count() == 2:  # one of them is `HintLbl2`, another `self`
            self.RightPagesItem.HintLbl2.setVisible(True)
        delete_ui_field()

    @asyncSlot()
    async def show_edit(self):
        self.FieldCopyBtn.setVisible(False)
        self.FieldHideBtn.setVisible(False)
        self.FieldSaveBtn.setVisible(True)
        self.FieldDeleteBtn.setVisible(True)
        self.FieldEditBtn.setVisible(False)
        self.FieldNameInput.setDisabled(False)
        self.FieldValueInput.setDisabled(False)
        self.FieldValueInput.show_echo()
