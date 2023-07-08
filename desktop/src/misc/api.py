from aioqui.misc.aiorequest import request
from mimetypes import MimeTypes
from datetime import datetime
from aioqui.types import Icon
from .utils import prepare
from aioqui import CONTEXT
from copy import deepcopy
from typing import Any
from uuid import UUID
import ujson as json
import aiohttp
import os

from .assets import EXTENSIONS, PATHS
from .utils import accept_h, auth_h, accept_content_h, login_h, Storage
from . import crud


# request.baseurl = 'https://pmapi.cxllmerichie.com'
request.baseurl = 'http://127.0.0.1:8888'

fields: list[str] = []
attachments: list[str] = []


async def login(auth_data: dict[str, Any]) -> dict[str, Any]:
    params = dict(username=auth_data['email'], password=auth_data['password'],
                  grant_type='', scope='', client_id='', client_secret='')
    response = await request.post('/auth/token', headers=login_h(), data=params)
    if token := response.get('access_token'):
        CONTEXT['token'] = token
    return response


async def check_email(email: str) -> bool:
    return await request.get(f'/auth/{email}', headers=accept_h())


async def create_user(user: dict[str, Any]) -> dict[str, Any]:
    response = await request.post('/user', headers=accept_content_h(), body=user)
    if token := response.get('access_token'):
        CONTEXT['token'] = token
    return response


async def get_categories() -> list[dict[str, Any]]:
    if Storage.is_remote():
        response = await request.get('/categories/', headers=auth_h(), pythonize=True)
    else:
        response = await crud.get_categories()
    return response


async def create_category(category: dict[str, Any]) -> dict[str, Any]:
    if Storage.is_remote():
        response = await request.post('/category', headers=auth_h(), body=await prepare(category), pythonize=True)
    else:
        response = await crud.create_category(category)
    return response


async def get_category(category_id: int) -> dict[str, Any]:
    if Storage.is_remote():
        response = await request.get(f'/category{category_id}', headers=auth_h(), pythonize=True)
    else:
        response = await crud.get_category(category_id)
    return response


async def update_category(category_id: int, category: dict[str, Any]) -> dict[str, Any]:
    if Storage.is_remote():
        response = await request.put(f'/category/{category_id}', headers=auth_h(), body=await prepare(category), pythonize=True)
    else:
        response = await crud.update_category(category_id, category)
    return response


async def delete_category(category_id: int) -> dict[str, Any]:
    if Storage.is_remote():
        response = await request.delete(f'/category/{category_id}', headers=auth_h(), pythonize=True)
    else:
        response = await crud.delete_category(category_id)
    return response


async def create_item(category_id: int, item: dict[str, Any]) -> dict[str, Any]:
    if Storage.is_remote():
        response = await request.post(f'/category/{category_id}/item', headers=auth_h(), body=await prepare(item), pythonize=True)
    else:
        response = await crud.create_item(category_id, item)
    return response


async def get_items(category_id: int) -> list[dict[str, Any]]:
    if Storage.is_remote():
        response = await request.get(f'/category/{category_id}/items', headers=auth_h(), pythonize=True)
    else:
        response = await crud.get_items(category_id)
    return response


async def delete_item(item_id: int) -> dict[str, Any]:
    if Storage.is_remote():
        response = await request.delete(f'/item/{item_id}', headers=auth_h(), pythonize=True)
    else:
        response = await crud.delete_item(item_id)
    return response


async def update_item(item_id: int, item: dict[str, Any]) -> dict[str, Any]:
    if Storage.is_remote():
        response = await request.put(f'/item/{item_id}', headers=auth_h(), body=await prepare(item, ['expires_at']), pythonize=True)
    else:
        response = await crud.update_item(item_id, item)
    return response


async def export_item(item: dict[str, Any], directory: str) -> str:
    # create copy to manage dict keys later on
    _item = deepcopy(item)
    # create sub dir in selected dir to save there all the data
    export_dir = os.path.join(directory, _item['title'])
    attachments_dir = os.path.join(export_dir, 'attachments')
    os.makedirs(attachments_dir)
    # manage necessary keys to make human-readable *.json file
    item_pop_keys = ['icon', 'id', 'category_id']
    for key in item_pop_keys:
        _item.pop(key)
    field_pop_keys = ['id', 'item_id']
    _item['fields'] = await get_fields(item['id'])
    for i in range(len(_item['fields'])):
        for key in field_pop_keys:
            _item['fields'][i].pop(key)
    attachment_pop_keys = ['id', 'item_id', 'content', 'mime', 'filename']
    _item['attachments'] = await get_attachments(item['id'])
    for i in range(len(_item['attachments'])):
        filepath = os.path.abspath(os.path.join(attachments_dir, _item['attachments'][i]['filename']))
        _item['attachments'][i]['file'] = filepath
        await download_attachment(filepath, _item['attachments'][i])
        for key in attachment_pop_keys:
            _item['attachments'][i].pop(key)
    for key, value in _item.items():
        if isinstance(value, datetime):
            _item[key] = str(value)
    with open(os.path.join(export_dir, 'item.json'), 'w') as file:
        json.dump(_item, file, indent=4)
    return export_dir


