from PyQt5.QtWidgets import QApplication
import sys

from src.app import App


if __name__ == '__main__':
    qapp = QApplication(sys.argv)
    qapp.setStyle('Windows')
    app = App().init()
    app.show()
    sys.exit(qapp.exec_())

# ToDo: fix QPushButton.disabled Icon
# ToDo: display micro-instruction below description during creation of category
# ToDo: display "No items yet" in CentralPagesItems when category does not have items
# ToDo: create "Loader" using threads while waiting for displaying items in CentralPagesitems
# ToDo: Fix 'elided' in CentralPagesItems when resizing SplitterWidgets
# ToDo: Make LeftMenu to be SplitterWidget
# ToDo: Add search bar to categories
# ToDo: Move toggle LeftMenu button to the horizontal layout together with search bar for categories
# ToDo: Add search bar to items
# ToDo: Display Category.title (or topic as All/Favourite) when displaying items
