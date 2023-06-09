from apidevtools.logman import LoggerManager
from aioqui import qasyncio

from src.app import App


async def amain():
    from aioqui import CONTEXT
    from src.misc.const import db, tables

    # CONTEXT['storage'] = None
    # CONTEXT['token'] = None

    assert await db.create_pool()
    await db.execute(tables)
    app = await App().init()
    app.show()


if __name__ == '__main__':
    LoggerManager.disable('apidevtools')
    LoggerManager.disable('aioqui')
    LoggerManager.disable('__main__')

    qasyncio.run(amain)
