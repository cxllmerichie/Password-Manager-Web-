from aioqui.widgets import Frame, Label, Layout, Parent


class LabelExtended(Frame):
    def __init__(self, parent: Parent, name: str, visible: bool = True):
        Frame.__init__(self, parent, f'{name}Frame', visible)
        self.__name = name

    async def init(
            self, *,
            text: str = '', margins: tuple[int, ...] = (0, 0, 0, 0)
    ) -> 'LabelExtended':
        await super().init(layout=await Layout.horizontal().init(
            margins=margins,
            items=[
                label := await Label(self.parent(), self.__name).init(
                    text=text
                )
            ]
        ))
        self.label = label
        return self
