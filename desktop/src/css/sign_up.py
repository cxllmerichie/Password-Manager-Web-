from ..assets import Color

css = f'''
#SignUp {{
    background-color: {Color.background};
}}

#SignUpInputLabel {{
    font-size: 20px;
    font-weight: bold;
    height: 25px;
    color: white;
}}

#SignUpInputField {{
    font-size: 16px;
    height: 25px;
    min-width: 300px;
    border: none;
    background-color: transparent;
    color: white;
}}

#SignUpInputFrame {{
    border-radius: 10px;
    background-color: {Color.foreground};
}}

#SignUpBtn {{
    min-width: 200px;
    height: 30px;
    font-size: 20px;
    font-weight: bold;
    background-color: {Color.main};
    color: white;
}}
'''
