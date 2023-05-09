from qcontextapi.widgets import Button, LineInput, Layout, Frame, Popup
from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtCore import pyqtSlot, QUrl
from PyQt5.QtGui import QDesktopServices
from uuid import uuid4
from typing import Any
import tempfile

from ..misc import ICONS, API
from .. import stylesheets


class RightPagesItemAttachment(Frame):
    def __init__(self, parent: QWidget, attachment: dict[str, Any], creating: bool):
        self.identifier = str(uuid4())
        name = f'Attachment{self.identifier}'
        super().__init__(parent, name, stylesheet=stylesheets.right_pages_item_attachment.attachment(name))

        self.creating = creating
        self.attachment = attachment
        API.attachment_identifiers.append(self.identifier)

    def init(self) -> 'RightPagesItemAttachment':
        self.setLayout(Layout.horizontal().init(
            spacing=5,
            items=[
                LineInput(self, f'AttachmentFilenameInput').init(
                    text=self.attachment['filename'], alignment=Layout.Center
                ),
                Button(self, 'AttachmentShowBtn').init(
                    icon=ICONS.EYE, slot=self.execute_show
                ),
#                 # Button(self, 'AttachmentDownloadBtn').init(
                #     icon=ICONS.DOWNLOAD, slot=self.execute_download
                # ),
                Button(self, f'AttachmentEditBtn').init(
                    icon=ICONS.EDIT.adjusted(size=ICONS.SAVE.size), slot=self.show_edit
                ),
                Button(self, f'AttachmentSaveBtn').init(
                    icon=ICONS.SAVE, slot=self.execute_save
                ),
                Button(self, f'AttachmentDeleteBtn').init(
                    icon=ICONS.CROSS_CIRCLE,
                    slot=lambda: Popup(self.core, stylesheet=stylesheets.components.popup).init(
                        message=f'Delete attachment\n"{self.AttachmentFilenameInput.text()}"?',
                        on_success=self.execute_delete
                    )
                ),
            ]
        ))
        self.show_attachment()
        return self

    def show_attachment(self):
        if not self.creating and API.item:  # add ui attachment to existing item
            self.AttachmentFilenameInput.setText(self.attachment['filename'])
            self.AttachmentFilenameInput.setDisabled(True)
            self.AttachmentDeleteBtn.setVisible(False)
            self.AttachmentSaveBtn.setVisible(False)
            self.AttachmentEditBtn.setVisible(True)
            self.AttachmentShowBtn.setVisible(True)
            # self.AttachmentDownloadBtn.setVisible(True)
        elif API.item:  # creating attachment for existing item
            self.AttachmentFilenameInput.setDisabled(False)
            self.AttachmentDeleteBtn.setVisible(True)
            self.AttachmentSaveBtn.setVisible(True)
            self.AttachmentEditBtn.setVisible(False)
            self.AttachmentShowBtn.setVisible(False)
            # self.AttachmentDownloadBtn.setVisible(False)
        else:  # creating attachment while creating item
            self.AttachmentFilenameInput.setDisabled(False)
            self.AttachmentDeleteBtn.setVisible(True)
            self.AttachmentEditBtn.setVisible(False)
            self.AttachmentSaveBtn.setVisible(False)
            self.AttachmentSaveBtn.setVisible(False)
            self.AttachmentShowBtn.setVisible(False)
            # self.AttachmentDownloadBtn.setVisible(False)

    @pyqtSlot()
    def execute_download(self):
        filepath, _ = QFileDialog.getSaveFileName(self, 'Choose a file', '', 'Image (*.jpg);;Text file (*.txt)')
        if filepath:
            API.download_attachment(filepath)

    @pyqtSlot()
    def execute_show(self):
        idx = self.attachment['filename'].rfind('.')
        filename, extension = self.attachment['filename'][0:idx], self.attachment['filename'][idx:]
        temp_file = tempfile.NamedTemporaryFile(prefix=filename, suffix=extension, delete=False)
        temp_file.write(eval(self.attachment['content']))
        temp_file.close()
        QDesktopServices.openUrl(QUrl('file:///' + temp_file.name))

    @pyqtSlot()
    def execute_save(self):
        if not self.creating:
            self.attachment['filename'] = self.AttachmentFilenameInput.text()
            response = API.update_attachment(self.attachment['id'], self.attachment)
        else:
            response = API.add_attachment(API.item['id'], self.attachment)
        if response.get('id'):
            self.attachment = response
            self.creating = False
            self.show_attachment()
        else:
            if self.creating:
                self.setVisible(False)
                self.deleteLater()
            else:
                self.show_attachment()

    @pyqtSlot()
    def execute_delete(self):
        def delete_ui_attachment():
            if self.identifier in API.attachment_identifiers:
                API.attachment_identifiers.remove(self.identifier)
            self.setVisible(False)
            self.deleteLater()
        if not self.creating:
            deleted_attachment = API.delete_attachment(self.attachment['id'])
            if attachment_id := deleted_attachment.get('id'):
                delete_ui_attachment()
            else:
                self.RightPagesItem.ErrorLbl.setText('Internal error, please try again')
        if self.RightPagesItem.AttachmentScrollArea.widget().layout().count() == 2:  # one of them is `HintLbl3`, another `self`
            self.RightPagesItem.HintLbl3.setVisible(True)
        delete_ui_attachment()

    @pyqtSlot()
    def show_edit(self):
        self.AttachmentSaveBtn.setVisible(True)
        self.AttachmentDeleteBtn.setVisible(True)
        self.AttachmentEditBtn.setVisible(False)
        self.AttachmentShowBtn.setVisible(False)
        # self.AttachmentDownloadBtn.setVisible(False)
        self.AttachmentFilenameInput.setDisabled(False)
