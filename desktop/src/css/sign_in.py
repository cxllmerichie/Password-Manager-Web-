from ..assets import Color

css = f'''
#SignIn {{
    background-color: {Color.background};
}}

#SignInInputLabel {{
    font-size: 20px;
    font-weight: bold;
    height: 25px;
    color: white;
}}

#SignInInputField {{
    font-size: 16px;
    height: 25px;
    min-width: 300px;
    border: none;
    background-color: transparent;
    color: white;
}}

#SignInInputFrame {{
    border-radius: 10px;
    background-color: {Color.foreground};
}}

#SignInBtn {{
    min-width: 200px;
    height: 30px;
    font-size: 20px;
    font-weight: bold;
    background-color: {Color.main};
    color: white;
}}

#SignInDontHaveBtn {{
    height: 20px;
    color: white;
    font-size: 14px;
    background-color: transparent;
}}
'''
