from ..misc import Colors, Sizes


css = f'''
#SignUp {{
    background-color: {Colors.BACKGROUND};
}}

#InputLabelEmail,
#InputLabelPassword,
#InputLabelConfpass {{
    font-size: 20px;
    font-weight: bold;
    height: {Sizes.AuthInputLabel.h}px;
    color: white;
}}

#InputFieldEmail,
#InputFieldPassword,
#InputFieldConfpass {{
    font-size: 16px;
    height: {Sizes.AuthInputField.h}px;
    min-width: {Sizes.AuthInputField.w}px;
    border: none;
    color: white;
    background-color: {Colors.INPUT};
    border-radius: 5px;
    padding: 5px;
}}

#InputFrameEmail,
#InputFramePassword,
#InputFrameConfpass {{
    border-radius: 10px;
    background-color: {Colors.FOREGROUND};
}}

#AuthMainBtn {{
    min-width: {Sizes.AuthMainBtn.w}px;
    height: {Sizes.AuthMainBtn.h}px;
    font-size: 20px;
    font-weight: bold;
    background-color: {Colors.MAINRED};
    color: white;
}}

#AuthMainBtn:hover {{
    background-color: {Colors.MAINRED_HOVER};
}}

#AuthTextBtn {{
    height: {Sizes.AuthTextBtn.h}px;
    color: white;
    font-size: 14px;
    background-color: transparent;
    min-width: {Sizes.AuthInputField.w}px;
}}

#AuthTextBtn:hover {{
    font-weight: bold;
}}

#AuthExitBtn {{
    background-color: transparent;
    border: none;    
}}

#AuthExitBtn:hover {{
    background-color: {Colors.MAINRED_HOVER};
}}

#ErrorLbl {{
    color: red;
    font-size: 16px;
}}
'''
