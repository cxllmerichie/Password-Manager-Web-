from ..misc import SIZES, COLORS


css: str = f'''
#Panel {{
    background-color: {COLORS.PANEL};
    min-height: {SIZES.Panel.h}px;
    max-height: {SIZES.Panel.h}px;
}}

#MinimizeBtn,
#RestoreBtn,
#CloseBtn {{
    border: none;
    background-color: {COLORS.TRANSPARENT};
}}

#ToggleMenuBtn {{
    background-color: {COLORS.TRANSPARENT};
}}

#ToggleMenuBtn:hover,
#MinimizeBtn:hover,
#RestoreBtn:hover {{
    background-color: {COLORS.HOVER};
}}

#CloseBtn:hover {{
    background-color: {COLORS.RED};
}}

#TitleImg,
#TitleLbl {{
    color: {COLORS.TEXT_PRIMARY};
    font-size: 16px;
    font-weight: bold;
}}

#TitleLbl {{
    padding-left: 5px;
}}
'''
