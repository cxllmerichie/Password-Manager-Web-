from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import *
from .database import db


app = FastAPI(
    title='Title',
    description='Description',
    version='1.0.0',
    contact={
        "name": "cxllmerichie",
        "url": "https://github.com/cxllmerichie",
        "email": "cxllmerichie@gmail.com",
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True,
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(password_router)


@app.on_event('startup')
async def startup():
    if await db.create_pool():
        with open('api/build/init.sql', 'r') as file:
            await db.execute(file.read())


@app.on_event('shutdown')
async def shutdown():
    await db.close_pool()
