from ..misc import Colors


css = f'''
#LeftMenu {{
    background-color: {Colors.DARK_GRAY};
}}

#LeftMenuItemsLabel,
#LeftMenuCategoriesLabel {{
    font-size: 20px;
    color: white;
}}

#MenuButtonIconBtn {{
    background-color: transparent;
}}

#MenuButtonTextLbl {{
    background-color: transparent;
    font-size: 16px;
    min-width: 110px;
    color: white;
}}

#MenuButtonTotalLbl {{
    background-color: transparent;
    font-size: 14px;
    color: white;
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
    color: white;
    font-size: 20px;
    height: 25px;
    border: none;
}}

#MenuButton:hover {{
    background-color: {Colors.RED};
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

#AddCategoryBtn {{
    color: white;
    background-color: transparent;
    font-size: 14px;
    max-width: 200px;
    border: none;
    min-height: 30px;
}}

#AddCategoryBtn:hover {{
    background-color: rgba(255, 255, 255, 0.1);
}}
'''
