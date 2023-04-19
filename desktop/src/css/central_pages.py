from ..misc import Colors


css: str = f'''
#CentralPages {{
    background-color: transparent;
}}
'''

cp_items = f'''
#CP_Items {{
    background-color: {Colors.CENTRAL};
    border: none;
}}

#CP_ItemsWidget {{
    background-color: transparent;
}}

#FavouriteLbl,
#LetterLbl {{
    color: white;
    font-size: 20px;
    font-weight: bold;
}}
'''

cp_item = f'''
#CP_Item {{
    background-color: {Colors.LIGHT_GRAY};
    border-radius: 10px;
    min-height: 75px;
    min-width: 200px;
}}

#ItemTitleLbl {{
    color: white;
    font-size: 22px;
}}

#ItemDescriptionLbl {{
    color: gray;
    font-size: 18px;
}}
'''
