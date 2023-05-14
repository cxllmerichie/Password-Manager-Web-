from aioqui.misc.server import Server, Config
from aioqui.qasyncio import AsyncApp
import loguru
import sys

from src import App
from api.app import app
from api.const import API_HOST, API_PORT, LOG_CONFIG


if __name__ == '__main__':
    loguru.logger.disable('apidevttols')
    loguru.logger.disable('qcontext')
    loguru.logger.disable('__main__')

    server = Server(config=Config(app, host=API_HOST, port=API_PORT, log_config=LOG_CONFIG))
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
