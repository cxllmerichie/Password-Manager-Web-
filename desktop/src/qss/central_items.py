from ..misc import COLORS


css = f'''
#CentralItems {{
    background-color: {COLORS.TRANSPARENT};
    min-width: 300px;
}}

#HintLbl1,
#NoCategoriesLbl {{
    color: {COLORS.TEXT_PRIMARY};
    font-size: 20px;
    font-style: italic;
}}

#ScrollArea {{
    background-color: {COLORS.TRANSPARENT};
    border: none;
}}

#ScrollAreaWidget {{
    background-color: {COLORS.TRANSPARENT};
}}

#FavouriteLbl,
#LetterLbl {{
    color: {COLORS.TEXT_PRIMARY};
    font-size: 20px;
    font-weight: bold;
}}
'''
