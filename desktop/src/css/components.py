from ..misc import COLORS


scroll: str = f'''
QScrollBar:vertical {{
    background: {COLORS.TRANSPARENT};
    width: 7px;
    border: none;
    border-radius: 3px;
    margin: 0px 0 1px 0;
}}

QScrollBar::handle:vertical {{
    background: {COLORS.RED};
    border-radius: 3px;
}}

QScrollBar::handle:vertical:hover {{
    background: {COLORS.RED_HOVER};
}}

QScrollBar::add-line:vertical {{
    height: 0px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}}

QScrollBar::sub-line:vertical {{
    height: 0px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {{
    background: none;
}}
'''

img_btn = f'''
#ImageButton::disabled {{
    
}}

#ImageButton {{
    background-color: {COLORS.LIGHT_GRAY};
    min-width: 120px;
    min-height: 120px;
    border-radius: 59px;
    border: none;
}}
'''

fav_btn = f'''
#FavouriteButton {{
    background-color: {COLORS.TRANSPARENT};
}}
'''

splitter = f'''
#MainViewSplitter {{
    background-color: {COLORS.Palette.LAYER_3};
}}

#MainViewSplitter::handle {{
    background-color: {COLORS.TRANSPARENT};
}}
'''

search = f'''
#SearchBar {{
    background-color: {COLORS.SEARCH};
    font-size: 18px;
    padding: 5px;
    color: {COLORS.TEXT_PRIMARY};
    border: none;
}}

#SearchBarPopup {{
    background-color: {COLORS.Palette.LAYER_1};
    border: none;
    color: white;
    font-size: 16px;
}}

QListView::item:hover {{
    background-color: {COLORS.Palette.LAYER_6};
}}
'''
