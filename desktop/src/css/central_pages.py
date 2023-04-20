from ..misc import Colors


css: str = f'''
#CentralPages {{
    background-color: {Colors.TRANSPARENT};
}}
'''

cp_items = f'''
#CP_Items {{
    background-color: {Colors.CENTRAL};
    border: none;
}}

#CP_ItemsWidget {{
    background-color: {Colors.TRANSPARENT};
}}

#FavouriteLbl,
#LetterLbl {{
    color: {Colors.TEXT_PRIMARY};
    font-size: 20px;
    font-weight: bold;
}}
'''

cp_item = f'''
#CP_Item {{
    background-color: {Colors.LIGHT_GRAY};
    border-radius: 10px;
    min-height: 75px;
    max-width: 400px;
}}

#ItemTitleLbl {{
    color: {Colors.TEXT_PRIMARY};
    font-size: 22px;
}}

#ItemDescriptionLbl {{
    color: {Colors.TEXT_SECONDARY};
    font-size: 18px;
}}
'''
