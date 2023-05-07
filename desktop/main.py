from PyQt5.QtWidgets import QApplication
import sys

from src import App


if __name__ == '__main__':
    qapp = QApplication(sys.argv)
    qapp.setStyle('Windows')
    app = App().init()
    app.show()
    sys.exit(qapp.exec_())


# ToDo: local/remote storage (fetch from both if local chosen, any new added to local, colors of local/remote are different)

# ToDo: add password generating procedure (fetch from api)
# ToDo: create "Loader" using threads while waiting for displaying items in CentralPagesItems
# ToDo: multilang (translations)
