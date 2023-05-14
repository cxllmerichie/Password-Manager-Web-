from aioqui.widgets import Layout, Label, Frame, Parent
from aioqui.types import Icon
from aioqui import CONTEXT
from typing import Any

from .. import stylesheets


class CentralItem(Frame):
    def __init__(self, parent: Parent):
        super().__init__(parent, self.__class__.__name__, stylesheet=stylesheets.central_item.css)

    async def init(self, item: dict[str, Any]) -> 'CentralItem':
        await super().init(
            events=Frame.Events(on_click=lambda: CONTEXT.RightPagesItem.show_item(item)),
            layout=await Layout.horizontal(self, 'ItemLayout').init(
                margins=(10, 10, 10, 10), alignment=Layout.Left, spacing=20,
                items=[
                    await Label(self, 'ItemIconLbl').init(
                        icon=Icon(item['icon'], (50, 50))
                    ), Layout.Left,
                    await Layout.vertical().init(
                        items=[
                            await Label(self, 'ItemTitleLbl').init(
                                text=item['title'], elide=Label.ElideRight,
                                sizes=Label.Sizes(hpolicy=Label.Expanding)
                            ),
                            await Label(self, 'ItemDescriptionLbl').init(
                                text=item['description'], elide=Label.ElideRight,
                                sizes=Label.Sizes(hpolicy=Label.Expanding)
                            )
                        ]
                    )
                ]
            )
        )
        return self
