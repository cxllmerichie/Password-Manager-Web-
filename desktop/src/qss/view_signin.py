from ..misc import COLORS, SIZES


css = f'''
#SignIn {{
    background-color: {COLORS.SIGNIN};
}}

#EmailLbl,
#PasswordLbl {{
    font-size: 20px;
    font-weight: bold;
    height: {SIZES.AuthInputLabel.h}px;
    color: white;
}}

#EmailInp,
#PasswordInp {{
    font-size: 16px;
    height: {SIZES.AuthInputField.h}px;
    min-width: {SIZES.AuthInputField.w}px;
    border: none;
    background-color: {COLORS.INPUT};
    border-radius: 5px;
    padding: 5px;
    color: white;
}}

#EmailFrm,
#PasswordFrm {{
    border-radius: 10px;
    background-color: {COLORS.DARK};
}}

#ContinueBtn,
#LogInBtn {{
    min-width: {SIZES.AuthMainBtn.w}px;
    height: {SIZES.AuthMainBtn.h}px;
    font-size: 20px;
    font-weight: bold;
    background-color: {COLORS.RED};
    color: white;
}}

#ContinueBtn:hover,
#LogInBtn:hover {{
    background-color: {COLORS.RED_HOVER};
}}

#TextBtn {{
    height: {SIZES.AuthTextBtn.h}px;
    color: white;
    font-size: 14px;
    background-color: {COLORS.TRANSPARENT};
    min-width: {SIZES.AuthInputField.w}px;
}}

#TextBtn:hover {{
    font-weight: bold;
}}

#ErrorLbl {{
    color: red;
    font-size: 16px;
    min-width: {SIZES.ERROR.w}px;
    min-height: {SIZES.ERROR.h}px;}}

#EditBtn {{
    background-color: rgba(255, 255, 255, 0.1);
    font-size: 16px;
    color: white;
}}

#EditBtn:hover {{
    background-color: rgba(255, 255, 255, 0.2);
}}

#InfoLbl {{
    color: white;
    font-size: 30px;
    font-weight: bold;
}}
'''
