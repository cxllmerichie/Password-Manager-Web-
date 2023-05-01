from qcontextapi.widgets import Frame, Widget, Layout, Button, Label, Selector
from qcontextapi.customs import ImageButton
from qcontextapi.utils import Icon
from qcontextapi import CONTEXT

from ..misc import API
from .. import css


class Profile(Frame):
    def __init__(self, parent: Widget):
        super().__init__(parent, self.__class__.__name__, stylesheet=css.profile.css)

    def init(self) -> 'Profile':
        user = API.current_user()
        self.setLayout(Layout.vertical().init(
            items=[
                Frame(self, 'ProfileFrame').init(
                    layout=Layout.vertical().init(
                        alignment=Layout.TopCenter,
                        items=[
                            ImageButton(self).init(
                                icon=Icon(user['avatar'], (80, 80))
                            ),
                            Label(self, 'ProfileEmailLbl').init(
                                text=user['email']
                            ),
                            Layout.horizontal().init(
                                items=[
                                    Label(self, 'StorageLbl').init(
                                        text='Storage:'
                                    ),

                                ]
                            )
                        ]
                    )
                )
            ]
        ))
        return self

    def show_profile(self):
        CONTEXT.CentralPages.setCurrentWidget(CONTEXT.Profile)
