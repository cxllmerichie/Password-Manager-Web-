from aioqui.widgets.custom.qss.colors import gradient

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

#ItemsLbl,
#CategoriesLbl {{
    font-size: 20px;
    color: {COLORS.TEXT_PRIMARY};
    font-weight: bold;
}}

#AllItemsBtnIconBtn,
#FavItemsBtnIconBtn,
#TotalButtonIconBtn {{
    background-color: {COLORS.TRANSPARENT};
}}

#AllItemsBtnTextLbl,
#FavItemsBtnTextLbl,
#TotalButtonTextLbl {{
    background-color: {COLORS.TRANSPARENT};
    font-size: 20px;
    color: {COLORS.TEXT_PRIMARY};
}}

#AllItemsBtnTotalLbl,
#FavItemsBtnTotalLbl,
#TotalButtonTotalLbl {{
    background-color: {COLORS.TRANSPARENT};
    font-size: 14px;
    color: {COLORS.TEXT_PRIMARY};
    border: 1px solid white;
    border-radius: 5px;
    min-width: 30px;
    max-height: 18px;
}}

#TotalButton {{
    background: {gradient(p1=(0, 1), p2=(1, 1), c1=COLORS.DARK, c2=COLORS.TRANSPARENT)};
    min-height: 40px;
    color: {COLORS.TEXT_PRIMARY};
    height: 25px;
    border: none;
}}

#AllItemsBtn,
#FavItemsBtn {{
    background-color: {gradient(p1=(0, 1), p2=(1, 1), c1=COLORS.LIGHT, c2=COLORS.TRANSPARENT)};
    min-height: 40px;
    color: {COLORS.TEXT_PRIMARY};
    height: 25px;
    border: none;
}}

#AllItemsBtn:hover,
#FavItemsBtn:hover,
#TotalButton:hover {{
    background-color: {COLORS.HOVER};
}}

#NoCategoriesLbl {{
    color: {COLORS.TEXT_PRIMARY};
    font-size: 14px;
    font-style: italic;
    max-width: 100px;
}}

#ScrollArea {{
    background-color: {COLORS.TRANSPARENT};
    border: none;
}}

#ScrollAreaWidget {{
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
