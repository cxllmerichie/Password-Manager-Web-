from PyQt5.QtWidgets import QApplication
import sys

from src.app import App


if __name__ == '__main__':
    qapp = QApplication(sys.argv)
    qapp.setStyle('Windows')
    app = App().init()
    app.show()
    sys.exit(qapp.exec_())
