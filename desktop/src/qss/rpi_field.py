from ..misc import COLORS, SIZES


def field(name: str) -> str:
    return f'''
    #{name} {{
        background-color: {COLORS.RIGHT_MENU};
        border-radius: 5px;
    }}

    #Empty {{
        background-color: {COLORS.TRANSPARENT};
    }}

    #CopyBtn,
    #HideBtn,
    #DeleteBtn,
    #SaveBtn,
    #EditBtn {{
        border: none;
        max-width: 20px;
        min-width: 20px;
        max-height: 20px;
        min-height: 20px;
        border-radius: 9px;
    }}
    
    #DeleteBtn {{
        background-color: {COLORS.RED_HOVER};
    }}
    
    #DeleteBtn:hover {{
        background-color: {COLORS.RED};
    }}
    
    #CopyBtn:hover,
    #HideBtn:hover,
    #EditBtn:hover {{
        background-color: {COLORS.HOVER};
    }}
    
    #NameInp,
    #ValueInp {{
        color: {COLORS.TEXT_PRIMARY};
        border: none;
        min-height: 30px;
        background-color: {COLORS.TRANSPARENT};
        font-size: 16px;
    }}
    
    #NameInp {{
        border-top-left-radius: 5px;
        border-bottom-left-radius: 5px;
    }}
    
    #ValueInp {{
        border-top-right-radius: 5px;
        border-bottom-right-radius: 5px;
    }}
    '''
