from ..misc import COLORS, SIZES


css = f'''
#SignUp {{
    background-color: {COLORS.SIGNUP};
}}

#EmailLbl,
#PasswordLbl,
#ConfpassLbl {{
    font-size: 20px;
    font-weight: bold;
    height: {SIZES.AuthInputLabel.h}px;
    color: white;
}}

#EmailInp,
#PasswordInp,
#ConfpassInp {{
    font-size: 16px;
    height: {SIZES.AuthInputField.h}px;
    min-width: {SIZES.AuthInputField.w}px;
    border: none;
    color: white;
    background-color: {COLORS.INPUT};
    border-radius: 5px;
    padding: 5px;
}}

#EmailFrm,
#PasswordFrm,
#ConfpassFrm {{
    border-radius: 10px;
    background-color: {COLORS.DARK};
}}

#MainBtn {{
    min-width: {SIZES.AuthMainBtn.w}px;
    height: {SIZES.AuthMainBtn.h}px;
    font-size: 20px;
    font-weight: bold;
    background-color: {COLORS.RED};
    color: white;
}}

#MainBtn:hover {{
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
    min-height: {SIZES.ERROR.h}px;
}}

#InfoLbl {{
    color: white;
    font-size: 30px;
    font-weight: bold;
}}
'''
