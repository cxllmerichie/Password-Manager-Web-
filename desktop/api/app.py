from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import const, routers


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
