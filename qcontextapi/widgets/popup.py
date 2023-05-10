from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QMessageBox, QWidget
from qasync import asyncSlot

from .widget import Widget
from .layout import Layout
from .button import Button
from .label import Label
from .frame import Frame


class Popup(Widget):
    YES = QMessageBox.Yes
    NO = QMessageBox.No
    OK = QMessageBox.Ok
    CANCEL = QMessageBox.Cancel

    stylesheet = f'''
        #Popup {{
            background-color: rgba(255, 255, 255, 0.1);
        }}

        #PopupFrame {{
            background-color: #17212B;
            min-width: 400px;
            min-height: 200px;
            border-radius: 20px;
        }}

        #PopupMessageLbl {{
            color: white;
            font-size: 24px;
            background-color: transparent;
        }}

        #PopupYesBtn,
        #PopupNoBtn {{
            color: white;
            border: none;
            font-size: 18px; 
            border-radius: 5px;
            min-height: 40px;
        }}

        #PopupYesBtn {{
            background-color: darkgreen;
        }}

        #PopupYesBtn:hover {{
            background-color: rgba(0, 255, 0, 0.5);
        }}

        #PopupNoBtn {{
            background-color: rgba(182, 0, 40, 1);
        }}

        #PopupNoBtn:hover {{
            background-color: rgba(182, 0, 40, 0.5);
        }}
        '''

    def __init__(self, parent: QWidget, name: str = None, stylesheet: str = stylesheet):
        super().__init__(parent, name if name else self.__class__.__name__, True, stylesheet)

    @asyncSlot()
    async def display(
            self, *,
            message: str = '',
            on_success: callable = lambda: None, on_failure: callable = lambda: None
    ) -> 'Popup':
        self.setLayout(await Layout.vertical().init(
            spacing=10, alignment=Layout.Center, margins=(20, 20, 20, 20),
            items=[
                await Frame(self, f'{self.objectName()}Frame').init(
                    layout=await Layout.vertical().init(
                        spacing=20, margins=(20, 20, 20, 20),
                        items=[
                            await Label(self, f'{self.objectName()}MessageLbl').init(
                                text=message, wrap=True, alignment=Layout.Center
                            ),
                            await Layout.horizontal().init(
                                spacing=20,
                                items=[
                                    await Button(self, f'{self.objectName()}YesBtn').init(
                                        text='Yes', slot=lambda: self.slot(on_success)
                                    ),
                                    await Button(self, f'{self.objectName()}NoBtn').init(
                                        text='No', slot=lambda: self.slot(on_failure)
                                    )
                                ]
                            )
                        ]
                    )
                )
            ]
        ))
        return self

    @asyncSlot()
    async def slot(self, slot: callable):
        slot()
        self.deleteLater()

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.resize(self.parent().size())
