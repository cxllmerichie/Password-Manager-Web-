from PyQt5.QtWidgets import QApplication
import sys
from qcontextapi import CONTEXT

from src import App


if __name__ == '__main__':
    qapp = QApplication(sys.argv)
    qapp.setStyle('Windows')
    app = App().init()
    app.show()
    # костыли ебаные, дерьмо не работает если вызывать до появления окна (что-то там с ресайзами)

    sys.exit(qapp.exec_())


# ToDo: Fix 'elided' in CentralPagesItems when resizing SplitterWidgets
# ToDo: Item attachments
# ToDo: user profile and settings
# ToDo: local/remote storage (fetch from both if local chosen, any new added to local, colors of local/remote are different)

# ToDo: fix QPushButton.disabled Icon
# ToDo: add password generating procedure (fetch from api)
# ToDo: create "Loader" using threads while waiting for displaying items in CentralPagesItems
# ToDo: multilang (translations)
