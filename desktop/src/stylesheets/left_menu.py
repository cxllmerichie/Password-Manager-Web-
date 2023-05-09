from ..misc import COLORS


css = f'''
#FavouriteLbl,
#LetterLbl {{
    color: {COLORS.TEXT_PRIMARY};
    font-size: 16px;
}}

#LeftMenu {{
    background-color: {COLORS.LEFT_MENU};
}}

#LeftMenuItemsLabel,
#LeftMenuCategoriesLabel {{
    font-size: 20px;
    color: {COLORS.TEXT_PRIMARY};
    font-weight: bold;
}}

#MenuButtonIconBtn {{
    background-color: {COLORS.TRANSPARENT};
}}

#MenuButtonTextLbl {{
    background-color: {COLORS.TRANSPARENT};
    font-size: 20px;
    color: {COLORS.TEXT_PRIMARY};
}}

#MenuButtonTotalLbl {{
    background-color: {COLORS.TRANSPARENT};
    font-size: 14px;
    color: {COLORS.TEXT_PRIMARY};
    border: 1px solid white;
    border-radius: 5px;
    min-width: 30px;
    max-height: 18px;
}}

#MenuButton {{
    background-color: {COLORS.LIGHT_GRAY};
    min-height: 40px;
    color: {COLORS.TEXT_PRIMARY};
    height: 25px;
    border: none;
}}

#MenuButton:hover {{
    background-color: {COLORS.RED};
}}

#NoCategoriesLbl {{
    color: {COLORS.TEXT_PRIMARY};
    font-size: 14px;
    font-style: italic;
    max-width: 100px;
}}

#CategoriesScrollArea {{
    background-color: {COLORS.TRANSPARENT};
    border: none;
}}

#CategoriesScrollAreaWidget {{
    background-color: {COLORS.TRANSPARENT};
    border: none;
}}

#AddCategoryBtn {{
    color: {COLORS.TEXT_PRIMARY};
    background-color: {COLORS.TRANSPARENT};
    font-size: 14px;
    border: none;
    min-height: 30px;
}}

#AddCategoryBtn:hover {{
    background-color: {COLORS.HOVER};
}}
'''
