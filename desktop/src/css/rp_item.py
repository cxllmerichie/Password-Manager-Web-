from ..misc import Colors, Sizes


css: str = f'''
#ItemFrame {{
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
    color: white;
    font-size: 16px;
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
    background-color: rgba(0, 255, 0, 0.2);
}}

#IconBtn {{
    background-color: {Colors.LIGHT_GRAY};
    min-width: 120px;
    min-height: 120px;
    border-radius: 59px;
    border: none;
}}

#TitleInput,
#DescriptionInput {{
    border: none;
    background-color: {Colors.LIGHT_GRAY};
    min-width: 180px;
    color: {Colors.TEXT_PRIMARY};
    font-size: 18px;
    padding: 5px;
    border-radius: 5px;
}} 

#DescriptionInput {{
}}

#RemoveBtn,
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

#AddDocumentBtn,
#AddFieldBtn,
#AddItemBtn {{
    color: {Colors.TEXT_PRIMARY};
    background-color: {Colors.TRANSPARENT};
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
    background-color: {Colors.LIGHT_GRAY};
    min-width: 300px;
    min-height: 200px;
    border: none;
    border-radius: 5px;
}}

#FieldScrollAreaWidget {{
    background-color: {Colors.TRANSPARENT};
}}
'''

field: str = f'''
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
    color: white;
    border: none;
    min-height: 30px;
    background-color: {Colors.TRANSPARENT};
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
