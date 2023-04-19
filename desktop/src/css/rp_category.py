from ..misc import Colors, Sizes


css: str = f'''
#SaveBtn {{
    background-color: {Colors.GREEN};
}}

#SaveBtn:hover {{
    background-color: {Colors.GREEN_HOVER};
}}

#CancelBtn {{
    background-color: {Colors.RED};
}}

#CancelBtn:hover {{
    background-color: {Colors.RED_HOVER};
}}

#SaveBtn,
#CancelBtn {{
    color: white;
    font-size: 16px;
    min-width: 100px;
    min-height: 30px;
    font-size: 16px;
    border: none;
    font-weight: bold;
}}

#CreateBtn {{
    background-color: green;
    color: white;
    min-width: 200px;
    min-height: 30px;
    font-size: 16px;
    border: none;
    font-weight: bold;
}}

#CreateBtn:hover {{
    background-color: rgba(0, 255, 0, 0.2);
}}

#IconBtn {{
    background-color: {Colors.DARK_GRAY};
    min-width: 120px;
    max-width: 120px;
    min-height: 120px;
    max-height: 120px;
    border-radius: 59px;
    border: none;
}}

#TitleInput,
#DescriptionInput {{
    border: none;
    background-color: {Colors.DARK_GRAY};
    max-width: {Sizes.CATEGORY.w}px;
    min-width: {Sizes.CATEGORY.w}px;
    color: white;
    font-size: 18px;
    padding: 5px;
    border-radius: 5px;
}} 

#DescriptionInput {{
    max-height: 100px;
}}

#RemoveBtn,
#EditBtn,
#FavouriteBtn,
#CloseBtn {{
    background-color: transparent;
}}

#ControlBtns {{
    max-width: {Sizes.CATEGORY.w}px;
}}

#ErrorLbl {{
    color: red;
    font-size: 16px;
    min-width: {Sizes.ERROR.w}px;
    min-height: {Sizes.ERROR.h}px;
}}

#AddItemBtn {{
    color: white;
    background-color: transparent;
    font-size: 14px;
    min-width: 200px;
    border: none;
    min-height: 30px;
}}

#AddItemBtn:hover {{
    background-color: rgba(255, 255, 255, 0.1);
}}
'''
