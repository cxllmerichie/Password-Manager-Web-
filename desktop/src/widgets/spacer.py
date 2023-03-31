from PyQt5.QtWidgets import QSpacerItem, QSizePolicy


class Spacer(QSpacerItem):
    def __init__(self, hpolicy: QSizePolicy, vpolicy: QSizePolicy):
        super().__init__(0, 0, hpolicy, vpolicy)
