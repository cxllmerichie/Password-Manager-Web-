from ..misc import COLORS, SIZES


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

image_button = f'''
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

favourite_button = f'''
#FavouriteButton {{
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

date_time_picker = f'''
#ExpiresSelector QAbstractItemView,
#DateTimePickerDaySelector QAbstractItemView,
#DateTimePickerMonthSelector QAbstractItemView,
#DateTimePickerYearSelector QAbstractItemView,
#DateTimePickerHourSelector QAbstractItemView,
#DateTimePickerMinuteSelector QAbstractItemView,
#DateTimePickerSecondSelector QAbstractItemView {{
    border: none;
    color: white;
    background-color: {COLORS.RIGHT_MENU};
}}

#DateTimePickerDaySelector,
#DateTimePickerMonthSelector,
#DateTimePickerYearSelector,
#DateTimePickerHourSelector,
#DateTimePickerMinuteSelector,
#DateTimePickerSecondSelector,
#ExpiresSelector {{
    border: none;
    font-size: 12px;
    font-weight: bold;
    color: white;
    background-color: {COLORS.TRANSPARENT};
}}

#DateTimePickerDaySelector,
#DateTimePickerMonthSelector,
#DateTimePickerYearSelector,
#DateTimePickerHourSelector,
#DateTimePickerMinuteSelector,
#DateTimePickerSecondSelector {{
    min-width: 25px;
}}

#DateTimePickerYearSelector {{
    min-width: 45px;
}}
'''

fullscreen_popup = f'''
#FullscreenPopup {{
    background-color: {COLORS.HOVER};
}}

#StorageLbl {{
    font-weight: bold;
    color: white;
    font-size: 28px;
}}

#LocalBtn,
#RemoteBtn {{
    min-height: 50px;
    color: white;
    font-size: 20px;
    min-width: 400px;
}}

#LocalBtn:hover,
#RemoteBtn:hover {{
    background-color: {COLORS.RED_HOVER};
}}

#HintLbl1 {{
    color: white;
    font-size: 20px;
}}

#HintLbl2 {{
    color: white;
    font-size: 16px;
}}

#ContinueBtn {{
    min-width: {SIZES.AuthMainBtn.w}px;
    height: {SIZES.AuthMainBtn.h}px;
    font-size: 20px;
    font-weight: bold;
    background-color: {COLORS.RED};
    color: white;
}}

#ContinueBtn:hover  {{
    background-color: {COLORS.RED_HOVER};
}}

#AuthExitBtn {{
    background-color: {COLORS.TRANSPARENT};
    border: none;    
}}

#AuthExitBtn:hover {{
    background-color: {COLORS.RED_HOVER};
}}

'''

active_button = f'''
    background-color: {COLORS.RED};
    border: none;
'''

inactive_button = f'''
    background-color: gray;
    border: none;
'''
