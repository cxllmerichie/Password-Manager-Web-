from ..assets import Icon, Size, Colors


css: str = f'''
#Panel {{
    background-color: {Colors.FOREGROUND};
    min-height: 30px;
}}

#ToggleLeftMenuBtn {{
    background-color: transparent;
}}

#ToggleLeftMenuBtn:hover {{
    background-color: {Colors.BACKGROUND};
}}

#PanelMinimizeBtn,
#PanelRestoreBtn,
#PanelCloseBtn {{
    border: none;
    background-color: transparent;
}}

#PanelMinimizeBtn:hover,
#PanelRestoreBtn:hover {{
    background-color: {Colors.BACKGROUND};
}}

#PanelCloseBtn:hover {{
    background-color: {Colors.MAINRED};
}}

#PanelTitleLbl {{
    color: white;
    font-size: 16px;
    font-weight: bold;
}}
'''
