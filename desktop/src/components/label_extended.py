from aioqui.widgets import Frame, Label, Layout, Parent
from aioqui.types import Icon
from PySide6.QtCore import QSize


class LabelExtended(Frame):
    def __init__(self, parent: Parent, name: str, visible: bool = True):
        Frame.__init__(self, parent, f'{name}Frame', visible)
        self.__name = name

    async def init(
            self, *,
            text: str = '', inner_alignment: Label.Alignment = Label.Left, wrap: bool = False, size: QSize = None,
            icon: Icon = None, elided: bool = False, policy: tuple[Label.SizePolicy, Label.SizePolicy] = None,
            margins: tuple[int, ...] = (0, 0, 0, 0), outer_alignment: Layout.Alignment = None
    ) -> 'LabelExtended':
        await super().init(layout=await Layout.horizontal().init(
            margins=margins, alignment=outer_alignment,
            items=[
                label := await Label(self.parent(), self.__name).init(
                    text=text, wrap=wrap, icon=icon, elide=Label.ElideLeft,
                    sizes=Label.Sizes(alignment=inner_alignment, fixed_size=size, policy=policy)
                )
            ]
        ))
        self.label = label
        return self