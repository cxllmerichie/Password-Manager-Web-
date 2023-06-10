from ..misc import COLORS, SIZES


def field(name: str) -> str:
    return f'''
    #{name} {{
        background-color: {COLORS.DARK};
        border-radius: 5px;
    }}
            
    #FieldCopyBtn,
    #FieldHideBtn,
    #FieldDeleteBtn,
    #FieldSaveBtn,
    #FieldEditBtn {{
        border: none;
        border-radius: 9px;
    }}
    
    #FieldNameInput,
    #FieldValueInput {{
        color: {COLORS.TEXT_PRIMARY};
        border: none;
        min-height: 30px;
        background-color: {COLORS.TRANSPARENT};
        font-size: 16px;
    }}
    
    #FieldNameInput {{
        border-top-left-radius: 5px;
        border-bottom-left-radius: 5px;
    }}
    
    #FieldValueInput {{
        border-top-right-radius: 5px;
        border-bottom-right-radius: 5px;
    }}
    '''
