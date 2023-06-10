from ..misc import COLORS, SIZES


def attachment(name: str) -> str:
    return f'''
    #{name} {{
        background-color: {COLORS.DARK};
        border-radius: 5px;
    }}
    
    #DownloadBtn,
    #ShowBtn,
    #DeleteBtn,
    #SaveBtn,
    #EditBtn {{
        border: none;
        border-radius: 9px;
    }}
    
    #FilenameInput {{
        color: {COLORS.TEXT_PRIMARY};
        border: none;
        min-height: 30px;
        background-color: {COLORS.TRANSPARENT};
        font-size: 16px;
    }}
    '''
