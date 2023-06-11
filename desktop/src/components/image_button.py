from aioqui.widgets.custom import ImageButton as ImageButtonBase


class ImageButton(ImageButtonBase):
    default: bool = False

    async def init(
            self, *,
            on_success=lambda: None, directory='',
            **kwargs
    ) -> 'ImageButton':
        if kwargs.get('icon'):
            self.default = True
        return await super().init(on_success=on_success, directory=directory, **kwargs)

    @property
    def bytes(self):
        if self.default:
            return None
        return super().bytes

    def setIcon(self, icon) -> None:
        self.default = False
        return super().setIcon(icon)
