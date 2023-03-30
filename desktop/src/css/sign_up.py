from ..assets import Color, Sizes

css = f'''
#SignUp {{
    background-color: {Color.BACKGROUND};
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
    background-color: {Color.FOREGROUND};
}}

#SignUpBtn {{
    min-width: {Sizes.AuthMainBtn.w}px;
    height: {Sizes.AuthMainBtn.h}px;
    font-size: 20px;
    font-weight: bold;
    background-color: {Color.MAINRED};
    color: white;
}}

#SignUpAlreadyHaveBtn {{
    height: {Sizes.AuthTextBtn.h}px;
    color: white;
    font-size: 14px;
    background-color: transparent;
}}
'''
