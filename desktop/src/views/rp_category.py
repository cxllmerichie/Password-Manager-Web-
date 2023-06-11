from aioqui.widgets.custom import StateButton, DurationLabel, Popup
from aioqui.widgets import Button, Input, Layout, Label, Spacer, Frame, Parent
from aioqui.misc.fileops import select_file
from aioqui.asynq import asyncSlot
from aioqui.types import Icon
from aioqui import CONTEXT
from typing import Any

from ..components import ImageButton
from ..misc import ICONS, API, PATHS, SIZES, COLORS
from .. import qss


class RightPagesCategory(Frame):
    def __init__(self, parent: Parent):
        super().__init__(parent, self.__class__.__name__, qss=(
            qss.rp_category.css,
            qss.components.image_button(COLORS.DARK),
        ))

    async def init(self) -> 'RightPagesCategory':
        self.setLayout(await Layout.vertical().init(
            spacing=20, margins=(25, 10, 25, 20),
            items=[
                await Layout.horizontal().init(
                    margins=(0, 0, 0, 20),
                    items=[
                        await StateButton(self, 'FavBtn').init(
                            event=self.toggle_favourite, fix_size=SIZES.CONTROL
                        ), Layout.Left,
                        await Button(self, 'EditBtn', False).init(
                            icon=ICONS.EDIT.adjusted(size=(30, 30)), on_click=self.execute_edit, fix_size=SIZES.CONTROL
                        ),
                        await Button(self, 'DeleteBtn', False).init(
                            icon=ICONS.TRASH.adjusted(size=(30, 30)), fix_size=SIZES.CONTROL,
                            on_click=lambda: Popup(
                                self.core, on_success=self.execute_delete,
                                message=f'Delete category\n\'{API.category["title"]}\'?'
                            ).display(),
                        ),
                        await Button(self, 'CloseBtn').init(
                            icon=ICONS.CROSS.adjusted(size=(30, 30)), fix_size=SIZES.CONTROL,
                            on_click=CONTEXT.RightPages.shrink
                        ), Layout.Right
                    ]
                ),
                await ImageButton(self, 'ImageBtn').init(
                    icon=ICONS.CATEGORY, directory=PATHS.ICONS
                ), Layout.TopCenter,
                await Input.line(self, 'TitleInp').init(
                    placeholder='title'
                ), Layout.Top,
                await Input.reach(self, 'DescInp').init(
                    placeholder='description (optional)'
                ), Layout.Top,
                await Label(self, 'HintLbl1', False).init(
                    wrap=True, alignment=Layout.Center,
                    text='Hint: Create category like "Social Media" to store your Twitter, Facebook or Instagram personal data'
                ),
                Spacer(Spacer.Minimum, Spacer.Expanding),
                await DurationLabel(self, 'ErrorLbl').init(
                    wrap=True, alignment=Layout.Center
                ), Layout.Center,
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
                ),
                await Layout.horizontal().init(
                    items=[
                        await Button(self, 'ImportBtn', False).init(
                            text='Import item', icon=ICONS.IMPORT, on_click=self.import_item
                        ),
                        await Button(self, 'AddItemBtn', False).init(
                            text='Add item', icon=ICONS.PLUS, on_click=self.add_item
                        )
                    ]
                )
            ]
        ))
        return self

    @asyncSlot()
    async def toggle_favourite(self) -> bool:
        if not API.category:
            return True
        updated_category = await API.set_category_favourite(API.category['id'], not self.FavBtn.state)
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
        self.ImageBtn.setIcon(ICONS.CATEGORY.icon)
        self.ImageBtn.setDisabled(False)
        self.ImageBtn.image_bytes = None
        self.FavBtn.state = False
        self.TitleInp.setEnabled(True)
        self.TitleInp.setText('')
        self.DescInp.setDisabled(False)
        self.DescInp.setText('')
        self.DescInp.setVisible(True)
        self.ImportBtn.setVisible(False)

        await CONTEXT.CentralItems.refresh_items([])
        CONTEXT.RightPages.setCurrentWidget(CONTEXT.RightPagesCategory)
        CONTEXT.RightPages.expand()

    @asyncSlot()
    async def import_item(self):
        if filepath := await select_file(self, filters='JSON (*.json)'):
            imported_item = await API.import_item(filepath)
            if item_id := imported_item.get('id'):
                await CONTEXT.LeftMenu.refresh_categories()
                await CONTEXT.CentralItems.refresh_items()
                await CONTEXT.RightPagesItem.show_item(imported_item)

    @asyncSlot()
    async def execute_delete(self):
        deleted_category = await API.delete_category(API.category['id'])
        if category_id := deleted_category.get('id'):
            self.TitleInp.setText('')
            self.DescInp.setText('')
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
        self.ImageBtn.setDisabled(False)
        self.EditBtn.setVisible(False)
        self.TitleInp.setEnabled(True)
        self.DescInp.setDisabled(False)
        self.DescInp.setVisible(True)
        self.DeleteBtn.setVisible(True)

    @asyncSlot()
    async def execute_save(self):
        if not len(title := self.TitleInp.text()):
            return self.ErrorLbl.setText('Title can not be empty')
        prev_icon = API.category['icon']
        updated_category = await API.update_category(API.category['id'], {
            'icon': self.ImageBtn.bytes, 'title': title,
            'description': self.DescInp.text(), 'is_favourite': self.FavBtn.state
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
        self.TitleInp.setEnabled(False)
        self.ImageBtn.setIcon(Icon(API.category['icon']).icon)
        self.ImageBtn.setDisabled(True)
        self.DescInp.setDisabled(True)
        self.DescInp.setVisible(API.category['description'] is not None)
        self.SaveCancelFrame.setVisible(False)
        self.AddItemBtn.setVisible(True)
        self.DeleteBtn.setVisible(False)
        self.EditBtn.setVisible(True)

    @asyncSlot()
    async def show_category(self, category: dict[str, Any]):
        API.category = category
        self.FavBtn.state = API.category['is_favourite']
        self.TitleInp.setEnabled(False)
        self.TitleInp.setText(API.category['title'])
        self.ImageBtn.setIcon(Icon(API.category['icon']).icon)
        self.ImageBtn.setDisabled(True)
        self.DescInp.setText(API.category['description'])
        self.DescInp.setDisabled(True)
        self.DescInp.setVisible(API.category['description'] is not None)
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
        title = self.TitleInp.text()
        if not len(title):
            return self.ErrorLbl.setText('Title can not be empty')
        created_category = await API.create_category({
            'icon': self.ImageBtn.bytes, 'title': title,
            'description': self.DescInp.text(), 'is_favourite': self.FavBtn.state
        })
        if created_category.get('id'):
            await CONTEXT.LeftMenu.refresh_categories()
            await self.show_category(API.category)
        else:
            self.ErrorLbl.setText('Internal error, please try again')
