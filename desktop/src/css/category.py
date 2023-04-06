from ..misc import Colors, Sizes


css: str = f'''
#MainBtn {{
    background-color: green;
    color: white;
    font-size: 16px;
    min-width: 200px;
    min-height: 30px;
    border: none;
    font-weight: bold;
}}

#MainBtn:hover {{
    background-color: rgba(0, 255, 0, 0.2);
}}

#IconBtn {{
    background-color: {Colors.BACKGROUND};
    min-width: 120px;
    max-width: 120px;
    min-height: 120px;
    max-height: 120px;
    border-radius: 59px;
    border: none;
}}

#NameInput,
#DescriptionInput {{
    border: none;
    background-color: {Colors.BACKGROUND};
    max-width: 300px;
    min-width: 300px;
    color: white;
    font-size: 18px;
    padding: 5px;
    border-radius: 5px;
}} 


#NameInput {{
}}

#DescriptionInput {{
}}

#FavouriteBtn,
#CloseBtn {{
    background-color: transparent;
}}

#FavouriteBtn {{
}}


#CloseBtn {{
}}

#ControlBtns {{
    max-width: 300px;
}}
'''
