from ..misc import COLORS, SIZES


css = f'''
#SignIn {{
    background-color: {COLORS.LIGHT_GRAY};
}}

#InputLabelEmail,
#InputLabelPassword {{
    font-size: 20px;
    font-weight: bold;
    height: {SIZES.AuthInputLabel.h}px;
    color: white;
}}

#InputFieldEmail,
#InputFieldPassword {{
    font-size: 16px;
    height: {SIZES.AuthInputField.h}px;
    min-width: {SIZES.AuthInputField.w}px;
    border: none;
    background-color: {COLORS.INPUT};
    border-radius: 5px;
    padding: 5px;
    color: white;
}}

#InputFrameEmail,
#InputFramePassword {{
    border-radius: 10px;
    background-color: {COLORS.DARK_GRAY};
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

#AuthTextBtn {{
    height: {SIZES.AuthTextBtn.h}px;
    color: white;
    font-size: 14px;
    background-color: {COLORS.TRANSPARENT};
    min-width: {SIZES.AuthInputField.w}px;
}}

#AuthTextBtn:hover {{
    font-weight: bold;
}}

#AuthExitBtn {{
    background-color: {COLORS.TRANSPARENT};
    border: none;    
}}

#AuthExitBtn:hover {{
    background-color: {COLORS.RED_HOVER};
}}

#ErrorLbl {{
    color: red;
    font-size: 16px;
    min-width: {SIZES.ERROR.w}px;
    min-height: {SIZES.ERROR.h}px;}}

#InputLabelEmailEditBtn {{
    background-color: rgba(255, 255, 255, 0.1);
    font-size: 16px;
    color: white;
}}

#InputLabelEmailEditBtn:hover {{
    background-color: rgba(255, 255, 255, 0.2);
}}

#InfoLbl {{
    color: white;
    font-size: 30px;
    font-weight: bold;
}}
'''
