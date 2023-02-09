from .assets import Color


style = f'''
#Application {{
    background: {Color.accent1};
    border: none;
}}

#ScrollArea {{
    background: transparent;
}}

#SearchBar {{
    background: {Color.accent2};
    color: {Color.text1};
    font-size: 18px;
    border: none;
    height: 30px;
}}

#SearchBarWidget {{
    background: transparent;
}}

#Key, #Value {{
    background: {Color.accent1};
    color: {Color.text1};
    border: 0.5px solid white;
}}

#PushButton {{
    background: {Color.accent1};
    color: white;
}}

#PushButton:hover {{
    background: {Color.accent2};
}}
'''