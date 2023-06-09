from ..misc import COLORS, SIZES


css: str = f'''
#ExpiresFrame {{
    min-height: 50px;
}}

#CreatedHintLbl,
#ModifiedHintLbl,
#ExpiresHintLbl,
#CreatedLbl,
#ExpiresLbl,
#ModifiedLbl {{
    font-size: 14px;
}}

#CreatedLbl,
#ExpiresLbl,
#ModifiedLbl {{
    font-weight: bold;
}}

#ExpiresSelector {{
    border: none;
    font-size: 12px;
    font-weight: bold;
    color: white;
    background-color: {COLORS.TRANSPARENT};
}}

#SaveBtn {{
    background-color: {COLORS.GREEN};
}}

#HintLbl3,
#HintLbl2 {{
    color: {COLORS.TEXT_PRIMARY};
    font-size: 16px;
    font-style: italic;
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

#CreateBtn:hover {{
    background-color: {COLORS.GREEN_HOVER};
}}

#ControlFrame {{
    background-color: {COLORS.HOVER};
}}

#SaveBtn,
#CancelBtn {{
    color: {COLORS.TEXT_PRIMARY};
    font-size: 16px;
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

#TitleInput,
#DescriptionInput {{
    border: none;
    background-color: {COLORS.LIGHT};
    color: {COLORS.TEXT_PRIMARY};
    font-size: 18px;
    padding: 5px;
    border-radius: 5px;
}} 

#DeleteBtn,
#EditBtn,
#FavouriteBtn,
#CloseBtn {{
    border-radius: {SIZES.CONTROL.w // 2 - 1};
    background-color: {COLORS.TRANSPARENT};
}}

#EditBtn:hover,
#FavouriteBtn:hover {{
    background-color: {COLORS.HOVER};
}}

#DeleteBtn:hover,
#CloseBtn:hover {{
    background-color: {COLORS.RED_HOVER};
}}

#ErrorLbl {{
    color: {COLORS.TEXT_ALERT};
    font-size: 16px;
    min-width: {SIZES.ERROR.w}px;
    min-height: {SIZES.ERROR.h}px;
}}

#ExportBtn,
#AddAttachmentBtn,
#AddFieldBtn {{
    color: {COLORS.TEXT_PRIMARY};
    background-color: {COLORS.TRANSPARENT};
    font-size: 14px;
    border: none;
    min-height: 30px;
}}

#ExportBtn:hover,
#AddAttachmentBtn:hover,
#AddFieldBtn:hover {{
    background-color: {COLORS.HOVER};
}}

#AddAttachmentBtn,
#AddFieldBtn {{
    background-color: {COLORS.BUTTON};
    border-bottom-left-radius: 5px;
    border-bottom-right-radius: 5px;
}}

#AttachmentScrollArea,
#FieldScrollArea {{
    background-color: {COLORS.LIGHT};
    min-height: 90px;
    border: none;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
}}

#AttachmentScrollAreaWidget,
#FieldScrollAreaWidget {{
    background-color: {COLORS.TRANSPARENT};
}}
'''
