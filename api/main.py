import uvicorn
from contextlib import suppress

from src.app import app, const


if __name__ == '__main__':
    loop = 'auto'
    with suppress(ModuleNotFoundError):
        import uvloop

        uvloop.install()
        loop = 'uvloop'
    uvicorn.run(app=app, host=const.API_HOST, port=const.API_PORT, loop=loop, log_config='config.ini')
