from ..misc import Colors, Sizes


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

#SignInInputFieldEmail,
#SignInInputFieldPassword {{
    font-size: 16px;
    height: {Sizes.AuthInputField.h}px;
    min-width: {Sizes.AuthInputField.w}px;
    border: none;
    background-color: {Colors.INPUT};
    border-radius: 5px;
    padding: 5px;
    color: white;
}}

#SignInInputFramePassword,
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
    min-width: {Sizes.AuthInputField.w}px;
}}

#SignInDontHaveBtn:hover {{
    font-weight: bold;
}}

#AuthExitBtn {{
    background-color: transparent;
    border: none;    
}}

#AuthExitBtn:hover {{
    background-color: {Colors.MAINRED_HOVER};
}}

#SignInErrorLbl {{
    color: red;
    font-size: 16px;
}}

#SignInInputLabelBtn {{
    background-color: rgba(255, 255, 255, 0.1);
    font-size: 16px;
    color: white;
}}

#SignInInputLabelBtn:hover {{
    background-color: rgba(255, 255, 255, 0.2);
}}
'''
