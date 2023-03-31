from ..const import Colors, Sizes


css = f'''
#SignIn {{
    background-color: {Colors.BACKGROUND};
}}

#SignInInputLabel {{
    font-size: 20px;
    font-weight: bold;
    height: {Sizes.AuthInputLabel.h}px;
    color: white;
}}

#SignInInputField {{
    font-size: 16px;
    height: {Sizes.AuthInputField.h}px;
    min-width: {Sizes.AuthInputField.w}px;
    border: none;
    background-color: transparent;
    color: white;
}}

#SignInInputFrame {{
    border-radius: 10px;
    background-color: {Colors.FOREGROUND};
}}

#SignInBtn {{
    min-width: {Sizes.AuthMainBtn.w}px;
    height: {Sizes.AuthMainBtn.h}px;
    font-size: 20px;
    font-weight: bold;
    background-color: {Colors.MAINRED};
    color: white;
}}

#SignInBtn:hover {{
    background-color: {Colors.MAINRED_HOVER};
}}

#SignInDontHaveBtn {{
    height: {Sizes.AuthTextBtn.h}px;
    color: white;
    font-size: 14px;
    background-color: transparent;
}}

#AuthExitBtn {{
    background-color: transparent;
    border: none;    
}}
'''
