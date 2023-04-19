from ..misc import Colors, Sizes


css: str = f'''
#CategoryFrame {{
    background-color: {Colors.RIGHT_MENU};
}}

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
    color: {Colors.TEXT_PRIMARY};
    min-width: 100px;
    min-height: 30px;
    font-size: 16px;
    border: none;
    font-weight: bold;
}}

#CreateBtn {{
    background-color: {Colors.GREEN};
    color: {Colors.TEXT_PRIMARY};
    min-width: 200px;
    min-height: 30px;
    font-size: 16px;
    border: none;
    font-weight: bold;
}}

#CreateBtn:hover {{
    background-color: {Colors.GREEN_HOVER};
}}

#TitleInput,
#DescriptionInput {{
    border: none;
    background-color: {Colors.LIGHT_GRAY};
    min-width: {Sizes.CATEGORY.w}px;
    color: {Colors.TEXT_PRIMARY};
    font-size: 18px;
    padding: 5px;
    border-radius: 5px;
}} 

#DescriptionInput {{
    max-height: 600px;
}}

#DeleteBtn,
#EditBtn,
#FavouriteBtn,
#CloseBtn {{
    background-color: {Colors.TRANSPARENT};
}}

#ControlBtns {{
}}

#ErrorLbl {{
    color: {Colors.TEXT_ALERT};
    font-size: 16px;
    min-width: {Sizes.ERROR.w}px;
    min-height: {Sizes.ERROR.h}px;
}}

#AddItemBtn {{
    color: {Colors.TEXT_PRIMARY};
    background-color: {Colors.TRANSPARENT};
    font-size: 14px;
    min-width: 200px;
    border: none;
    min-height: 30px;
}}

#AddItemBtn:hover {{
    background-color: {Colors.HOVER};
}}
'''
