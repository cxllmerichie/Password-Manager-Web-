from PyQt5.QtWidgets import QApplication
import sys
import asyncio

from src.app import App


async def amain():
    qapp = QApplication(sys.argv)
    qapp.setStyle('Windows')
    window = await App().init()
    window.show()
    sys.exit(qapp.exec_())


if __name__ == '__main__':
    LOOP = asyncio.get_event_loop()
    LOOP.run_until_complete(amain())
