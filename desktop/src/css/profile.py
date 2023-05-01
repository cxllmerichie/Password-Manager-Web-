from ..misc import COLORS, ICONS, SIZES


css = f'''
QComboBox QAbstractItemView {{
    border: none;
    color: white;
    background-color: {COLORS.RIGHT_MENU};
}}

#StorageSelector {{
    border: none;
    font-size: 16px;
    font-weight: bold;
    color: white;
    background-color: {COLORS.TRANSPARENT};
}}

#Profile {{
    
}}

#ImageButton {{
    background-color: {COLORS.TRANSPARENT};
}}

#ProfileEmailLbl {{
    color: white;
    font-weight: bold;
    font-size: 20px;
}}

#ProfileFrame {{
    background-color: {COLORS.TRANSPARENT};
}}

#StorageLbl {{
    color: white;
    font-size: 16px;
}}
'''
