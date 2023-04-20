from PyQt5.QtWidgets import QWidget, QFrame
from PyQt5.QtCore import pyqtSlot
from uuid import uuid4
from typing import Any

from ..widgets import Button, LineInput, Layout, Label, TextInput, Spacer, Frame, ScrollArea, ui
from ..custom import FavouriteButton, ImageButton
from ..misc import Icons, api, Colors
from .. import css


class Field(Frame):
    def __init__(self, parent: QWidget, item_id: int, field: dict[str, Any] = None):
        self.identifier = str(uuid4())

        super().__init__(parent, f'Field{self.identifier}', stylesheet=css.rp_item.field + f'''
            #Field{self.identifier} {{
                background-color: {Colors.DARK_GRAY};
                border-radius: 5px;
            }}
        ''')

        self.item_id = item_id
        self.field = field

    def init(self) -> 'Field':
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
                    icon=Icons.EYE, slot=self.FieldValueInput.toggle_echo
                ),
                Button(self, 'FieldCopyBtn').init(
                    icon=Icons.COPY
                ),
                Button(self, f'FieldEditBtn').init(
                    icon=Icons.EDIT.adjusted(size=Icons.SAVE.size), slot=self.execute_edit
                ),
                Button(self, f'FieldSaveBtn').init(
                    icon=Icons.SAVE, slot=self.execute_save
                ),
                Button(self, f'FieldDeleteBtn').init(
                    icon=Icons.CROSS_CIRCLE, slot=self.execute_delete
                )
            ]
        ))

        if self.field and self.item_id:
            self.FieldDeleteBtn.setVisible(False)
            self.FieldNameInput.setText(self.field['name'])
            self.FieldNameInput.setDisabled(True)
            self.FieldValueInput.setText(self.field['value'])
            self.FieldValueInput.hide_echo()
            self.FieldValueInput.setDisabled(True)
            self.FieldSaveBtn.setVisible(False)
            self.FieldEditBtn.setVisible(True)
        elif self.item_id:
            self.FieldDeleteBtn.setVisible(True)
            self.FieldSaveBtn.setVisible(True)
            self.FieldEditBtn.setVisible(False)
            self.FieldCopyBtn.setVisible(False)
            self.FieldHideBtn.setVisible(False)
        else:
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
            response = api.update_field(self.field['id'], field)
        else:
            response = api.add_field(self.item_id, field)
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
        self.setVisible(False)
        self.RP_Item.field_identifiers.remove(self.identifier)
        if self.field:
            api.remove_field(self.field['id'])
        self.deleteLater()

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


