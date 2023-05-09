from PyQt5.QtWidgets import QApplication
import sys

from src import App


if __name__ == '__main__':
    from qcontextapi import CONTEXT

    # CONTEXT['storage'] = None
    # CONTEXT['token'] = None
    qapp = QApplication(sys.argv)
    qapp.setStyle('Windows')
    app = App().init()
    app.show()
    sys.exit(qapp.exec_())



# ToDo: add password generating procedure (fetch from api)
# ToDo: create "Loader" using threads while waiting for displaying items in CentralPagesItems
# ToDo: multilang (translations)
