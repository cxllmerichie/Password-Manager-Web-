from ..assets import Colors, Sizes

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

#SignUpInputField {{
    font-size: 16px;
    height: {Sizes.AuthInputField.h}px;
    min-width: {Sizes.AuthInputField.w}px;
    border: none;
    background-color: transparent;
    color: white;
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
}}

#AuthExitBtn {{
    background-color: transparent;
    border: none;    
}}
'''