class RP_Item(Frame):
    def __init__(self, parent: QWidget):
        super().__init__(parent, self.__class__.__name__,
                         stylesheet=css.rp_item.css + css.components.scroll + css.components.img_btn + css.components.fav_btn)

        self.item = None
        self.category_id = None
        self.field_identifiers = []

    def init(self) -> 'RP_Item':
        self.setLayout(Layout.vertical().init(
            spacing=20, margins=(25, 10, 25, 20),
            items=[
                Layout.horizontal().init(
                    margins=(0, 0, 0, 20),
                    items=[
                        FavouriteButton(self).init(
                            icon=Icons.STAR.adjusted(size=(30, 30)), slot=self.toggle_favourite
                        ), Layout.Left,
                        Button(self, 'EditBtn').init(
                            icon=Icons.EDIT.adjusted(size=(30, 30)), slot=self.execute_edit
                        ),
                        Button(self, 'RemoveBtn', False).init(
                            icon=Icons.TRASH.adjusted(size=(30, 30)), slot=self.execute_delete
                        ),
                        Button(self, 'CloseBtn').init(
                            icon=Icons.CROSS.adjusted(size=(30, 30)), slot=ui.RightPages.shrink
                        ), Layout.Right
                    ]
                ),
                ImageButton(self).init(
                    icon=Icons.CATEGORY
                ), Layout.TopCenter,
                LineInput(self, 'TitleInput').init(
                    placeholder='title'
                ), Layout.Top,
                TextInput(self, 'DescriptionInput').init(
                    placeholder='description (optional)'
                ), Layout.Top,
                Frame(self, 'AddBtnsFrame').init(
                    layout=Layout.horizontal().init(
                        items=[
                            Button(self, 'AddDocumentBtn').init(
                                text='Add document', icon=Icons.PLUS
                            ),
                            Button(self, 'AddFieldBtn').init(
                                text='Add field', icon=Icons.PLUS, slot=self.add_field
                            )
                        ]
                    )
                ),
                ScrollArea(self, 'FieldScrollArea').init(
                    orientation=Layout.Vertical, alignment=Layout.Top, margins=(5, 10, 5, 0), spacing=10
                ),
                Label(self, 'ErrorLbl').init(
                    wrap=True, alignment=Layout.Center
                ), Layout.Center,
                Button(self, 'CreateBtn').init(
                    text='Create item', slot=self.execute_create
                ), Layout.HCenter,
                Frame(self, 'SaveCancelFrame', False).init(
                    layout=Layout.horizontal().init(
                        spacing=50,
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
    def add_field(self, field: dict[str, Any] = None):
        layout = self.FieldScrollArea.widget().layout()
        item_id = None
        if self.item:
            item_id = self.item['id']
        layout.addWidget(field := Field(self, item_id, field).init())
        self.field_identifiers.append(field.identifier)

    @pyqtSlot()
    def add_document(self):
        ...

    @pyqtSlot()
    def execute_edit(self):
        self.CreateBtn.setVisible(False)
        self.EditBtn.setVisible(False)
        self.RemoveBtn.setVisible(True)
        self.SaveCancelFrame.setVisible(True)
        self.TitleInput.setDisabled(False)
        self.DescriptionInput.setDisabled(False)
        self.ImageButton.setDisabled(False)
        self.AddFieldBtn.setVisible(False)
        self.AddDocumentBtn.setVisible(False)

    @pyqtSlot()
    def toggle_favourite(self):
        if self.item:
            item = {'title': self.TitleInput.text(), 'is_favourite': self.FavouriteButton.is_favourite}
            self.item = api.update_item(self.item['id'], item)
            ui.LeftMenu.refresh_categories(api.get_categories())

    @pyqtSlot()
    def execute_save(self):
        title = self.TitleInput.text()
        if not len(title):
            return self.ErrorLbl.setText('Title can not be empty')
        item = {'icon': self.ImageButton.icon_bytes, 'title': title,
                'description': self.DescriptionInput.toPlainText(), 'is_favourite': self.FavouriteButton.is_favourite}
        if (item := api.update_item(self.item['id'], item)).get('id'):
            self.execute_cancel()
            self.item = item
            ui.LeftMenu.refresh_categories(api.get_categories())
            ui.CP_Items.refresh_items(api.get_items(self.category_id))
        else:
            self.ErrorLbl.setText('Internal error, please try again')

    @pyqtSlot()
    def execute_cancel(self):
        self.ErrorLbl.setText('')
        self.EditBtn.setVisible(True)
        self.RemoveBtn.setVisible(False)
        self.SaveCancelFrame.setVisible(False)
        self.TitleInput.setDisabled(True)
        self.DescriptionInput.setDisabled(True)
        self.ImageButton.setDisabled(True)
        self.AddFieldBtn.setVisible(True)
        self.AddDocumentBtn.setVisible(True)

    def show_create(self):
        self.item = None
        self.EditBtn.setVisible(False)
        self.TitleInput.setEnabled(True)
        self.TitleInput.setText('')
        self.DescriptionInput.setEnabled(True)
        self.DescriptionInput.setText('')
        self.FieldScrollArea.clear()
        self.CreateBtn.setVisible(True)

    def show_item(self, item: dict[str, Any]):
        self.item = item
        if not self.category_id:
            self.category_id = item['category_id']  # item shown from click through `CentralPages` items
        self.FavouriteButton.set(item['is_favourite'])
        self.TitleInput.setText(item['title'])
        self.TitleInput.setEnabled(False)
        self.ImageButton.setIcon(Icons.from_bytes(item['icon']).icon)
        self.ImageButton.setDisabled(True)
        self.DescriptionInput.setText(item['description'])
        self.DescriptionInput.setDisabled(True)
        self.ErrorLbl.setText('')
        self.SaveCancelFrame.setVisible(False)
        self.EditBtn.setVisible(True)
        self.CreateBtn.setVisible(False)

        self.FieldScrollArea.clear()
        for field in item['fields']:
            self.add_field(field)

        ui.RightPages.setCurrentWidget(ui.RP_Item)
        ui.RightPages.expand()

    @pyqtSlot()
    def execute_create(self):
        if not len(title := self.TitleInput.text()):
            return self.ErrorLbl.setText('Title can not be empty')
        fields = [self.findChild(QFrame, f'Field{identifier}') for identifier in self.field_identifiers]
        fields = [{'name': field.FieldNameInput.text(), 'value': field.FieldValueInput.text()} for field in fields]
        item = {'icon': self.ImageButton.icon_bytes, 'title': title, 'description': self.DescriptionInput.toPlainText(),
                'is_favourite': self.FavouriteButton.is_favourite}
        if (item := api.create_item(self.category_id, item, fields)).get('id'):
            self.ImageButton.setIcon(Icons.from_bytes(item['icon']).icon)
            self.show_item(item)
            self.item = item
            self.CreateBtn.setVisible(False)
            ui.LeftMenu.refresh_categories(api.get_categories())
            ui.CP_Items.refresh_items(api.get_items(self.category_id))
        else:
            self.ErrorLbl.setText('Internal error, please try again')

    @pyqtSlot()
    def execute_delete(self):
        if (item := api.delete_item(self.item['id'])).get('id'):
            self.item = None
            self.TitleInput.setText('')
            self.DescriptionInput.setText('')
            self.DeleteBtn.setVisible(False)
            self.show_create()
            ui.LeftMenu.refresh_categories(api.get_categories())
            ui.CP_Items.refresh_items(api.get_items(self.category_id))
        else:
            self.ErrorLbl.setText('Internal error, please try again')
