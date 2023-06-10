from ..misc import SIZES, COLORS


css: str = f'''
#Panel {{
    background-color: {COLORS.PANEL};
    min-height: {SIZES.Panel.h}px;
    max-height: {SIZES.Panel.h}px;
}}

#ToggleMenuBtn {{
    background-color: {COLORS.TRANSPARENT};
}}

#ToggleMenuBtn:hover {{
    background-color: {COLORS.LIGHT};
}}

#MinimizeBtn,
#RestoreBtn,
#CloseBtn {{
    border: none;
    background-color: {COLORS.TRANSPARENT};
}}

#MinimizeBtn:hover,
#RestoreBtn:hover {{
    background-color: {COLORS.LIGHT};
}}

#CloseBtn:hover {{
    background-color: {COLORS.RED};
}}

#TitleLbl {{
    color: {COLORS.TEXT_PRIMARY};
    font-size: 16px;
    font-weight: bold;
}}
'''
