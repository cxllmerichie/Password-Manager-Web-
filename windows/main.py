from PyQt5.QtWidgets import QApplication
from sys import argv, exit

from windows.src import Application, style


def main():
    qapp = QApplication(argv)
    qapp.setStyle('Windows')
    qapp.setStyleSheet(style)
    app = Application('data.json')
    app.show()
    exit(qapp.exec_())


if __name__ == '__main__':
    main()
