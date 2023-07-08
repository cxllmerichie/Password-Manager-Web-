from aioqui.widgets import Button, Input, Layout, Label, Frame, ScrollArea, Selector, Parent, DateTime
from aioqui.widgets.custom import StateButton, DurationLabel, Popup
from aioqui.misc.fileops import select_file, select_dir, explore_dir
from aioqui.asynq import asyncSlot
from aioqui.types import Icon
from aioqui import CONTEXT
from PySide6.QtWidgets import QFrame
from typing import Any
from datetime import datetime

from ..misc import ICONS, api, PATHS, SIZES
from ..components import Field, Attachment, ImageButton
from .. import qss


class RightPagesItem(Frame):
    item: dict[str, Any] = None
    category_id: int = None

    def __init__(self, parent: Parent):
        super().__init__(parent, self.__class__.__name__, qss=(
            qss.rp_item.css,
            qss.components.scroll,
            qss.components.image_button()
        ))

    async def init(self) -> 'RightPagesItem':
        self.setLayout(await Layout.vertical().init(
            spacing=20, margins=(25, 10, 25, 20),
            items=[
                await Layout.horizontal().init(
                    margins=(0, 0, 0, 20),
                    items=[
                        await StateButton(self, 'FavBtn').init(
                            event=self.toggle_favourite, fix_size=SIZES.CONTROL
                        ), Layout.Left,
                        await Button(self, 'EditBtn').init(
                            icon=ICONS.EDIT.adjusted(size=(30, 30)), on_click=self.show_edit, fix_size=SIZES.CONTROL
                        ),
                        await Button(self, 'DeleteBtn', False).init(
                            icon=ICONS.TRASH.adjusted(size=(30, 30)), fix_size=SIZES.CONTROL,
                            on_click=lambda: Popup(
                                self.core, qss=qss.components.popup, on_success=self.execute_delete,
                                message=f'Delete item\n\'{self.item["title"]}\'?'
                            ).display()
                        ),
                        await Button(self, 'CloseBtn').init(
                            icon=ICONS.CROSS.adjusted(size=(30, 30)), fix_size=SIZES.CONTROL,
                            on_click=CONTEXT.RightPages.shrink
                        ), Layout.Right
                    ]
                ),
                await ImageButton(self, 'ImageBtn').init(
                    icon=ICONS.ITEM, directory=PATHS.ICONS
                ), Layout.TopCenter,
                await Input.line(self, 'TitleInp').init(
                    placeholder='title'
                ), Layout.Top,
                await Frame(self, 'CreatedFrame', False).init(
                    layout=await Layout.horizontal().init(
                        items=[
                            await Label(self, 'CreatedHintLbl').init(
                                text='Created:'
                            ),
                            await Label(self, 'CreatedLbl').init()
                        ]
                    )
                ),
                await Frame(self, 'ModifiedFrame', False).init(
                    layout=await Layout.horizontal().init(
                        items=[
                            await Label(self, 'ModifiedHintLbl').init(
                                text='Modified:'
                            ),
                            await Label(self, 'ModifiedLbl').init()
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
                                alignment=Layout.Top,
                                items=[
                                    await Selector(self, 'ExpiresSelector').init(
                                        on_change=self.expires_textchanged,
                                        items=[
                                            Selector.Item(text='No'),
                                            Selector.Item(text='Yes'),
                                        ]
                                    ),
                                    await DateTime(self, 'DateTime', False).init(),
                                ]
                            )
                        ]
                    )
                ),
                await Input.reach(self, 'DescInp').init(
                    placeholder='description (optional)'
                ), Layout.Top,
                await Frame(self, 'FieldFrame').init(
                    layout=await Layout.vertical().init(
                        items=[
                            await ScrollArea(self, 'FieldScrollArea').init(
                                orientation=Layout.Vertical, alignment=Layout.Top, margins=(5, 10, 5, 0), spacing=10,
                                items=[
                                    await Label(self, 'HintLbl2').init(
                                        wrap=True, text='Hint: Add new field with name "password" or "username" and it\'s value',
                                        alignment=Label.Center
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
                                        text='Hint: Attach documents (*.txt, *.jpg) to the item', wrap=True,
                                        alignment=Label.Center
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
            print(self.item)
            await explore_dir(await api.export_item(self.item, directory))
            print(self.item)

    @asyncSlot()
    async def add_field(self, field: dict[str, Any] = None):
        self.HintLbl2.setVisible(False)
        self.FieldScrollArea.widget().layout().addWidget(await Field(self, field).init())

    @asyncSlot()
    async def add_attachment(self, attachment: dict[str, Any] = None):
        creating = attachment is None
        if not attachment:
            if filepath := await select_file(self, filters='Images (*.jpg);;Documents (*.txt)'):
                attachment = await api.get_attachment_data(filepath)
        if attachment:
            self.HintLbl3.setVisible(False)
            self.AttachmentScrollArea.widget().layout().addWidget(await Attachment(self, attachment, creating).init())

    @asyncSlot()
    async def expires_textchanged(self):
        yes = self.ExpiresSelector.currentText() == 'Yes'
        self.DateTime.setVisible(yes)
        # editable when selector visible (on edit)
        self.DateTime.setReadOnly(not self.ExpiresSelector.isVisible())

    @asyncSlot()
    async def show_edit(self):
        self.ExportBtn.setVisible(False)
        self.CreatedFrame.setVisible(False)
        self.ModifiedFrame.setVisible(False)
        self.ExpiresFrame.setVisible(True)
        self.ExpiresSelector.setVisible(True)
        if expires_at := self.item['expires_at']:
            self.ExpiresSelector.setCurrentText('No')  # workaround
            self.ExpiresSelector.setCurrentText('Yes')
            self.DateTime.setDateTime(expires_at)
        else:
            self.ExpiresSelector.setCurrentText('No')
            self.DateTime.setDateTime(datetime.now())
        self.CreateBtn.setVisible(False)
        self.EditBtn.setVisible(False)
        self.DeleteBtn.setVisible(True)
        self.SaveCancelFrame.setVisible(True)
        self.TitleInp.setDisabled(False)
        self.DescInp.setDisabled(False)
        self.DescInp.setVisible(True)
        self.ImageBtn.setDisabled(False)
        self.AddFieldBtn.setVisible(False)
        self.AddAttachmentBtn.setVisible(False)
        self.FieldScrollArea.setVisible(False)
        self.AttachmentScrollArea.setVisible(False)

    @asyncSlot()
    async def toggle_favourite(self) -> bool:
        if not self.item:
            return True
        to_update = self.item
        self.item['is_favourite'] = not self.FavBtn.state
        updated_item = await api.update_item(self.item['id'], to_update)
        if item_id := updated_item.get('id'):
            self.item = updated_item
            await CONTEXT.LeftMenu.refresh_categories()
            await CONTEXT.CentralItems.refresh_items(await api.get_items(self.item['category_id']))
            return True
        self.ErrorLbl.setText('Internal error, please try again')
        return False

    @asyncSlot()
    async def execute_save(self):
        if not len(title := self.TitleInp.text()):
            return self.ErrorLbl.setText('Title can not be empty')
        expires_at = None
        if self.ExpiresSelector.currentText() == 'Yes':
            expires_at = str(self.DateTime.dateTime())
        prev_icon = self.item['icon']
        updated_item = await api.update_item(self.item['id'], {
            'icon': self.ImageBtn.bytes, 'title': title, 'description': self.DescInp.text(),
            'is_favourite': self.FavBtn.state, 'expires_at': expires_at
        })
        if item_id := updated_item.get('id'):
            self.item = updated_item
            await CONTEXT.LeftMenu.refresh_categories()
            await CONTEXT.CentralItems.refresh_items(await api.get_items(self.item['category_id']))
            await self.execute_cancel()
            await self.show_item(self.item)
            if prev_icon != (curr_icon := self.item['icon']):
                await api.save_icon(curr_icon)
        else:
            self.ErrorLbl.setText('Internal error, please try again')

    @asyncSlot()
    async def execute_cancel(self):
        self.ExportBtn.setVisible(True)
        self.ModifiedFrame.setVisible(bool(self.item and self.item['modified_at']))
        if expires := (self.item and self.item['expires_at']):
            self.ExpiresSelector.setVisible(False)
            self.DateTime.setVisible(True)
            self.DateTime.setDateTime(self.item['expires_at'])
            self.DateTime.setReadOnly(True)
        self.ExpiresFrame.setVisible(bool(expires))

        self.CreatedFrame.setVisible(True)
        self.ErrorLbl.setText('')
        self.EditBtn.setVisible(True)
        self.DeleteBtn.setVisible(False)
        self.SaveCancelFrame.setVisible(False)
        self.TitleInp.setDisabled(True)
        self.DescInp.setDisabled(True)
        self.DescInp.setVisible(bool(self.item and self.item['description']))
        if self.item:
            self.ImageBtn.setIcon(Icon(self.item['icon']).icon)
        self.ImageBtn.setDisabled(True)
        self.AddFieldBtn.setVisible(True)
        self.FieldScrollArea.setVisible(True)
        self.AddAttachmentBtn.setVisible(True)
        self.AttachmentScrollArea.setVisible(True)

    @asyncSlot()
    async def show_create(self, category_id: int):
        self.item = None
        self.category_id = category_id

        api.fields.clear()
        api.attachments.clear()

        self.ExportBtn.setVisible(False)
        self.CreatedFrame.setVisible(False)
        self.ModifiedFrame.setVisible(False)
        self.ExpiresFrame.setVisible(True)
        self.DeleteBtn.setVisible(False)
        self.ImageBtn.setIcon(ICONS.ITEM.icon)
        self.ImageBtn.default = True
        self.ImageBtn.setEnabled(True)
        self.EditBtn.setVisible(False)
        self.TitleInp.setEnabled(True)
        self.TitleInp.setText('')
        self.DescInp.setEnabled(True)
        self.DescInp.setText('')
        self.DescInp.setVisible(True)
        self.FieldScrollArea.clear([self.HintLbl2])
        self.HintLbl2.setVisible(True)
        self.AttachmentScrollArea.clear([self.HintLbl3])
        self.HintLbl3.setVisible(True)
        self.CreateBtn.setVisible(True)
        self.FavBtn.setVisible(True)
        self.FavBtn.state = False

    @asyncSlot()
    async def show_item(self, item: dict[str, Any]):
        self.item = item

        self.ExportBtn.setVisible(True)

        self.CreatedFrame.setVisible(True)
        if created_at := item['created_at']:
            self.CreatedLbl.setText(created_at.strftime(DateTime.format))

        if modified_at := item['modified_at']:
            self.ModifiedLbl.setText(modified_at.strftime(DateTime.format))
        self.ModifiedFrame.setVisible(modified_at is not None)

        if expires_at := item['expires_at']:
            self.ExpiresSelector.setCurrentText('Yes')
            self.ExpiresSelector.setVisible(False)
            self.DateTime.setDateTime(expires_at)
        else:
            self.ExpiresSelector.setCurrentText('No')
        self.ExpiresFrame.setVisible(expires_at is not None)

        self.FavBtn.state = self.item['is_favourite']
        self.TitleInp.setText(self.item['title'])
        self.TitleInp.setEnabled(False)
        self.ImageBtn.setIcon(Icon(self.item['icon']).icon)
        self.ImageBtn.setDisabled(True)
        self.DescInp.setText(self.item['description'])
        self.DescInp.setVisible(bool(self.item['description']))
        self.DescInp.setDisabled(True)
        self.ErrorLbl.setText('')
        self.SaveCancelFrame.setVisible(False)
        self.DeleteBtn.setVisible(False)
        self.EditBtn.setVisible(True)
        self.CreateBtn.setVisible(False)

        self.FieldScrollArea.setVisible(True)
        self.FieldScrollArea.clear([self.HintLbl2])
        for field in (fields := await api.get_fields(self.item['id'])):
            await self.add_field(field)
        self.HintLbl2.setVisible(not len(fields))

        self.AttachmentScrollArea.setVisible(True)
        self.AttachmentScrollArea.clear([self.HintLbl3])
        for attachment in (attachments := await api.get_attachments(self.item['id'])):
            await self.add_attachment(attachment)
        self.HintLbl3.setVisible(not len(attachments))

        CONTEXT.RightPages.setCurrentWidget(CONTEXT.RightPagesItem)
        CONTEXT.RightPages.expand()

    @asyncSlot()
    async def execute_create(self):
        if not len(title := self.TitleInp.text()):
            return self.ErrorLbl.setText('Title can not be empty')
        created_item = await api.create_item(self.category_id, {
            'icon': self.ImageBtn.bytes, 'description': self.DescInp.text(),
            'title': title, 'is_favourite': self.FavBtn.state
        })
        if item_id := created_item.get('id'):
            self.item = created_item
            for identifier in api.fields:
                field = self.findChild(QFrame, f'Field{identifier}')
                await api.add_field(item_id, {
                    'name': field.NameInp.text(), 'value': field.ValueInp.text()
                })
            await CONTEXT.LeftMenu.refresh_categories()
            await CONTEXT.CentralItems.refresh_items(await api.get_items(self.item['category_id']))
            await self.show_item(self.item)
        else:
            self.ErrorLbl.setText('Internal error, please try again')

    @asyncSlot()
    async def execute_delete(self):
        deleted_item = await api.delete_item(self.item['id'])
        if item_id := deleted_item.get('id'):
            self.item = None
            await CONTEXT.LeftMenu.refresh_categories()
            await CONTEXT.CentralItems.refresh_items(await api.get_items(deleted_item['category_id']))
            await self.execute_cancel()
            await self.show_create()
        else:
            self.ErrorLbl.setText('Internal error, please try again')
