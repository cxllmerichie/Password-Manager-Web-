from qcontextapi.misc import Size, Icon
from PyQt5.QtCore import QSize


class PATHS:
    ICONS = 'icons'


class EXTENSIONS:
    ICON = 'jpg'
    TEXT = 'txt'


class PALETTE:
    LAYER_1 = '#0E1621'
    LAYER_2 = '#17212B'
    LAYER_3 = '#242F3D'
    LAYER_4 = ''
    LAYER_5 = '#023535'
    LAYER_6 = '#008F8C'
    LAYER_7 = '#3E546A'


class COLORS:
    Palette = PALETTE
    TRANSPARENT = 'transparent'
    LIGHT = PALETTE.LAYER_6
    DARK = PALETTE.LAYER_5
    RED = 'rgba(182, 0, 40, 1)'
    RED_HOVER = 'rgba(182, 0, 40, 0.5)'
    INPUT = 'rgba(27, 29, 40, 0.5)'
    GREEN = 'darkgreen'
    GREEN_HOVER = 'rgba(0, 255, 0, 0.5)'
    HOVER = 'rgba(255, 255, 255, 0.1)'
    BUTTON = 'rgba(255, 255, 255, 0.2)'
    SEARCH = PALETTE.LAYER_3

    SIGNIN = PALETTE.LAYER_1
    SIGNUP = PALETTE.LAYER_1

    PANEL = PALETTE.LAYER_3
    STATUS = PALETTE.LAYER_3
    LEFT_MENU = PALETTE.LAYER_2
    RIGHT_MENU = PALETTE.LAYER_2
    CENTRAL = PALETTE.LAYER_1

    TEXT_PRIMARY = 'white'
    TEXT_SECONDARY = 'gray'
    TEXT_ALERT = 'red'


class SIZES:
    CONTROL = QSize(40, 40)
    App = QSize(1000, 600)
    AuthTextBtn = Size(..., 20)
    AuthMainBtn = Size(200, 30)
    AuthInputLabel = Size(..., 25)
    AuthInputField = Size(300, 25)
    NoCategoriesLbl = QSize(150, 50)
    StatusBarLbl = Size(..., 20)
    PanelNavigationBtn = QSize(30, 30)
    Panel = Size(..., 30)
    CATEGORY = Size(300, ...)
    ERROR = Size(300, 50)
    RightMenuMin = Size(400, ...)
    RightMenuMax = Size(800, ...)
    RightMenuDefault = Size(400, ...)
    MenuBtnIcon = Size(30, 30)
    RightMenuImage = Size(80, 80)
    LeftMenuMin = 250
    LeftMenuMax = 400
    LeftMenuLettersMargin = 18, 0, 0, 0
    LeftMenuTitlesMargin = 0, 20, 0, 10
    CentralPagesLettersMargin = 18, 0, 0, 0


class ICONS:
    APP = Icon('icon.png', (25, 25))
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
