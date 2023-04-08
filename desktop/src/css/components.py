from ..misc import Colors, Sizes


scroll: str = f'''
QScrollBar:vertical {{
    background: white;
    width: 7px;
    border: none;
    border-radius: 3px;
    margin: 0px 0 1px 0;
}}

QScrollBar::handle:vertical {{
    background: {Colors.RED};
    border-radius: 3px;
}}

QScrollBar::handle:vertical:hover {{
    background: {Colors.RED_HOVER};
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
