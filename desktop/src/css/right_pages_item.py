from ..misc import COLORS, SIZES


css: str = f'''
#ExpiresFrame {{
    min-height: 50px;
}}

#CreatedHintLbl,
#ModifiedHintLbl,
#ExpiresHintLbl {{
    font-size: 14px;
}}

#CreatedLbl,
#ExpiresLbl,
#ModifiedLbl {{
    font-size: 14px;
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

#CreateBtn:hover {{
    background-color: rgba(0, 255, 0, 0.2);
}}

#IconBtn {{
    background-color: {COLORS.LIGHT_GRAY};
    min-width: 120px;
    min-height: 120px;
    border-radius: 59px;
    border: none;
}}

#TitleInput,
#DescriptionInput {{
    border: none;
    background-color: {COLORS.LIGHT_GRAY};
    min-width: 180px;
    color: {COLORS.TEXT_PRIMARY};
    font-size: 18px;
    padding: 5px;
    border-radius: 5px;
}} 

#DescriptionInput {{
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

#AddDocumentBtn,
#AddFieldBtn,
#AddItemBtn {{
    color: {COLORS.TEXT_PRIMARY};
    background-color: {COLORS.TRANSPARENT};
    font-size: 14px;
    border: none;
    min-height: 30px;
}}

#AddItemBtn {{
    min-width: 200px;
}}

#AddDocumentBtn:hover,
#AddFieldBtn:hover,
#AddItemBtn:hover {{
    background-color: rgba(255, 255, 255, 0.1);
}}

#AddDocumentBtn,
#AddFieldBtn {{
    min-width: 140px;
}}

#FieldScrollArea {{
    background-color: {COLORS.LIGHT_GRAY};
    min-width: 300px;
    min-height: 200px;
    border: none;
    border-radius: 5px;
}}

#FieldScrollAreaWidget {{
    background-color: {COLORS.TRANSPARENT};
}}
'''
