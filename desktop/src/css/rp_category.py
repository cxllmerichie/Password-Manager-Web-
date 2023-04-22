from ..misc import COLORS, SIZES


css: str = f'''
#SaveBtn {{
    background-color: {COLORS.GREEN};
}}

#SaveBtn:hover {{
    background-color: {COLORS.GREEN_HOVER};
}}

#CancelBtn {{
    background-color: {COLORS.RED};
}}

#CancelBtn:hover {{
    background-color: {COLORS.RED_HOVER};
}}

#SaveBtn,
#CancelBtn {{
    color: {COLORS.TEXT_PRIMARY};
    min-width: 100px;
    min-height: 30px;
    font-size: 16px;
    border: none;
    font-weight: bold;
}}

#CreateBtn {{
    background-color: {COLORS.GREEN};
    color: {COLORS.TEXT_PRIMARY};
    min-width: 200px;
    min-height: 30px;
    font-size: 16px;
    border: none;
    font-weight: bold;
}}

#CreateBtn:hover {{
    background-color: {COLORS.GREEN_HOVER};
}}

#TitleInput,
#DescriptionInput {{
    border: none;
    background-color: {COLORS.LIGHT_GRAY};
    min-width: {SIZES.CATEGORY.w}px;
    color: {COLORS.TEXT_PRIMARY};
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
    background-color: {COLORS.TRANSPARENT};
}}

#ControlBtns {{
}}

#ErrorLbl {{
    color: {COLORS.TEXT_ALERT};
    font-size: 16px;
    min-width: {SIZES.ERROR.w}px;
    min-height: {SIZES.ERROR.h}px;
}}

#AddItemBtn {{
    color: {COLORS.TEXT_PRIMARY};
    background-color: {COLORS.TRANSPARENT};
    font-size: 14px;
    border: none;
    min-height: 30px;
}}

#AddItemBtn:hover {{
    background-color: {COLORS.HOVER};
}}
'''
