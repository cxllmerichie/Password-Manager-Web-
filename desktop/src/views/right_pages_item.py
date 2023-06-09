from aioqui.widgets import Button, Input, Layout, Label, Frame, ScrollArea, Selector, Parent, DateTime
from aioqui.widgets.custom import StateButton, ImageButton, DurationLabel, Popup
from aioqui.misc.fileops import select_file, select_dir, explore_dir
from aioqui.asynq import asyncSlot
from aioqui.types import Icon
from aioqui import CONTEXT
from PySide6.QtWidgets import QFrame
from typing import Any
from datetime import datetime

from ..misc import ICONS, API, PATHS, SIZES
from ..components import RightPagesItemField, RightPagesItemAttachment
from .. import qss


class RightPagesItem(Frame):
    def __init__(self, parent: Parent):
        super().__init__(parent, self.__class__.__name__, qss=(
            qss.right_pages_item.css,
            qss.components.scroll,
            qss.components.image_button(),
            qss.components.favourite_button,
            qss.components.date_time_picker
        ))

    async def init(self) -> 'RightPagesItem':
        self.setLayout(await Layout.vertical().init(
            spacing=20, margins=(25, 10, 25, 20),
            items=[
                await Layout.horizontal().init(
                    margins=(0, 0, 0, 20),
                    items=[
                        await StateButton(self, 'FavouriteButton').init(
                            pre_slot=self.toggle_favourite, fix_size=SIZES.CONTROL
                        ), Layout.Left,
                        await Button(self, 'EditBtn').init(
                            icon=ICONS.EDIT.adjusted(size=(30, 30)), on_click=self.execute_edit, fix_size=SIZES.CONTROL
                        ),
                        await Button(self, 'DeleteBtn', False).init(
                            icon=ICONS.TRASH.adjusted(size=(30, 30)), fix_size=SIZES.CONTROL,
                            on_click=lambda: Popup(
                                self.core, qss=qss.components.popup,
                                message=f'Delete item\n\'{API.item["title"]}\'?', on_success=self.execute_delete
                            ).display()
                        ),
                        await Button(self, 'CloseBtn').init(
                            icon=ICONS.CROSS.adjusted(size=(30, 30)), fix_size=SIZES.CONTROL,
                            on_click=CONTEXT.RightPages.shrink
                        ), Layout.Right
                    ]
                ),
                await ImageButton(self).init(
                    icon=ICONS.ITEM, directory=PATHS.ICONS
                ), Layout.TopCenter,
                await Input.line(self, 'TitleInput').init(
                    placeholder='title'
                ), Layout.Top,
                await Frame(self, 'CreatedFrame', False).init(
                    layout=await Layout.horizontal().init(
                        items=[
                            await Label(self, 'CreatedHintLbl').init(
                                text='Created:'
                            ),
                            await Label(self, 'CreatedLbl').init(

                            )
                        ]
                    )
                ),
                await Frame(self, 'ModifiedFrame', False).init(
                    layout=await Layout.horizontal().init(
                        items=[
                            await Label(self, 'ModifiedHintLbl').init(
                                text='Modified:'
                            ),
                            await Label(self, 'ModifiedLbl').init(

                            )
                        ]
                    )
                ),
                await Frame(self, 'ExpiresFrame', False).init(
                    layout=await Layout.horizontal().init(
                        alignment=Layout.Top,
                        items=[
                            await Label(self, 'ExpiresHintLbl').init(
                                text='Expires:'
                            ), Layout.Top,
                            await Layout.vertical().init(
                                alignment=Layout.Top, spacing=5,
                                items=[
                                    await Selector(self, 'ExpiresSelector').init(
                                        on_change=lambda: self.DateTimePicker.setVisible(self.ExpiresSelector.currentText() == 'Yes'),
                                        items=[
                                            Selector.Item(text='No'),
                                            Selector.Item(text='Yes'),
                                        ]
                                    ),
                                    await Label(self, 'ExpiresLbl').init(

                                    ),
                                    await DateTime(self, 'DateTimePicker', False).init(

                                    )
                                ]
                            )
                        ]
                    )
                ),
                await Input.reach(self, 'DescriptionInput').init(
                    placeholder='description (optional)'
                ), Layout.Top,
                await Frame(self, 'FieldFrame').init(
                    layout=await Layout.vertical().init(
                        items=[
                            await ScrollArea(self, 'FieldScrollArea').init(
                                orientation=Layout.Vertical, alignment=Layout.Top, margins=(5, 10, 5, 0), spacing=10,
                                items=[
                                    await Label(self, 'HintLbl2').init(
                                        wrap=True, text='Add new field with name "password" or "username" and it\'s value'
                                    ), Layout.Center
                                ]
                            ),
                            await Button(self, 'AddFieldBtn').init(
                                text='Add field', icon=ICONS.PLUS, on_click=self.add_field
                            )
                        ]
                    )
                ),
                await Frame(self, 'AttachmentFrame').init(
                    layout=await Layout.vertical().init(
                        items=[
                            await ScrollArea(self, 'AttachmentScrollArea').init(
                                orientation=Layout.Vertical, alignment=Layout.Top, margins=(5, 10, 5, 0), spacing=10,
                                items=[
                                    await Label(self, 'HintLbl3').init(
                                        wrap=True, text='Attach *.txt or *.jpg files to the item'
                                    ), Layout.Center
                                ]
                            ),
                            await Button(self, 'AddAttachmentBtn').init(
                                text='Add document', icon=ICONS.PLUS, on_click=self.add_attachment
                            )
                        ]
                    )
                ),
                await DurationLabel(self, 'ErrorLbl').init(
                    wrap=True, alignment=Layout.Center
                ), Layout.Center,
                await Button(self, 'ExportBtn', False).init(
                    text='Export item', icon=ICONS.EXPORT, on_click=self.export_item
                ),
                await Button(self, 'CreateBtn').init(
                    text='Create', on_click=self.execute_create
                ),
                await Frame(self, 'SaveCancelFrame', False).init(
                    layout=await Layout.horizontal().init(
                        spacing=20,
                        items=[
                            await Button(self, 'SaveBtn').init(
                                text='Save', on_click=self.execute_save
                            ),
                            await Button(self, 'CancelBtn').init(
                                text='Cancel', on_click=self.execute_cancel
                            )
                        ]
                    )
                )
            ]
        ))
        return self

    @asyncSlot()
    async def export_item(self):
        if directory := await select_dir(self, 'Select', '.'):
            await explore_dir(await API.export_item(directory))

    @asyncSlot()
    async def add_field(self, field: dict[str, Any] = None):
        self.HintLbl2.setVisible(False)
        layout = self.FieldScrollArea.widget().layout()
        layout.addWidget(await RightPagesItemField(self, field).init())

    @asyncSlot()
    async def add_attachment(self, attachment: dict[str, Any] = None):
        creating = attachment is None
        if not attachment:
            if filepath := await select_file(self, filters='Images (*.jpg);;Documents (*.txt)'):
                attachment = await API.get_attachment_data(filepath)
        if attachment:
            self.HintLbl3.setVisible(False)
            layout = self.AttachmentScrollArea.widget().layout()
            layout.addWidget(await RightPagesItemAttachment(self, attachment, creating).init())

    @asyncSlot()
    async def execute_edit(self):
        self.ExportBtn.setVisible(False)
        self.CreatedFrame.setVisible(False)
        self.ModifiedFrame.setVisible(False)
        self.ExpiresFrame.setVisible(True)
        self.ExpiresLbl.setVisible(False)
        self.ExpiresSelector.setVisible(True)
        if expires_at := API.item['expires_at']:
            self.DateTimePicker.setDateTime(expires_at)
            self.DateTimePicker.setVisible(True)
            self.ExpiresSelector.setCurrentText('Yes')
        else:
            self.ExpiresSelector.setCurrentText('No')
            self.DateTimePicker.setVisible(False)
            self.DateTimePicker.setDateTime(datetime.now())
        self.CreateBtn.setVisible(False)
        self.EditBtn.setVisible(False)
        self.DeleteBtn.setVisible(True)
        self.SaveCancelFrame.setVisible(True)
        self.TitleInput.setDisabled(False)
        self.DescriptionInput.setDisabled(False)
        self.DescriptionInput.setVisible(True)
        self.ImageButton.setDisabled(False)
        self.AddFieldBtn.setVisible(False)
        self.AddAttachmentBtn.setVisible(False)
        self.FieldScrollArea.setVisible(False)
        self.AttachmentScrollArea.setVisible(False)

    @asyncSlot()
    async def toggle_favourite(self) -> bool:
        if not API.item:
            return True
        updated_category = await API.set_item_favourite(API.item['id'], self.FavouriteButton.state)
        if category_id := updated_category.get('id'):
            await CONTEXT.LeftMenu.refresh_categories()
            await CONTEXT.CentralItems.refresh_items()
            return True
        self.ErrorLbl.setText('Internal error, please try again')
        return False

    @asyncSlot()
    async def execute_save(self):
        title = self.TitleInput.text()
        if not len(title):
            return self.ErrorLbl.setText('Title can not be empty')
        expires_at = None
        if self.ExpiresSelector.currentText() == 'Yes':
            expires_at = str(self.DateTimePicker.dateTime())
        prev_icon = API.item['icon']
        updated_category = await API.update_item(API.item['id'], {
            'icon': self.ImageButton.bytes, 'title': title, 'description': self.DescriptionInput.toPlainText(),
            'is_favourite': self.FavouriteButton.state, 'expires_at': expires_at
        })
        if category_id := updated_category.get('id'):
            await CONTEXT.LeftMenu.refresh_categories()
            await CONTEXT.CentralItems.refresh_items()
            await self.execute_cancel()
            await self.show_item(API.item)
            if prev_icon != (curr_icon := API.item['icon']):
                await API.save_icon(curr_icon)
        else:
            self.ErrorLbl.setText('Internal error, please try again')

    @asyncSlot()
    async def execute_cancel(self):
        self.ExportBtn.setVisible(True)
        self.ModifiedFrame.setVisible(bool(API.item and API.item['modified_at']))
        if API.item and API.item['expires_at']:
            self.ExpiresFrame.setVisible(True)
            self.ExpiresSelector.setVisible(False)
            self.DateTimePicker.setVisible(False)

        self.CreatedFrame.setVisible(True)
        self.ErrorLbl.setText('')
        self.EditBtn.setVisible(True)
        self.DeleteBtn.setVisible(False)
        self.SaveCancelFrame.setVisible(False)
        self.TitleInput.setDisabled(True)
        self.DescriptionInput.setDisabled(True)
        self.DescriptionInput.setVisible(bool(API.item and API.item['description']))
        if API.item:
            self.ImageButton.setIcon(Icon(API.item['icon']).icon)
        self.ImageButton.setDisabled(True)
        self.AddFieldBtn.setVisible(True)
        self.FieldScrollArea.setVisible(True)
        self.AddAttachmentBtn.setVisible(True)
        self.AttachmentScrollArea.setVisible(True)

    @asyncSlot()
    async def show_create(self):
        API.item = None
        API.field_identifiers.clear()
        API.attachment_identifiers.clear()

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
        self.DescriptionInput.setVisible(True)
        self.FieldScrollArea.clear([self.HintLbl2])
        self.HintLbl2.setVisible(True)
        self.AttachmentScrollArea.clear([self.HintLbl3])
        self.HintLbl3.setVisible(True)
        self.CreateBtn.setVisible(True)
        self.FavouriteButton.setVisible(True)
        self.FavouriteButton.state = False

    @asyncSlot()
    async def show_item(self, item: dict[str, Any]):
        API.item = item

        self.ExportBtn.setVisible(True)

        self.CreatedFrame.setVisible(True)
        if created_at := item['created_at']:
            self.CreatedLbl.setText(created_at.strftime(DateTime.defstrf))

        if modified_at := item['modified_at']:
            self.ModifiedLbl.setText(modified_at.strftime(DateTime.defstrf))
        self.ModifiedFrame.setVisible(modified_at is not None)

        if expires_at := item['expires_at']:
            self.ExpiresLbl.setText(expires_at.strftime(DateTime.defstrf))
            self.ExpiresLbl.setVisible(True)
            self.ExpiresSelector.setVisible(False)
            self.DateTimePicker.setVisible(False)
            self.DateTimePicker.setDateTime(expires_at)
        else:
            self.ExpiresSelector.setCurrentText('No')
        self.ExpiresFrame.setVisible(expires_at is not None)

        self.FavouriteButton.state = API.item['is_favourite']
        self.TitleInput.setText(API.item['title'])
        self.TitleInput.setEnabled(False)
        self.ImageButton.setIcon(Icon(API.item['icon']).icon)
        self.ImageButton.setDisabled(True)
        self.DescriptionInput.setText(API.item['description'])
        self.DescriptionInput.setVisible(API.item['description'] is not None)
        self.DescriptionInput.setDisabled(True)
        self.ErrorLbl.setText('')
        self.SaveCancelFrame.setVisible(False)
        self.DeleteBtn.setVisible(False)
        self.EditBtn.setVisible(True)
        self.CreateBtn.setVisible(False)

        self.FieldScrollArea.setVisible(True)
        self.FieldScrollArea.clear([self.HintLbl2])
        for field in API.item['fields']:
            await self.add_field(field)
        self.HintLbl2.setVisible(not len(API.item['fields']))

        self.AttachmentScrollArea.setVisible(True)
        self.AttachmentScrollArea.clear([self.HintLbl3])
        for attachment in API.item['attachments']:
            await self.add_attachment(attachment)
        self.HintLbl3.setVisible(not len(API.item['attachments']))

        CONTEXT.RightPages.setCurrentWidget(CONTEXT.RightPagesItem)
        CONTEXT.RightPages.expand()

    @asyncSlot()
    async def execute_create(self):
        if not len(title := self.TitleInput.text()):
            return self.ErrorLbl.setText('Title can not be empty')
        created_item = await API.create_item(API.category['id'], {
            'icon': self.ImageButton.bytes, 'description': self.DescriptionInput.toPlainText(),
            'title': title, 'is_favourite': self.FavouriteButton.state
        })
        if item_id := created_item.get('id'):
            for identifier in API.field_identifiers:
                field = self.findChild(QFrame, f'Field{identifier}')
                await API.add_field(item_id, {
                    'name': field.FieldNameInput.text(), 'value': field.FieldValueInput.text()
                })
            await CONTEXT.LeftMenu.refresh_categories()
            await CONTEXT.CentralItems.refresh_items()
            await self.show_item(API.item)
        else:
            self.ErrorLbl.setText('Internal error, please try again')

    @asyncSlot()
    async def execute_delete(self):
        deleted_item = await API.delete_item(API.item['id'])
        if item_id := deleted_item.get('id'):
            await CONTEXT.LeftMenu.refresh_categories()
            await CONTEXT.CentralItems.refresh_items()
            await self.execute_cancel()
            await self.show_create()
        else:
            self.ErrorLbl.setText('Internal error, please try again')
