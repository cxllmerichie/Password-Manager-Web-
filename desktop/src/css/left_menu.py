from ..assets import Color


css = f'''
#LeftMenu {{
    background-color: {Color.FOREGROUND};    
}}

#LeftMenuCategoriesLabel {{

}}

#CountableButtonIcon {{
    background-color: transparent;
}}

#CountableButtonLbl {{
    background-color: transparent;
    font-size: 20px;
    min-width: 120px;
    color: white;
}}

#CountableButtonCountLbl {{
    background-color: transparent;
    font-size: 18px;
    color: white;
    border: 1px solid white;
    border-radius: 5px;
    min-width: 30px;
}}

#CountableButton {{
    background-color: transparent;
    min-width: 180px;
    color: white;
    font-size: 20px;
    height: 25px;
    border: none;
}}

#CountableButton:hover {{
    background-color: {Color.FOREGROUND};
}}
'''
