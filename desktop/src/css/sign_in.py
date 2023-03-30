from ..assets import Color, Size


css = f'''
#SignIn {{
    background-color: {Color.BACKGROUND};
}}

#SignInInputLabel {{
    font-size: 20px;
    font-weight: bold;
    height: {Size.AuthInputLabel.h}px;
    color: white;
}}

#SignInInputField {{
    font-size: 16px;
    height: {Size.AuthInputField.h}px;
    min-width: {Size.AuthInputField.w}px;
    border: none;
    background-color: transparent;
    color: white;
}}

#SignInInputFrame {{
    border-radius: 10px;
    background-color: {Color.FOREGROUND};
}}

#SignInBtn {{
    min-width: {Size.AuthMainBtn.w}px;
    height: {Size.AuthMainBtn.h}px;
    font-size: 20px;
    font-weight: bold;
    background-color: {Color.Main};
    color: white;
}}

#SignInDontHaveBtn {{
    height: {Size.AuthTextBtn.h}px;
    color: white;
    font-size: 14px;
    background-color: transparent;
}}
'''
