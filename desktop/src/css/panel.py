from ..misc import Sizes, Colors


css: str = f'''
#Panel {{
    background-color: {Colors.PANEL};
    min-height: {Sizes.Panel.h}px;
    max-height: {Sizes.Panel.h}px;
}}

#ToggleLeftMenuBtn {{
    background-color: {Colors.TRANSPARENT};
}}

#ToggleLeftMenuBtn:hover {{
    background-color: {Colors.LIGHT_GRAY};
}}

#PanelMinimizeBtn,
#PanelRestoreBtn,
#PanelCloseBtn {{
    border: none;
    background-color: {Colors.TRANSPARENT};
}}

#PanelMinimizeBtn:hover,
#PanelRestoreBtn:hover {{
    background-color: {Colors.LIGHT_GRAY};
}}

#PanelCloseBtn:hover {{
    background-color: {Colors.RED};
}}

#PanelTitleLbl {{
    color: {Colors.TEXT_PRIMARY};
    font-size: 16px;
    font-weight: bold;
}}
'''
