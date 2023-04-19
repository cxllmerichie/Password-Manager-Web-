from ..misc import Colors


css = f'''
#LeftMenu {{
    background-color: {Colors.LEFT_MENU};
}}

#LeftMenuItemsLabel,
#LeftMenuCategoriesLabel {{
    font-size: 20px;
    color: {Colors.TEXT_PRIMARY};
}}

#MenuButtonIconBtn {{
    background-color: {Colors.TRANSPARENT};
}}

#MenuButtonTextLbl {{
    background-color: {Colors.TRANSPARENT};
    font-size: 16px;
    min-width: 110px;
    color: {Colors.TEXT_PRIMARY};
}}

#MenuButtonTotalLbl {{
    background-color: {Colors.TRANSPARENT};
    font-size: 14px;
    color: {Colors.TEXT_PRIMARY};
    border: 1px solid white;
    border-radius: 5px;
    min-width: 30px;
    max-height: 18px;
}}

#MenuButton {{
    background-color: {Colors.LIGHT_GRAY};
    min-width: 200px;
    max-width: 200px;
    min-height: 30px;
    color: {Colors.TEXT_PRIMARY};
    font-size: 20px;
    height: 25px;
    border: none;
}}

#MenuButton:hover {{
    background-color: {Colors.RED};
}}

#NoCategoriesLbl {{
    color: {Colors.TEXT_PRIMARY};
    font-size: 14px;
    font-style: italic;
}}

#CategoriesScrollArea {{
    background-color: {Colors.TRANSPARENT};
    border: none;
}}

#CategoriesScrollAreaWidget {{
    background-color: {Colors.TRANSPARENT};
    border: none;
}}

#AddCategoryBtn {{
    color: {Colors.TEXT_PRIMARY};
    background-color: {Colors.TRANSPARENT};
    font-size: 14px;
    max-width: 200px;
    border: none;
    min-height: 30px;
}}

#AddCategoryBtn:hover {{
    background-color: {Colors.HOVER};
}}
'''
