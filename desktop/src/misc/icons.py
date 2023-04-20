from qcontextapi.utils import Icon

from .sizes import Sizes


class Icons:
    APP = Icon('icon.png', (25, 25))
    MINIMIZE = Icon('minus.svg', (25, 25))
    RESTORE = Icon('square.svg', (20, 20))
    CROSS = Icon('x.svg', (27, 27))
    HOME = Icon('home.svg', Sizes.MenuBtnIcon.size)
    STAR = Icon('star.svg', Sizes.MenuBtnIcon.size)
    STAR_FILL = Icon('star-fill.svg', (20, 20))
    MENU = Icon('menu.svg', (25, 25))
    PLUS = Icon('plus-circle.svg', (20, 20))
    EDIT = Icon('edit.svg', (30, 30))
    CROSS_CIRCLE = Icon('x-circle.svg', (20, 20))
    SAVE = Icon('save.svg', (20, 20))
    TRASH = Icon('trash-2.svg', (20, 20))
    COPY = Icon('copy.svg', (20, 20))
    EYE = Icon('eye.svg', (20, 20))
    EYE_OFF = Icon('eye-off.svg', (20, 20))
    CATEGORY = Icon('tag.svg', Sizes.RightMenuImage.size)
    ITEM = Icon('archive.svg', Sizes.RightMenuImage.size)

