from abc import abstractmethod
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
    VCenterTop = Qt.AlignVCenter | Qt.AlignTop
    VCenterCenter = Qt.AlignVCenter | Qt.AlignHCenter
    VCenterBottom = Qt.AlignVCenter | Qt.AlignBottom

    HCenter = Qt.AlignHCenter
    HCenterTop = Qt.AlignHCenter | Qt.AlignTop
    HCenterCenter = Qt.AlignHCenter | Qt.AlignVCenter
    HCenterBottom = Qt.AlignHCenter | Qt.AlignBottom

    Top = Qt.AlignTop
    Bottom = Qt.AlignBottom

    @abstractmethod
    async def init(
            self, *,
            margins: tuple[int, ...] = (0, 0, 0, 0),
            spacing: int = 0, alignment: Qt.Alignment = None
    ) -> 'Layout':
        ...
