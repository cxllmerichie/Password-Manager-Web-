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

#ControlFrame {{
    background-color: {COLORS.HOVER};
    max-height: 50px;
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

#TitleInp,
#DescInp {{
    border: none;
    background-color: {COLORS.DARK};
    min-width: {SIZES.CATEGORY.w}px;
    color: {COLORS.TEXT_PRIMARY};
    font-size: 18px;
    padding: 5px;
    border-radius: 5px;
}} 

#DescInp {{
    max-height: 600px;
}}

#DeleteBtn,
#EditBtn,
#FavBtn,
#CloseBtn {{
    background-color: {COLORS.TRANSPARENT};
}}

#DeleteBtn,
#EditBtn,
#FavBtn,
#CloseBtn {{
    border-radius: {SIZES.CONTROL.w // 2 - 1};
    background-color: {COLORS.TRANSPARENT};
}}

#EditBtn:hover,
#FavBtn:hover {{
    background-color: {COLORS.HOVER};
}}

#DeleteBtn:hover,
#CloseBtn:hover {{
    background-color: {COLORS.RED_HOVER};
}}

#HintLbl1 {{
    color: {COLORS.TEXT_PRIMARY};
    font-size: 16px;
    font-style: italic;
}}

#ErrorLbl {{
    color: {COLORS.TEXT_ALERT};
    font-size: 16px;
    min-width: {SIZES.ERROR.w}px;
    min-height: {SIZES.ERROR.h}px;
}}

#ImportBtn,
#AddItemBtn {{
    color: {COLORS.TEXT_PRIMARY};
    background-color: {COLORS.TRANSPARENT};
    font-size: 14px;
    border: none;
    min-height: 30px;
}}

#ImportBtn:hover,
#AddItemBtn:hover {{
    background-color: {COLORS.HOVER};
}}
'''
