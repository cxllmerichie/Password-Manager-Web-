from aioqui.widgets import Button, LineInput, Layout, Label, TextInput, Spacer, Frame, Popup, Parent
from aioqui.widgets.custom import FavouriteButton, ImageButton, ErrorLabel
from aioqui.qasyncio import asyncSlot
from aioqui.types import Icon
from aioqui import CONTEXT
from PySide6.QtWidgets import QFileDialog
from typing import Any

from ..misc import ICONS, API, PATHS, SIZES, COLORS
from .. import stylesheets


class RightPagesCategory(Frame):
    def __init__(self, parent: Parent):
        super().__init__(parent, self.__class__.__name__, stylesheet=stylesheets.right_pages_category.css +
                                                                     stylesheets.components.favourite_button +
                                                                     stylesheets.components.image_button(COLORS.DARK))

    async def init(self) -> 'RightPagesCategory':
        self.setLayout(await Layout.vertical().init(
            spacing=20, margins=(25, 10, 25, 20),
            items=[
                await Layout.horizontal().init(
                    margins=(0, 0, 0, 20),
                    items=[
                        await FavouriteButton(self).init(
                            pre_slot=self.toggle_favourite, sizes=FavouriteButton.Sizes(fixed_size=SIZES.CONTROL)
                        ), Layout.Left,
                        await Button(self, 'EditBtn', False).init(
                            icon=ICONS.EDIT.adjusted(size=(30, 30)), events=Button.Events(on_click=self.execute_edit),
                            sizes=Button.Sizes(fixed_size=SIZES.CONTROL)
                        ),
                        await Button(self, 'DeleteBtn', False).init(
                            icon=ICONS.TRASH.adjusted(size=(30, 30)), sizes=Button.Sizes(fixed_size=SIZES.CONTROL),
                            events=Button.Events(
                                on_click=lambda: Popup(self.core, stylesheet=stylesheets.components.popup).display(
                                    message=f'Delete category\n\'{API.category["title"]}\'?',
                                    on_success=self.execute_delete
                                )
                            ),
                        ),
                        await Button(self, 'CloseBtn').init(
                            icon=ICONS.CROSS.adjusted(size=(30, 30)), sizes=Button.Sizes(fixed_size=SIZES.CONTROL),
                            events=Button.Events(on_click=CONTEXT.RightPages.shrink)
                        ), Layout.Right
                    ]
                ),
                await ImageButton(self).init(
                    icon=ICONS.CATEGORY, directory=PATHS.ICONS
                ), Layout.TopCenter,
                await LineInput(self, 'TitleInput').init(
                    placeholder='title'
                ), Layout.Top,
                await TextInput(self, 'DescriptionInput').init(
                    placeholder='description (optional)'
                ), Layout.Top,
                await Label(self, 'HintLbl1', False).init(
                    wrap=True, sizes=Label.Sizes(alignment=Layout.Center),
                    text='Hint: Create category like "Social Media" to store your Twitter, Facebook or Instagram personal data'
                ),
                Spacer(False, True),
                await ErrorLabel(self, 'ErrorLbl').init(
                    wrap=True, sizes=ErrorLabel.Sizes(alignment=Layout.Center)
                ), Layout.Center,
                await Button(self, 'CreateBtn').init(
                    text='Create', events=Button.Events(on_click=self.execute_create)
                ),
                await Frame(self, 'SaveCancelFrame', False).init(
                    layout=await Layout.horizontal().init(
                        spacing=20,
                        items=[
                            await Button(self, 'SaveBtn').init(
                                text='Save', events=Button.Events(on_click=self.execute_save)
                            ),
                            await Button(self, 'CancelBtn').init(
                                text='Cancel', events=Button.Events(on_click=self.execute_cancel)
                            )
                        ]
                    )
                ),
                await Layout.horizontal().init(
                    items=[
                        await Button(self, 'ImportBtn', False).init(
                            text='Import item', icon=ICONS.IMPORT, events=Button.Events(on_click=self.import_item)
                        ),
                        await Button(self, 'AddItemBtn', False).init(
                            text='Add item', icon=ICONS.PLUS, events=Button.Events(on_click=self.add_item)
                        )
                    ]
                )
            ]
        ))
        return self

    @asyncSlot()
    async def toggle_favourite(self):
        if not API.category:
            return True
        updated_category = await API.set_category_favourite(API.category['id'], self.FavouriteButton.is_favourite)
        if category_id := updated_category.get('id'):
            self.ErrorLbl.setText('')
            await CONTEXT.LeftMenu.refresh_categories()
            return True
        self.ErrorLbl.setText('Internal error, please try again')
        return False

    @asyncSlot()
    async def add_item(self):
        CONTEXT.RightPages.setCurrentWidget(CONTEXT.RightPagesItem)
        await CONTEXT.RightPagesItem.show_create()

    @asyncSlot()
    async def show_create(self):
        API.category = None
        self.HintLbl1.setVisible(True)
        self.CreateBtn.setVisible(True)
        self.EditBtn.setVisible(False)
        self.SaveCancelFrame.setVisible(False)
        self.AddItemBtn.setVisible(False)
        self.ImageButton.setIcon(ICONS.CATEGORY.icon)
        self.ImageButton.setDisabled(False)
        self.ImageButton.image_bytes = None
        self.FavouriteButton.unset_favourite()
        self.TitleInput.setEnabled(True)
        self.TitleInput.setText('')
        self.DescriptionInput.setDisabled(False)
        self.DescriptionInput.setText('')
        self.DescriptionInput.setVisible(True)
        self.ImportBtn.setVisible(False)

        await CONTEXT.CentralItems.refresh_items([])
        CONTEXT.RightPages.setCurrentWidget(CONTEXT.RightPagesCategory)
        CONTEXT.RightPages.expand()

    @asyncSlot()
    async def import_item(self):
        filepath, _ = QFileDialog.getOpenFileName(self, 'Choose a file to import', '', 'JSON Files (*.json)')
        if filepath:
            imported_item = await API.import_item(filepath)
            if item_id := imported_item.get('id'):
                await CONTEXT.LeftMenu.refresh_categories()
                await CONTEXT.CentralItems.refresh_items()
                await CONTEXT.RightPagesItem.show_item(imported_item)

    @asyncSlot()
    async def execute_delete(self):
        deleted_category = await API.delete_category(API.category['id'])
        if category_id := deleted_category.get('id'):
            self.TitleInput.setText('')
            self.DescriptionInput.setText('')
            self.DeleteBtn.setVisible(False)

            await CONTEXT.LeftMenu.refresh_categories()
            await self.show_create()
        else:
            self.ErrorLbl.setText('Internal error, please try again')

    @asyncSlot()
    async def execute_edit(self):
        self.ImportBtn.setVisible(False)
        self.CreateBtn.setVisible(False)
        self.SaveCancelFrame.setVisible(True)
        self.AddItemBtn.setVisible(False)
        self.ImageButton.setDisabled(False)
        self.EditBtn.setVisible(False)
        self.TitleInput.setEnabled(True)
        self.DescriptionInput.setDisabled(False)
        self.DescriptionInput.setVisible(True)
        self.DeleteBtn.setVisible(True)

    @asyncSlot()
    async def execute_save(self):
        if not len(title := self.TitleInput.text()):
            return self.ErrorLbl.setText('Title can not be empty')
        prev_icon = API.category['icon']
        updated_category = await API.update_category(API.category['id'], {
            'icon': self.ImageButton.image_bytes_str, 'title': title,
            'description': self.DescriptionInput.toPlainText(), 'is_favourite': self.FavouriteButton.is_favourite
        })
        if category_id := updated_category.get('id'):
            CONTEXT.LeftMenu.refresh_categories()
            await self.execute_cancel()
            await self.show_category(API.category)

            if prev_icon != (curr_icon := API.category['icon']):
                await API.save_icon(curr_icon)
        else:
            self.ErrorLbl.setText('Internal error, please try again')

    @asyncSlot()
    async def execute_cancel(self):
        self.ErrorLbl.setText('')
        self.TitleInput.setEnabled(False)
        self.ImageButton.setIcon(Icon(API.category['icon']).icon)
        self.ImageButton.setDisabled(True)
        self.DescriptionInput.setDisabled(True)
        self.DescriptionInput.setVisible(API.category['description'] is not None)
        self.SaveCancelFrame.setVisible(False)
        self.AddItemBtn.setVisible(True)
        self.DeleteBtn.setVisible(False)
        self.EditBtn.setVisible(True)

    @asyncSlot()
    async def show_category(self, category: dict[str, Any]):
        API.category = category
        self.FavouriteButton.set(API.category['is_favourite'])
        self.TitleInput.setEnabled(False)
        self.TitleInput.setText(API.category['title'])
        self.ImageButton.setIcon(Icon(API.category['icon']).icon)
        self.ImageButton.setDisabled(True)
        self.DescriptionInput.setText(API.category['description'])
        self.DescriptionInput.setDisabled(True)
        self.DescriptionInput.setVisible(API.category['description'] is not None)
        self.ErrorLbl.setText('')
        self.SaveCancelFrame.setVisible(False)
        self.AddItemBtn.setVisible(True)
        self.CreateBtn.setVisible(False)
        self.EditBtn.setVisible(True)
        self.DeleteBtn.setVisible(False)
        self.HintLbl1.setVisible(False)
        self.ImportBtn.setVisible(True)

        CONTEXT.RightPages.setCurrentWidget(CONTEXT.RightPagesCategory)
        CONTEXT.RightPages.expand()
        await CONTEXT.CentralItems.refresh_items()

    @asyncSlot()
    async def execute_create(self):
        title = self.TitleInput.text()
        if not len(title):
            return self.ErrorLbl.setText('Title can not be empty')
        created_category = await API.create_category({
            'icon': self.ImageButton.image_bytes_str, 'title': title,
            'description': self.DescriptionInput.toPlainText(), 'is_favourite': self.FavouriteButton.is_favourite
        })
        if created_category.get('id'):
            await CONTEXT.LeftMenu.refresh_categories()
            await self.show_category(API.category)
        else:
            self.ErrorLbl.setText('Internal error, please try again')
