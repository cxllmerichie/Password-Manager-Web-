from apidevtools.logman import LoggerManager
from aioqui import asynq, CONTEXT

from src.app import App


async def amain():
    # from aioqui import CONTEXT
    #
    # CONTEXT['storage'] = None
    # CONTEXT['token'] = None
    #
    # CONTEXT.debug = True
    app = await App().init()
    app.show()


if __name__ == '__main__':
    # LoggerManager.disable('apidevtools')
    # LoggerManager.disable('aioqui')
    # LoggerManager.disable('__main__')

    asynq.run(amain)
