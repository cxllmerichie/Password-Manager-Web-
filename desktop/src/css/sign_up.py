from ..assets import Color, Size

css = f'''
#SignUp {{
    background-color: {Color.BACKGROUND};
}}

#SignUpInputLabel {{
    font-size: 20px;
    font-weight: bold;
    height: {Size.AuthInputLabel.h}px;
    color: white;
}}

#SignUpInputField {{
    font-size: 16px;
    height: {Size.AuthInputField.h}px;
    min-width: {Size.AuthInputField.w}px;
    border: none;
    background-color: transparent;
    color: white;
}}

#SignUpInputFrame {{
    border-radius: 10px;
    background-color: {Color.FOREGROUND};
}}

#SignUpBtn {{
    min-width: {Size.AuthMainBtn.w}px;
    height: {Size.AuthMainBtn.h}px;
    font-size: 20px;
    font-weight: bold;
    background-color: {Color.Main};
    color: white;
}}

#SignUpAlreadyHaveBtn {{
    height: {Size.AuthTextBtn.h}px;
    color: white;
    font-size: 14px;
    background-color: transparent;
}}
'''
