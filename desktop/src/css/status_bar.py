from ..misc import COLORS


css: str = f'''
#StatusBar {{
    background-color: {COLORS.STATUS};
}}

#StorageLbl {{
    color: white;
    background-color: {COLORS.TRANSPARENT};
    font-size: 12px;
}}

#StorageSelector QAbstractItemView {{
    border: none;
    color: white;
    background-color: {COLORS.RIGHT_MENU};
}}

#StorageSelector {{
    min-width: 75px;
    border: none;
    font-size: 12px;
    font-weight: bold;
    color: white;
    background-color: {COLORS.TRANSPARENT};
}}
'''
