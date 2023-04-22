from ..misc import SIZES, COLORS


css: str = f'''
#Panel {{
    background-color: {COLORS.PANEL};
    min-height: {SIZES.Panel.h}px;
    max-height: {SIZES.Panel.h}px;
}}

#ToggleLeftMenuBtn {{
    background-color: {COLORS.TRANSPARENT};
}}

#ToggleLeftMenuBtn:hover {{
    background-color: {COLORS.LIGHT_GRAY};
}}

#PanelMinimizeBtn,
#PanelRestoreBtn,
#PanelCloseBtn {{
    border: none;
    background-color: {COLORS.TRANSPARENT};
}}

#PanelMinimizeBtn:hover,
#PanelRestoreBtn:hover {{
    background-color: {COLORS.LIGHT_GRAY};
}}

#PanelCloseBtn:hover {{
    background-color: {COLORS.RED};
}}

#PanelTitleLbl {{
    color: {COLORS.TEXT_PRIMARY};
    font-size: 16px;
    font-weight: bold;
}}
'''
