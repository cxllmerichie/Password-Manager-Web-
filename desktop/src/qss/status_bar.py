from ..misc import COLORS


css: str = f'''
QStatusBar::item {{
    border: none;
}}

#StatusBar {{
    background-color: {COLORS.STATUS};
    min-height: 25px;
}}

#StorageLbl {{
    color: white;
    background-color: {COLORS.TRANSPARENT};
    font-size: 14px;
}}

#StorageSelector QAbstractItemView {{
    border: none;
    color: white;
    background-color: {COLORS.RIGHT_MENU};
}}

#StorageSelector {{
    min-width: 65px;
    border: none;
    font-size: 14px;
    font-weight: bold;
    color: white;
    background-color: {COLORS.TRANSPARENT};
}}

#LogoutBtn {{
    background-color: {COLORS.TRANSPARENT};
    font-size: 14px;
    color: white;
    min-height: 20px;
}}

#LogoutBtn:hover {{
    background-color: {COLORS.RED_HOVER};
}}
'''
