from apidevtools.logman import LoggerManager
from aioqui import qasyncio

from src.app import App


async def amain():
    from aioqui import CONTEXT

    # CONTEXT['storage'] = None
    # CONTEXT['token'] = None

    app = await App().init()
    app.show()


if __name__ == '__main__':
    LoggerManager.disable('apidevtools')
    LoggerManager.disable('aioqui')
    LoggerManager.disable('__main__')

    qasyncio.run(amain)
