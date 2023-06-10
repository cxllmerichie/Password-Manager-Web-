from ..misc import COLORS


def attachment(name: str) -> str:
    return f'''
    #{name} {{
        background-color: {COLORS.DARK};
        border-radius: 5px;
    }}
    
    #ShowBtn,
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
    #ShowBtn:hover,
    #EditBtn:hover {{
        background-color: {COLORS.HOVER};
    }}
    
    #FilenameInp {{
        color: {COLORS.TEXT_PRIMARY};
        border: none;
        min-height: 30px;
        background-color: {COLORS.TRANSPARENT};
        font-size: 16px;
    }}
    '''
