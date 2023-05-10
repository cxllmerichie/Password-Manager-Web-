from qcontextapi.qasyncio import AsyncApp

from src import App


async def run_app():
    async with AsyncApp():
        from qcontextapi import CONTEXT
        CONTEXT['storage'] = None
        CONTEXT['token'] = None
        app = await App().init()
        app.show()


def run_api():
    import contextlib
    import time
    import threading
    import uvicorn

    from api.app import app
    from api.const import API_HOST, API_PORT

    class Server(uvicorn.Server):
        def install_signal_handlers(self):
            pass

        @contextlib.contextmanager
        def run_in_thread(self):
            thread = threading.Thread(target=self.run)
            thread.start()
            try:
                while not self.started:
                    time.sleep(1e-3)
                yield
            finally:
                self.should_exit = True
                thread.join()

    config = uvicorn.Config(app, host=API_HOST, port=API_PORT, log_level='info')
    server = Server(config=config)

    with server.run_in_thread():
        AsyncApp.run(run_app)


if __name__ == '__main__':
    run_api()


# ToDo: add password generating procedure (fetch from api)
# ToDo: create "Loader" using threads while waiting for displaying items in CentralPagesItems
# ToDo: multilang (translations)
