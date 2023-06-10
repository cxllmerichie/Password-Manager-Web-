from aioqui.widgets import Button, Input, Layout, Frame, Parent
from aioqui.widgets.custom import Popup
from aioqui.asynq import asyncSlot
from aioqui.misc.fileops import explore_bytes
from uuid import uuid4
from typing import Any

from ..misc import ICONS, API
from .. import qss


class Attachment(Frame):
    def __init__(self, parent: Parent, attachment: dict[str, Any], creating: bool):
        self.identifier = str(uuid4())
        name = f'Attachment{self.identifier}'
        super().__init__(parent, name, qss=qss.item_attachment.attachment(name))

        self.creating = creating
        self.attachment = attachment
        API.attachment_identifiers.append(self.identifier)

    async def init(self) -> 'Attachment':
        self.setLayout(await Layout.horizontal().init(
            spacing=5,
            items=[
                await Input.line(self, f'FilenameInp').init(
                    text=self.attachment['filename'], alignment=Layout.Center
                ),
                await Button(self, 'ShowBtn').init(
                    icon=ICONS.EYE, on_click=self.execute_show
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
                        message=f'Delete attachment\n"{self.FilenameInp.text()}"?',
                        on_success=self.execute_delete
                    ).display
                ),
            ]
        ))
        await self.show_attachment()
        return self

    @asyncSlot()
    async def show_attachment(self):
        if not self.creating and API.item:  # add ui attachment to existing item
            self.FilenameInp.setText(self.attachment['filename'])
            self.FilenameInp.setDisabled(True)
            self.DeleteBtn.setVisible(False)
            self.SaveBtn.setVisible(False)
            self.EditBtn.setVisible(True)
            self.ShowBtn.setVisible(True)
            # self.AttachmentDownloadBtn.setVisible(True)
        elif API.item:  # creating attachment for existing item
            self.FilenameInp.setDisabled(False)
            self.DeleteBtn.setVisible(True)
            self.SaveBtn.setVisible(True)
            self.EditBtn.setVisible(False)
            self.ShowBtn.setVisible(False)
            # self.AttachmentDownloadBtn.setVisible(False)
        else:  # creating attachment while creating item
            self.FilenameInp.setDisabled(False)
            self.DeleteBtn.setVisible(True)
            self.EditBtn.setVisible(False)
            self.SaveBtn.setVisible(False)
            self.SaveBtn.setVisible(False)
            self.ShowBtn.setVisible(False)
            # self.AttachmentDownloadBtn.setVisible(False)

    @asyncSlot()
    async def execute_show(self):
        idx = self.attachment['filename'].rfind('.')
        filename, extension = self.attachment['filename'][0:idx], self.attachment['filename'][idx:]
        await explore_bytes(filename, extension, self.attachment['content'])

    @asyncSlot()
    async def execute_save(self):
        if not self.creating:
            self.attachment['filename'] = self.FilenameInp.text()
            response = await API.update_attachment(self.attachment['id'], self.attachment)
        else:
            response = await API.add_attachment(API.item['id'], self.attachment)
        if response.get('id'):
            self.attachment = response
            self.creating = False
            await self.show_attachment()
        else:
            if self.creating:
                self.setVisible(False)
                self.deleteLater()
            else:
                await self.show_attachment()

    @asyncSlot()
    async def execute_delete(self):
        def delete_ui_attachment():
            if self.identifier in API.attachment_identifiers:
                API.attachment_identifiers.remove(self.identifier)
            self.setVisible(False)
            self.deleteLater()
        if not self.creating:
            deleted_attachment = await API.delete_attachment(self.attachment['id'])
            if attachment_id := deleted_attachment.get('id'):
                delete_ui_attachment()
            else:
                self.RightPagesItem.ErrorLbl.setText('Internal error, please try again')
        if self.RightPagesItem.AttachmentScrollArea.widget().layout().count() == 2:  # one of them is `HintLbl3`, another `self`
            self.RightPagesItem.HintLbl3.setVisible(True)
        delete_ui_attachment()

    @asyncSlot()
    async def show_edit(self):
        self.SaveBtn.setVisible(True)
        self.DeleteBtn.setVisible(True)
        self.EditBtn.setVisible(False)
        self.ShowBtn.setVisible(False)
        # self.AttachmentDownloadBtn.setVisible(False)
        self.FilenameInp.setDisabled(False)
