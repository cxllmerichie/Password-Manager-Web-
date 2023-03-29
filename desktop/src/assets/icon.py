import os


def source(icon: str) -> str:
    return os.path.join(os.path.abspath('src'), 'assets', 'icons', icon)


class Icon:
    app = source('icon.png')
    minimize = source('minus.svg')
    restore = source('square.svg')
    cross = source('x.svg')
