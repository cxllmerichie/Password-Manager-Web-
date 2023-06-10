from aioqui.widgets import Button, Input, Layout, Frame, Parent
from aioqui.widgets.custom import StateButton, Popup
from aioqui.asynq import asyncSlot
from PySide6.QtWidgets import QApplication
from uuid import uuid4
from typing import Any

from ..misc import ICONS, API
from .. import qss


class Field(Frame):
    def __init__(self, parent: Parent, field: dict[str, Any]):
        self.identifier = str(uuid4())
        name = f'Field{self.identifier}'
        super().__init__(parent, name, qss=qss.item_field.field(name))

        self.field = field
        API.field_identifiers.append(self.identifier)

    async def init(self) -> 'Field':
        self.setLayout(await Layout.horizontal().init(
            spacing=5,
            items=[
                await Input.line(self, f'NameInput').init(
                    placeholder='name', alignment=Layout.Right
                ),
                await Input.line(self, f'ValueInput').init(
                    placeholder='value'
                ),
                await StateButton(self, 'HideBtn').init(
                    icon_true=ICONS.EYE, icon_false=ICONS.EYE_OFF, pre_slot=self.hide_value
                ),
                await Button(self, 'CopyBtn').init(
                    icon=ICONS.COPY, on_click=self.clipboard
                ),
                await Button(self, f'EditBtn').init(
                    icon=ICONS.EDIT.adjusted(size=ICONS.SAVE.size), on_click=self.show_edit
                ),
                await Button(self, f'SaveBtn').init(
                    icon=ICONS.SAVE, on_click=self.execute_save
                ),
                await Button(self, f'DeleteBtn').init(
                    icon=ICONS.CROSS_CIRCLE, on_click=Popup(
                        self.core, qss=qss.components.popup,
                        message=f'Delete attachment\n"{self.NameInput.text()}"?',
                        on_success=self.execute_delete
                    ).display
                )
            ]
        ))
        await self.show_field()
        return self

    @asyncSlot()
    async def show_field(self):
        if self.field and API.item:  # add field to existing item
            self.HideBtn.setVisible(True)
            self.CopyBtn.setVisible(True)
            self.DeleteBtn.setVisible(False)
            self.NameInput.setText(self.field['name'])
            self.NameInput.setDisabled(True)
            self.ValueInput.setText(self.field['value'])
            self.ValueInput.hide_echo()
            self.ValueInput.setDisabled(True)
            self.SaveBtn.setVisible(False)
            self.EditBtn.setVisible(True)
        elif API.item:  # creating field for existing item
            self.DeleteBtn.setVisible(True)
            self.SaveBtn.setVisible(True)
            self.EditBtn.setVisible(False)
            self.CopyBtn.setVisible(False)
            self.HideBtn.setVisible(False)
        else:  # creating field while creating item
            self.EditBtn.setVisible(False)
            self.SaveBtn.setVisible(True)
            self.CopyBtn.setVisible(False)
            self.HideBtn.setVisible(False)
            self.SaveBtn.setVisible(False)

    @asyncSlot()
    async def hide_value(self):
        self.ValueInput.toggle_echo()
        return True

    @asyncSlot()
    async def clipboard(self):
        QApplication.clipboard().setText(self.ValueInput.text())

    @asyncSlot()
    async def execute_save(self):
        field = {'name': self.NameInput.text(), 'value': self.ValueInput.text()}
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
        self.CopyBtn.setVisible(False)
        self.HideBtn.setVisible(False)
        self.SaveBtn.setVisible(True)
        self.DeleteBtn.setVisible(True)
        self.EditBtn.setVisible(False)
        self.NameInput.setDisabled(False)
        self.ValueInput.setDisabled(False)
        self.ValueInput.show_echo()
