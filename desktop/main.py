from PyQt5.QtWidgets import QApplication
from qcontextapi import CONTEXT
import sys

from src import App


def main():
    qapp = QApplication(sys.argv)
    qapp.setStyle('Windows')
    app = App().init()
    app.show()
    sys.exit(qapp.exec_())


if __name__ == '__main__':
    main()
    from src.misc import utils

    if CONTEXT['local']:
        utils.stop_local()


# ToDo: add password generating procedure (fetch from api)
# ToDo: create "Loader" using threads while waiting for displaying items in CentralPagesItems
# ToDo: multilang (translations)
