from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from typing import Callable
import os

from . import const, routers


app = FastAPI(
    title=const.API_TITLE,
    description=const.API_DESCRIPTION,
    version=const.API_VERSION,
    contact={
        'name': const.API_CONTACT_NAME,
        'url': const.API_CONTACT_URL,
        'email': const.API_CONTACT_EMAIL
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=const.API_CORS_ORIGINS,
    allow_methods=const.API_CORS_METHODS,
    allow_headers=const.API_CORS_HEADERS,
    allow_credentials=const.API_CORS_ALLOW_CREDENTIALS
)


@app.middleware('http')
async def _(request: Request, call_next: Callable):
    try:
        response: Response = await call_next(request)
        const.LOGGER.info(f'{response.status_code}\t{request.method} {request.url.path}')
        return response
    except Exception as error:
        const.LOGGER.error(f'During {request.method} {request.url.path} got {error}')


app.include_router(routers.auth_router)
app.include_router(routers.user_router)
app.include_router(routers.category_router)
app.include_router(routers.item_router)
app.include_router(routers.field_router)
app.include_router(routers.attachment_router)


@app.on_event('startup')
async def _():
    assert await const.db.create_pool()
    assert await const.keys.create_pool()
    assert await const.images.create_pool()
    with open(os.path.join('build', 'postgres.sql'), 'r') as file:
        await const.db.execute(file.read())


@app.on_event('shutdown')
async def _():
    await const.keys.close_pool()
    await const.images.close_pool()
    await const.db.close_pool()
