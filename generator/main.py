from PyQt5.QtWidgets import QApplication
from sys import argv

from gui import Application


def main():
    qapp = QApplication(argv)
    app = Application()
    qapp.exec()


if __name__ == '__main__':
    main()
