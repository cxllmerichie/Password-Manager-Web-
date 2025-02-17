from aioqui.misc import aiorequest
from mimetypes import MimeTypes
from datetime import datetime
from aioqui.types import Icon
from contextlib import suppress
from aioqui import CONTEXT
from copy import deepcopy
from typing import Any
from uuid import UUID
import ujson as json
import aiohttp
import os

from .assets import EXTENSIONS, PATHS
from .utils import accept_h, auth_h, accept_content_h, login_h, Storage, prepare
from . import crud


aiorequest.baseurl = 'https://pmapi.cxllmerichie.com'
# aiorequest.baseurl = 'http://127.0.0.1:8888'

fields: list[str] = []
attachments: list[str] = []


async def login(auth_data: dict[str, Any]) -> dict[str, Any]:
    params = dict(username=auth_data['email'], password=auth_data['password'],
                  grant_type='', scope='', client_id='', client_secret='')
    response = await aiorequest.post('/auth/token', headers=login_h(), data=params)
    if token := response.get('access_token'):
        CONTEXT['token'] = token
    return response


async def check_email(email: str) -> bool:
    return await aiorequest.get(f'/auth/{email}', headers=accept_h())


async def create_user(user: dict[str, Any]) -> dict[str, Any]:
    response = await aiorequest.post('/user', headers=accept_content_h(), body=user)
    if token := response.get('access_token'):
        CONTEXT['token'] = token
    return response


async def get_categories() -> list[dict[str, Any]]:
    if Storage.is_remote():
        response = await aiorequest.get('/categories', headers=auth_h(), deserialize=True)
    else:
        response = await crud.get_categories()
    return response


async def create_category(category: dict[str, Any]) -> dict[str, Any]:
    if Storage.is_remote():
        response = await aiorequest.post('/category', headers=auth_h(), body=await prepare(category), deserialize=True)
    else:
        response = await crud.create_category(category)
    return response


async def get_category(category_id: int) -> dict[str, Any]:
    if Storage.is_remote():
        response = await aiorequest.get(f'/category{category_id}', headers=auth_h(), deserialize=True)
    else:
        response = await crud.get_category(category_id)
    return response


async def update_category(category_id: int, category: dict[str, Any]) -> dict[str, Any]:
    if Storage.is_remote():
        response = await aiorequest.put(f'/category/{category_id}', headers=auth_h(), body=await prepare(category), deserialize=True)
    else:
        response = await crud.update_category(category_id, category)
    return response


async def delete_category(category_id: int) -> dict[str, Any]:
    if Storage.is_remote():
        response = await aiorequest.delete(f'/category/{category_id}', headers=auth_h(), deserialize=True)
    else:
        response = await crud.delete_category(category_id)
    return response


async def create_item(category_id: int, item: dict[str, Any]) -> dict[str, Any]:
    if Storage.is_remote():
        response = await aiorequest.post(f'/category/{category_id}/item', headers=auth_h(), body=await prepare(item), deserialize=True)
    else:
        response = await crud.create_item(category_id, item)
    return response


async def get_items(category_id: int) -> list[dict[str, Any]]:
    if Storage.is_remote():
        response = await aiorequest.get(f'/category/{category_id}/items', headers=auth_h(), deserialize=True)
    else:
        response = await crud.get_items(category_id)
    return response


async def delete_item(item_id: int) -> dict[str, Any]:
    if Storage.is_remote():
        response = await aiorequest.delete(f'/item/{item_id}', headers=auth_h(), deserialize=True)
    else:
        response = await crud.delete_item(item_id)
    return response


async def update_item(item_id: int, item: dict[str, Any]) -> dict[str, Any]:
    if Storage.is_remote():
        response = await aiorequest.put(f'/item/{item_id}', headers=auth_h(), body=await prepare(item, ['expires_at']), deserialize=True)
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
    for key in ['icon', 'id', 'category_id']:
        _item.pop(key)
    _item['fields'] = await get_fields(item['id'])
    for i in range(len(_item['fields'])):
        for key in ['id', 'item_id']:
            _item['fields'][i].pop(key)
    _item['attachments'] = await get_attachments(item['id'])
    for i in range(len(_item['attachments'])):
        filepath = os.path.abspath(os.path.join(attachments_dir, _item['attachments'][i]['filename']))
        _item['attachments'][i]['file'] = filepath
        with open(filepath, 'wb') as file:
            file.write(eval(_item['attachments'][i]['content']))
        for key in ['id', 'item_id', 'content', 'mime', 'filename']:
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
    fields, attachments = item.get('fields', ()), item.get('attachments', ())
    for key in ['created_at', 'modified_at', 'fields', 'attachments']:
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
        response = await aiorequest.post(f'/item/{item_id}/field', headers=auth_h(), body=field, deserialize=True)
    else:
        response = await crud.create_field(item_id, field)
    return response


async def get_fields(item_id: int) -> list[dict[str, Any]]:
    if Storage.is_remote():
        response = await aiorequest.get(f'/item/{item_id}/fields', headers=auth_h(), deserialize=True)
    else:
        response = await crud.get_fields(item_id)
    return response


async def update_field(field_id: UUID, field: dict[str, Any]) -> dict[str, Any]:
    if Storage.is_remote():
        response = await aiorequest.put(f'/field/{field_id}', headers=auth_h(), body=field, deserialize=True)
    else:
        response = await crud.update_field(field_id, field)
    return response


async def delete_field(field_id: UUID) -> dict[str, Any]:
    if Storage.is_remote():
        response = await aiorequest.delete(f'/field/{field_id}', headers=auth_h(), deserialize=True)
    else:
        response = await crud.delete_field(field_id)
    return response


async def add_attachment(item_id: int, attachment: dict[str, Any]) -> dict[str, Any]:
    if Storage.is_remote():
        response = await aiorequest.post(f'/item/{item_id}/attachment', headers=auth_h(), body=attachment, deserialize=True)
    else:
        response = await crud.create_attachment(item_id, attachment)
    return response


async def get_attachments(item_id: int) -> list[dict[str, Any]]:
    if Storage.is_remote():
        response = await aiorequest.get(f'/item/{item_id}/attachments', headers=auth_h(), deserialize=True)
    else:
        response = await crud.get_attachments(item_id)
    return response


async def update_attachment(attachment_id: UUID, attachment: dict[str, Any]) -> dict[str, Any]:
    if Storage.is_remote():
        response = await aiorequest.put(f'/attachment/{attachment_id}', headers=auth_h(), body=attachment, deserialize=True)
    else:
        response = await crud.update_attachment(attachment_id, attachment)
    return response


async def delete_attachment(attachment_id: UUID) -> dict[str, Any]:
    if Storage.is_remote():
        response = await aiorequest.delete(f'/attachment/{attachment_id}', headers=auth_h(), deserialize=True)
    else:
        response = await crud.delete_attachment(attachment_id)
    return response


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
    with suppress(Exception):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{aiorequest.baseurl}/docs') as response:
                return response.status == 200
    return False


async def save_icon(icon: bytes | str) -> None:
    filename = f"{datetime.now().strftime('%d.%m.%Y %H-%M-%S')}.{EXTENSIONS.ICON}"
    with open(os.path.join(PATHS.ICONS, filename), 'wb') as file:
        file.write(icon)
