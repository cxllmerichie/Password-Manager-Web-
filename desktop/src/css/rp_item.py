from ..misc import Colors, Sizes


css: str = f'''
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
    background-color: green;
    color: white;
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
    background-color: {Colors.DARK_GRAY};
    min-width: 120px;
    max-width: 120px;
    min-height: 120px;
    max-height: 120px;
    border-radius: 59px;
    border: none;
}}

#TitleInput,
#DescriptionInput {{
    border: none;
    background-color: {Colors.DARK_GRAY};
    max-width: 180px;
    min-width: 180px;
    color: white;
    font-size: 18px;
    padding: 5px;
    border-radius: 5px;
}} 

#DescriptionInput {{
    max-height: 70px;
}}

#RemoveBtn,
#EditBtn,
#FavouriteBtn,
#CloseBtn {{
    background-color: transparent;
}}

#ControlBtns {{
    max-width: {Sizes.CATEGORY.w}px;
}}

#ErrorLbl {{
    color: red;
    font-size: 16px;
    min-width: {Sizes.ERROR.w}px;
    min-height: {Sizes.ERROR.h}px;
}}

#AddDocumentBtn,
#AddFieldBtn,
#AddItemBtn {{
    color: white;
    background-color: transparent;
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
    max-width: 140px;
}}

#FieldScrollArea {{
    background-color: {Colors.DARK_GRAY};
    min-width: 300px;
    max-width: 300px;
    min-height: 200px;
    max-height: 200px;
    border: none;
    border-radius: 5px;
}}

#FieldScrollAreaWidget {{
    background-color: transparent;
}}
'''

field: str = f'''
#FieldCopyBtn,
#FieldHideBtn,
#FieldDeleteBtn,
#FieldSaveBtn,
#FieldEditBtn {{
    max-width: 20px;
    max-height: 20px;
    border: none;
    border-radius: 9px;
}}

#FieldNameInput,
#FieldValueInput {{
    color: white;
    border: none;
    min-height: 30px;
    background-color: transparent;
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