async def import_item(category_id: int, filepath: str) -> dict[str, Any]:
    with open(filepath, 'r') as file:
        item = json.load(file)
    item_pop_keys = ['created_at', 'modified_at', 'fields', 'attachments']
    fields, attachments = item.get('fields', ()), item.get('attachments', ())
    for key in item_pop_keys:
        if key in item.keys():
            item.pop(key)
    created_item = await create_item(category_id, await prepare(item))
    if item_id := created_item.get('id'):
        for field in fields:
            await add_field(item_id, field)
        for attachment in attachments:
            await add_attachment(item_id, await get_attachment_data(attachment['file']))
    return created_item


async def add_field(item_id: int, field: dict[str, Any]) -> dict[str, Any]:
    if Storage.is_remote():
        response = await request.post(f'/item/{item_id}/field', headers=auth_h(), body=field, pythonize=True)
    else:
        response = await crud.create_field(item_id, field)
    return response


async def get_fields(item_id: int) -> list[dict[str, Any]]:
    if Storage.is_remote():
        response = await request.get(f'/item/{item_id}/fields', headers=auth_h(), pythonize=True)
    else:
        response = await crud.get_fields(item_id)
    return response


async def update_field(field_id: UUID, field: dict[str, Any]) -> dict[str, Any]:
    if Storage.is_remote():
        response = await request.put(f'/field/{field_id}', headers=auth_h(), body=field, pythonize=True)
    else:
        response = await crud.update_field(field_id, field)
    return response


async def delete_field(field_id: UUID) -> dict[str, Any]:
    if Storage.is_remote():
        response = await request.delete(f'/field/{field_id}', headers=auth_h(), pythonize=True)
    else:
        response = await crud.delete_field(field_id)
    return response


async def add_attachment(item_id: int, attachment: dict[str, Any]) -> dict[str, Any]:
    if Storage.is_remote():
        response = await request.post(f'/item/{item_id}/attachment', headers=auth_h(), body=attachment, pythonize=True)
    else:
        response = await crud.create_attachment(item_id, attachment)
    return response


async def get_attachments(item_id: int) -> list[dict[str, Any]]:
    if Storage.is_remote():
        response = await request.get(f'/item/{item_id}/attachments', headers=auth_h(), pythonize=True)
    else:
        response = await crud.get_attachments(item_id)
    return response


async def update_attachment(attachment_id: UUID, attachment: dict[str, Any]) -> dict[str, Any]:
    if Storage.is_remote():
        response = await request.put(f'/attachment/{attachment_id}', headers=auth_h(), body=attachment, pythonize=True)
    else:
        response = await crud.update_attachment(attachment_id, attachment)
    return response


async def delete_attachment(attachment_id: UUID) -> dict[str, Any]:
    if Storage.is_remote():
        response = await request.delete(f'/attachment/{attachment_id}', headers=auth_h(), pythonize=True)
    else:
        response = await crud.delete_attachment(attachment_id)
    return response


async def download_attachment(filepath: str, attachment: dict[str, Any]):
    with open(filepath, 'wb') as file:
        file.write(eval(attachment['content']))


async def get_attachment_data(filepath: str) -> dict[str, Any]:
    mime = MimeTypes().guess_type(filepath)[0]
    if mime == 'image/jpeg':
        with open(filepath, 'rb') as file:
            content = str(Icon.bytes(Icon(file.read()).icon))
    elif mime == 'text/plain':
        with open(filepath, 'rb') as file:
            content = str(file.read())
    return {'content': content, 'filename': os.path.basename(filepath), 'mime': mime}


async def is_connected() -> bool:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{request.baseurl}/docs') as response:
                return response.status == 200
    except Exception:
        return False


async def save_icon(icon: bytes | str) -> None:
    filename = f"{datetime.now().strftime('%d.%m.%Y %H-%M-%S')}.{EXTENSIONS.ICON}"
    with open(os.path.join(PATHS.ICONS, filename), 'wb') as file:
        file.write(icon)
