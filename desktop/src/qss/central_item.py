from ..misc import COLORS


css = f'''
#CentralItem {{
    background-color: {COLORS.LIGHT};
    border-radius: 10px;
    min-height: 75px;
    max-width: 500px;
}}

#CentralItem:hover {{
    background-color: {COLORS.HOVER};
}}

#TitleLbl {{
    color: {COLORS.TEXT_PRIMARY};
    font-size: 22px;
}}

#DescriptionLbl {{
    color: {COLORS.TEXT_SECONDARY};
    font-size: 18px;
}}
'''
