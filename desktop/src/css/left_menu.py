from ..const import Colors


css = f'''
#LeftMenu {{
    background-color: {Colors.FOREGROUND};    
}}

#LeftMenuItemsLabel,
#LeftMenuCategoriesLabel {{
    font-size: 20px;
    color: white;
}}

#CountableButtonIcon {{
    background-color: transparent;
}}

#CountableButtonLbl {{
    background-color: transparent;
    font-size: 16px;
    min-width: 110px;
    color: white;
}}

#CountableButtonCountLbl {{
    background-color: transparent;
    font-size: 14px;
    color: white;
    border: 1px solid white;
    border-radius: 5px;
    min-width: 30px;
    max-height: 18px;
}}

#CountableButton {{
    background-color: {Colors.BACKGROUND};
    min-width: 200px;
    min-height: 30px;
    color: white;
    font-size: 20px;
    height: 25px;
    border: none;
}}

#CountableButton:hover {{
    background-color: {Colors.MAINRED};
}}

#NoCategoriesLbl {{
    color: white;
    font-size: 14px;
    font-style: italic;
}}

#CategoriesScrollArea {{
    background-color: transparent;
    border: none;
}}

#CategoriesScrollAreaWidget {{
    background-color: transparent;
    border: none;
}}

QScrollBar:vertical {{
    background: white;
    width: 7px;
    border: none;
    border-radius: 3px;
    margin: 0px 0 1px 0;
}}

QScrollBar::handle:vertical {{
    background: {Colors.MAINRED};
    border-radius: 3px;
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
