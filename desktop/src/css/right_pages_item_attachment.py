from ..misc import COLORS, SIZES


def attachment(name: str) -> str:
    return f'''
    #{name} {{
        background-color: {COLORS.DARK_GRAY};
        border-radius: 5px;
    }}
    
    #AttachmentDownloadBtn,
    #AttachmentShowBtn,
    #AttachmentDeleteBtn,
    #AttachmentSaveBtn,
    #AttachmentEditBtn {{
        border: none;
        border-radius: 9px;
    }}
    
    #AttachmentFilenameInput {{
        color: {COLORS.TEXT_PRIMARY};
        border: none;
        min-height: 30px;
        background-color: {COLORS.TRANSPARENT};
        font-size: 16px;
    }}
    '''
