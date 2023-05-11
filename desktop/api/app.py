from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import const, routers


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

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=const.API_CORS_ORIGINS)

app.include_router(routers.password_router)
app.include_router(routers.category_router)
app.include_router(routers.item_router)
app.include_router(routers.field_router)
app.include_router(routers.attachment_router)


@app.on_event('startup')
async def _():
    assert await const.db.create_pool()
    await const.db.execute(const.tables)


@app.on_event('shutdown')
async def _():
    assert await const.db.close_pool()
