from ..misc import Sizes, Colors


css: str = f'''
#Panel {{
    background-color: {Colors.GRAY};
    min-height: {Sizes.Panel.h}px;
}}

#ToggleLeftMenuBtn {{
    background-color: transparent;
}}

#ToggleLeftMenuBtn:hover {{
    background-color: {Colors.DARK_GRAY};
}}

#PanelMinimizeBtn,
#PanelRestoreBtn,
#PanelCloseBtn {{
    border: none;
    background-color: transparent;
}}

#PanelMinimizeBtn:hover,
#PanelRestoreBtn:hover {{
    background-color: {Colors.DARK_GRAY};
}}

#PanelCloseBtn:hover {{
    background-color: {Colors.RED};
}}

#PanelTitleLbl {{
    color: white;
    font-size: 16px;
    font-weight: bold;
}}
'''
