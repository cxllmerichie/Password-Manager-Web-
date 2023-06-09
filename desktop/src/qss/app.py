from ..misc import COLORS


css = f'''
#App {{
    background-image: url(".assets/background.png");
}}

* {{
    font-family: Verdana;
    color: {COLORS.TEXT_PRIMARY};
}}

#QPushButton:disabled {{
    border: none;
    color: rgba(0, 0, 0, 1);
    background-color: transparent;
}}
'''
