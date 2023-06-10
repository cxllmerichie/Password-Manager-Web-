from aioqui.widgets import Layout, Label, Frame, Parent
from aioqui.types import Icon
from aioqui import CONTEXT
from typing import Any

from .. import qss


class CentralItem(Frame):
    def __init__(self, parent: Parent):
        super().__init__(parent, self.__class__.__name__, qss=qss.central_item.css)

    async def init(self, item: dict[str, Any]) -> 'CentralItem':
        await super().init(
            on_click=lambda: CONTEXT.RightPagesItem.show_item(item),
            layout=await Layout.horizontal(self).init(
                margins=(10, 10, 10, 10), alignment=Layout.Left, spacing=20,
                items=[
                    await Label(self, 'IconLbl').init(
                        icon=Icon(item['icon'], (50, 50))
                    ), Layout.Left,
                    await Layout.vertical().init(
                        items=[
                            await Label(self, 'TitleLbl').init(
                                text=item['title'], elide=Label.ElideRight, hpolicy=Label.Expanding
                            ),
                            await Label(self, 'DescriptionLbl').init(
                                text=item['description'], elide=Label.ElideRight, hpolicy=Label.Expanding
                            ),
                        ]
                    )
                ]
            )
        )
        return self
