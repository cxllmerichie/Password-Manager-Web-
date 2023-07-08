from aioqui.types import Size, Icon
from PySide6.QtCore import QSize
import os


class PATHS:
    ASSETS = os.path.abspath('.assets')
    ICONS = os.path.join(ASSETS, 'icons')


class EXTENSIONS:
    ICON = 'jpg'
    TEXT = 'txt'


class PALETTE:
    # LAYER_2 = '#17212B'
    LAYER_2 = 'rgba(14 ,14, 14, 1)'
    LAYER_3 = 'rgba(155, 24, 223, 1)'
    LAYER_4 = 'rgba(88, 143, 242, 1)'


class COLORS:
    Palette = PALETTE
    TRANSPARENT = 'transparent'
    LIGHT = PALETTE.LAYER_4
    DARK = PALETTE.LAYER_3
    RED = 'rgba(182, 0, 40, 1)'
    RED_HOVER = 'rgba(182, 0, 40, 0.5)'
    INPUT = 'rgba(27, 29, 40, 0.5)'
    GREEN = 'darkgreen'
    GREEN_HOVER = 'rgba(0, 255, 0, 0.5)'
    HOVER = 'rgba(255, 255, 255, 0.1)'
    BUTTON = 'rgba(255, 255, 255, 0.2)'
    SEARCH_ITEM = PALETTE.LAYER_4.replace('1)', '0.5)')
    SEARCH_CATEGORY = PALETTE.LAYER_3.replace('1)', '0.5)')

    SIGNIN = PALETTE.LAYER_2
    SIGNUP = PALETTE.LAYER_2

    PANEL = STATUS = 'rgba(14, 14, 14, 1)'
    LEFT_MENU = RIGHT_MENU = 'rgba(14, 14, 14, 0.5)'

    TEXT_PRIMARY = 'white'
    TEXT_SECONDARY = 'rgba(255, 255, 255, 0.7)'
    TEXT_ALERT = 'red'


class SIZES:
    CONTROL = Size(40, 40)
    App = QSize(800, 600)
    AuthTextBtn = Size(..., 20)
    AuthMainBtn = Size(200, 30)
    AuthInputLabel = Size(..., 25)
    AuthInputField = Size(300, 25)
    NoCategoriesLbl = QSize(150, 50)
    StatusBarLbl = Size(..., 20)
    PanelNavigationBtn = Size(30, 30)
    Panel = Size(..., 30)
    CATEGORY = Size(300, ...)
    ERROR = Size(300, 50)

    RightMenuMin = 400
    RightMenuMax = 800
    RightMenuFix = 400

    MenuBtnIcon = Size(30, 30)
    RightMenuImage = Size(80, 80)

    LeftMenuFix = 300
    LeftMenuMin = 250
    LeftMenuMax = 400

    LeftMenuLettersMargin = 18, 0, 0, 0
    LeftMenuTitlesMargin = 0, 20, 0, 10
    CentralPagesLettersMargin = 18, 0, 0, 0


class ICONS:
    APP = Icon(os.path.join(PATHS.ASSETS, 'icon.png'), (25, 25))
    MINIMIZE = Icon('minus.svg', (25, 25))
    RESTORE = Icon('square.svg', (20, 20))
    CROSS = Icon('x.svg', (27, 27))
    HOME = Icon('home.svg', SIZES.MenuBtnIcon.size)
    STAR = Icon('star.svg', SIZES.MenuBtnIcon.size)
    STAR_FILL = Icon('star-fill.svg', (20, 20))
    MENU = Icon('menu.svg', (25, 25))
    PLUS = Icon('plus-circle.svg', (20, 20))
    EDIT = Icon('edit.svg', (30, 30))
    CROSS_CIRCLE = Icon('x-circle.svg', (20, 20))
    SAVE = Icon('check-circle.svg', (20, 20))
    DOWNLOAD = Icon('save.svg', (20, 20))
    TRASH = Icon('trash-2.svg', (20, 20))
    COPY = Icon('copy.svg', (20, 20))
    EYE = Icon('eye.svg', (20, 20))
    EYE_OFF = Icon('eye-off.svg', (20, 20))
    CATEGORY = Icon('tag.svg', SIZES.RightMenuImage.size)
    ITEM = Icon('archive.svg', SIZES.RightMenuImage.size)
    EXPORT = Icon('arrow-up-circle.svg', (20, 20))
    IMPORT = Icon('arrow-down-circle.svg', (20, 20))
    LOGOUT = Icon('log-out.svg', (18, 18))
