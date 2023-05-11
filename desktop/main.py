from qcontext.qasyncio import AsyncApp
from qcontext.misc.uvicorn_threaded_server import Server, Config

from src import App
from api.app import app
from api.const import API_HOST, API_PORT


if __name__ == '__main__':
    async def run_app():
        async with AsyncApp():
            from qcontext import CONTEXT
            CONTEXT['storage'] = None
            CONTEXT['token'] = None
            (await App().init()).show()

    with Server(config=Config(app, host=API_HOST, port=API_PORT)).run_in_thread():
        AsyncApp.run(run_app)


# ToDo: add password generating procedure (fetch from api)
# ToDo: create "Loader" using threads while waiting for displaying items in CentralPagesItems
# ToDo: multilang (translations)
