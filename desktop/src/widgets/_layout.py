from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt


class Layout:
    Left = Qt.AlignLeft
    LeftTop = Qt.AlignLeft | Qt.AlignTop
    LeftCenter = Qt.AlignLeft | Qt.AlignVCenter
    LeftBottom = Qt.AlignLeft | Qt.AlignBottom

    Right = Qt.AlignRight
    RightTop = Qt.AlignRight | Qt.AlignTop
    RightCenter = Qt.AlignRight | Qt.AlignVCenter
    RightBottom = Qt.AlignRight | Qt.AlignBottom

    VCenter = Qt.AlignVCenter
    VCenterLeft = Qt.AlignVCenter | Qt.AlignLeft
    VCenterRight = Qt.AlignVCenter | Qt.AlignRight

    HCenter = Qt.AlignHCenter
    HCenterTop = Qt.AlignHCenter | Qt.AlignTop
    HCenterBottom = Qt.AlignHCenter | Qt.AlignBottom

    Top = Qt.AlignTop
    Bottom = Qt.AlignBottom
    CenterCenter = Qt.AlignHCenter | Qt.AlignVCenter

    def init(
            self, *,
            margins: tuple[int, ...] = (0, 0, 0, 0), spacing: int = 0, alignment: Qt.Alignment = None
    ) -> 'Layout':
        self.setContentsMargins(*margins)
        self.setSpacing(spacing)
        if alignment:
            self.setAlignment(alignment)
        return self

    def clear(self):
        for i in reversed(range(self.count())):
            self.itemAt(i).widget().setParent(None)
