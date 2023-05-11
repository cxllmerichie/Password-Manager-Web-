from qcontext.qasyncio import AsyncApp
from qcontext.misc.uvicorn_threaded_server import Server, Config

from src import App
from api.app import app
from api.const import API_HOST, API_PORT


if __name__ == '__main__':
    async def run_app():
        async with AsyncApp():
            # from qcontext import CONTEXT
            #
            # CONTEXT['storage'] = None
            # CONTEXT['token'] = None

            (await App().init()).show()


    import os
    # with open(os.devnull, 'w') as null:
    #     stdout = os.dup(1)
    #     stderr = os.dup(2)
    #     os.dup2(null.fileno(), 1)
    #     os.dup2(null.fileno(), 2)
    # from logging import getLogger
    # getLogger('uvicorn.error').disabled = True
    # getLogger('uvicorn.access').disabled = True
    import sys
    sys.stdout = open(os.devnull, 'w')

    with Server(config=Config(app, host=API_HOST, port=API_PORT)).run_in_thread():
        AsyncApp.run(run_app)
