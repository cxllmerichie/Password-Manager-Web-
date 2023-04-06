from ..misc import Colors, Sizes


css = f'''
#SignUp {{
    background-color: {Colors.BACKGROUND};
}}

#SignUpInputLabel {{
    font-size: 20px;
    font-weight: bold;
    height: {Sizes.AuthInputLabel.h}px;
    color: white;
}}

#SignUpInputFieldEmail,
#SignUpInputFieldPassword,
#SignUpInputFieldConfpass {{
    font-size: 16px;
    height: {Sizes.AuthInputField.h}px;
    min-width: {Sizes.AuthInputField.w}px;
    border: none;
    color: white;
    background-color: {Colors.INPUT};
    border-radius: 5px;
    padding: 5px;
}}

#SignUpInputFrame {{
    border-radius: 10px;
    background-color: {Colors.FOREGROUND};
}}

#SignUpBtn {{
    min-width: {Sizes.AuthMainBtn.w}px;
    height: {Sizes.AuthMainBtn.h}px;
    font-size: 20px;
    font-weight: bold;
    background-color: {Colors.MAINRED};
    color: white;
}}

#SignUpBtn:hover {{
    background-color: {Colors.MAINRED_HOVER};
}}

#SignUpAlreadyHaveBtn {{
    height: {Sizes.AuthTextBtn.h}px;
    color: white;
    font-size: 14px;
    background-color: transparent;
    min-width: {Sizes.AuthInputField.w}px;
}}

#SignUpAlreadyHaveBtn:hover {{
    font-weight: bold;
}}

#AuthExitBtn {{
    background-color: transparent;
    border: none;    
}}

#AuthExitBtn:hover {{
    background-color: {Colors.MAINRED_HOVER};
}}

#SignUpErrorLbl {{
    color: red;
    font-size: 16px;
}}
'''
