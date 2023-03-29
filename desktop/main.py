from PyQt5.QtWidgets import QApplication
import sys
import asyncio

from src import App


async def amain():
    qapp = QApplication(sys.argv)
    qapp.setStyle('Windows')
    window = await App().init()
    window.show()
    sys.exit(qapp.exec_())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(amain())
