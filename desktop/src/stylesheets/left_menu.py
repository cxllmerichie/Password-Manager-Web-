from ..misc import COLORS


css = f'''
#FavouriteLbl,
#LetterLbl {{
    color: {COLORS.TEXT_PRIMARY};
    font-size: 16px;
    font-weight: bold;
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

#AllItemsBtnIconBtn,
#FavItemsBtnIconBtn,
#MenuButtonIconBtn {{
    background-color: {COLORS.TRANSPARENT};
}}

#AllItemsBtnTextLbl,
#FavItemsBtnTextLbl,
#MenuButtonTextLbl {{
    background-color: {COLORS.TRANSPARENT};
    font-size: 20px;
    color: {COLORS.TEXT_PRIMARY};
}}

#AllItemsBtnTotalLbl,
#FavItemsBtnTotalLbl,
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
    background-color: {COLORS.DARK};
    min-height: 40px;
    color: {COLORS.TEXT_PRIMARY};
    height: 25px;
    border: none;
}}

#AllItemsBtn,
#FavItemsBtn {{
    background-color: {COLORS.LIGHT};
    min-height: 40px;
    color: {COLORS.TEXT_PRIMARY};
    height: 25px;
    border: none;
}}

#AllItemsBtn:hover,
#FavItemsBtn:hover,
#MenuButton:hover {{
    background-color: {COLORS.HOVER};
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
