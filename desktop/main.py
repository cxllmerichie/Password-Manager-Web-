from qcontext.misc.uvicorn_threaded_server import Server, Config
from qcontext.qasyncio import AsyncApp
import sys

from src import App
from api.app import app
from api.const import API_HOST, API_PORT


if __name__ == '__main__':
    # import os
    # import sys
    # sys.stdout = open(os.devnull, 'w')

    server = Server(config=Config(app, host=API_HOST, port=API_PORT))
    with server.run_in_thread():
        async def on_close():
            server.stop()
            sys.exit(0)

        async def run_app():
            # from qcontext import CONTEXT
            #
            # CONTEXT['storage'] = None
            # CONTEXT['token'] = None

            (await App().init(
                on_close=on_close
            )).show()

        AsyncApp.run(run_app)
