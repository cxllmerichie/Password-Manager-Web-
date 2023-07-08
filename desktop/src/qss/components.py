from aioqui.widgets.custom.qss.colors import gradient

from ..misc import COLORS, SIZES


scroll: str = f'''
QScrollBar:vertical {{
    background: {COLORS.TRANSPARENT};
    width: 7px;
    border: none;
    border-radius: 3px;
    margin: REPLACEpx 0px 1px 0px;
}}

QScrollBar::handle:vertical {{
    background: {gradient(p1=(0, 1), p2=(1, 1), c1=COLORS.TRANSPARENT, c2=COLORS.RED_HOVER)};
    border-radius: 3px;
}}

QScrollBar::handle:vertical:hover {{
    background: {gradient(p1=(0, 1), p2=(1, 1), c1=COLORS.TRANSPARENT, c2=COLORS.RED)};
}}

QScrollBar::add-line:vertical {{
    height: 0px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}}

QScrollBar::sub-line:vertical {{
    height: 0px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {{
    background: none;
}}
'''


def image_button(color=COLORS.LIGHT):
    return f'''
        #ImageBtn {{
            background-color: {color};
            min-width: 120px;
            min-height: 120px;
            border-radius: 59px;
            border: none;
        }}
        '''


search = f'''
#SearchBar {{
    background: {COLORS.TRANSPARENT};
    font-size: 18px;
    padding: 5px;
    color: {COLORS.TEXT_PRIMARY};
    border: 1px solid REPLACE;
    border-radius: 5px;
}}

#SearchBarPopup {{
    background-color: {COLORS.Palette.LAYER_2};
    border: none;
    font-size: 20px;
    font-weight: bold;
    color: {COLORS.TEXT_SECONDARY};
}}

QListView::item:hover {{
    background-color: {COLORS.HOVER};
    color: {COLORS.TEXT_PRIMARY};
}}
'''

intro_popup = f'''
#IntroPopupFrame {{
    background-color: {COLORS.HOVER};
}}

#StorageLbl {{
    font-weight: bold;
    color: white;
    font-size: 28px;
}}

#HintLbl1 {{
    color: white;
    font-size: 20px;
}}

#HintLbl2 {{
    color: white;
    font-size: 16px;
}}

#ContinueBtn {{
    min-width: {SIZES.AuthMainBtn.w}px;
    height: {SIZES.AuthMainBtn.h}px;
    font-size: 20px;
    font-weight: bold;
    background-color: {COLORS.RED};
    color: white;
}}

#ContinueBtn:hover  {{
    background-color: {COLORS.RED_HOVER};
}}

#AuthExitBtn {{
    background-color: {COLORS.TRANSPARENT};
    border: none;    
}}

#AuthExitBtn:hover {{
    background-color: {COLORS.RED_HOVER};
}}

'''

common_button = f'''
    border: none;
    min-height: 50px;
    color: white;
    font-size: 20px;
    min-width: 400px;
'''

active_button = f'''
#StorageBtn {{
    {common_button}
    background-color: {COLORS.RED};
}}

#StorageBtn: hover {{
    background-color: {COLORS.RED_HOVER};
}}
'''

inactive_button = f'''
#StorageBtn {{
    {common_button}
    background-color: gray;
}}

#StorageBtn:hover {{
    background-color: {COLORS.HOVER};
}}
'''

popup = f'''
#Popup {{
    background-color: {COLORS.HOVER};
}}

#PopupFrame {{
    background-color: {COLORS.LEFT_MENU};
    min-width: 400px;
    min-height: 200px;
    border-radius: 20px;
}}

#PopupMessageLbl {{
    color: white;
    font-size: 24px;
    background-color: {COLORS.TRANSPARENT};
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
    background-color: {COLORS.GREEN};
}}

#PopupYesBtn:hover {{
    background-color: {COLORS.GREEN_HOVER};
}}

#PopupNoBtn {{
    background-color: {COLORS.RED};
}}

#PopupNoBtn:hover {{
    background-color: {COLORS.RED_HOVER};
}}
'''
