from aioqui.misc.aiorequest import request
from .utils import find, prepare
from mimetypes import MimeTypes
from datetime import datetime
from aioqui.types import Icon
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


class Api:
    def __init__(self):
        request.baseurl = 'https://pmapi.cxllmerichie.com'

    fields: list[str] = []
    attachments: list[str] = []

    # AUTH
    async def login(self, auth_data: dict[str, Any]) -> dict[str, Any]:
        params = dict(username=auth_data['email'], password=auth_data['password'],
                      grant_type='', scope='', client_id='', client_secret='')
        response = await request.post('/auth/token/', headers=login_h(), data=params)
        if token := response.get('access_token'):
            CONTEXT['token'] = token
        return response

    async def check_email(self, email: str) -> bool:
        return await request.get(f'/auth/{email}/', headers=accept_h())

    # USER
    async def create_user(self, user: dict[str, Any]) -> dict[str, Any]:
        response = await request.post('/users/', headers=accept_content_h(), body=user)
        if token := response.get('access_token'):
            CONTEXT['token'] = token
        return response

    # CATEGORIES
    async def get_categories(self) -> list[dict[str, Any]]:
        if Storage.remote():
            response = await request.get('/categories/', headers=auth_h(), pythonize=True)
        else:
            response = await crud.get_categories()
        self.__categories = response
        return response

    async def create_category(self, category: dict[str, Any]) -> dict[str, Any]:
        if Storage.remote():
            response = await request.post('/categories/', headers=auth_h(), body=await prepare(category), pythonize=True)
        else:
            response = await crud.create_category(category)
        return response

    async def get_category(self, category_id: int) -> dict[str, Any]:
        if Storage.remote():
            response = await request.get(f'/categories/{category_id}/', headers=auth_h(), pythonize=True)
        else:
            response = await crud.get_category(category_id)
        return response

    async def set_category_favourite(self, category_id: int, is_favourite: bool) -> dict[str, Any]:
        if Storage.remote():
            response = await request.put(f'/categories/{category_id}/favourite/', headers=auth_h(), params=dict(is_favourite=is_favourite), pythonize=True)
        else:
            response = await crud.set_category_favourite(category_id, is_favourite)
        return response

    async def update_category(self, category_id: int, category: dict[str, Any]) -> dict[str, Any]:
        if Storage.remote():
            response = await request.put(f'/categories/{category_id}/', headers=auth_h(), body=await prepare(category), pythonize=True)
        else:
            response = await crud.update_category(category_id, category)
        return response

    async def delete_category(self, category_id: int) -> dict[str, Any]:
        if Storage.remote():
            response = await request.delete(f'/categories/{category_id}/', headers=auth_h(), pythonize=True)
        else:
            response = await crud.delete_category(category_id)
        return response

    # ITEMS
    async def create_item(self, category_id: int, item: dict[str, Any]) -> dict[str, Any]:
        if Storage.remote():
            response = await request.post(f'/categories/{category_id}/items/', headers=auth_h(), body=await prepare(item), pythonize=True)
        else:
            response = await crud.create_item(category_id, item)
        return response

    async def delete_item(self, item_id: int) -> dict[str, Any]:
        if Storage.remote():
            response = await request.delete(f'/items/{item_id}/', headers=auth_h(), pythonize=True)
        else:
            response = await crud.delete_item(item_id)
        return response

    async def update_item(self, item_id: int, item: dict[str, Any]) -> dict[str, Any]:
        if Storage.remote():
            response = await request.put(f'/items/{item_id}/', headers=auth_h(), body=await prepare(item, ['expires_at']), pythonize=True)
        else:
            response = await crud.update_item(item_id, item)
        return response

    async def set_item_favourite(self, item_id: int, is_favourite: bool) -> dict[str, Any]:
        if Storage.remote():
            response = await request.put(f'/items/{item_id}/favourite/', headers=auth_h(), params=dict(is_favourite=is_favourite), pythonize=True)
        else:
            response = await crud.set_item_favourite(item_id, is_favourite)
        return response

    async def export_item(self, directory: str) -> str:
        # create copy to manage dict keys later on
        item = deepcopy(self.item)
        # create sub dir in selected dir to save there all the data
        export_dir = os.path.join(directory, item['title'])
        attachments_dir = os.path.join(export_dir, 'attachments')
        os.makedirs(attachments_dir)
        # manage necessary keys to make human-readable *.json file
        item_pop_keys = ['icon', 'id', 'category_id']
        for key in item_pop_keys:
            item.pop(key)
        field_pop_keys = ['id', 'item_id']
        for index in range(len(item['fields'])):
            for key in field_pop_keys:
                item['fields'][index].pop(key)
        attachment_pop_keys = ['id', 'item_id', 'content', 'mime', 'filename']
        for index in range(len(item['attachments'])):
            filepath = os.path.abspath(os.path.join(attachments_dir, item['attachments'][index]['filename']))
            item['attachments'][index]['file'] = filepath
            await self.download_attachment(filepath, item['attachments'][index])
            for key in attachment_pop_keys:
                item['attachments'][index].pop(key)
        for key, value in item.items():
            if isinstance(value, datetime):
                item[key] = str(value)
        with open(os.path.join(export_dir, 'item.json'), 'w') as file:
            json.dump(item, file, indent=4)
        return export_dir

    async def import_item(self, filepath: str) -> dict[str, Any]:
        with open(filepath, 'r') as file:
            item = json.load(file)
        item_pop_keys = ['created_at', 'modified_at', 'fields', 'attachments']
        fields, attachments = item.get('fields', ()), item.get('attachments', ())
        for key in item_pop_keys:
            if key in item.keys():
                item.pop(key)
        created_item = await self.create_item(self.category['id'], await prepare(item))
        if item_id := created_item.get('id'):
            for field in fields:
                await self.add_field(item_id, field)
            for attachment in attachments:
                await self.add_attachment(item_id, await self.get_attachment_data(attachment['file']))
        return created_item

    # FIELDS
    async def add_field(self, item_id: int, field: dict[str, Any]) -> dict[str, Any]:
        if Storage.remote():
            response = await request.post(f'/items/{item_id}/fields/', headers=auth_h(), body=field, pythonize=True)
        else:
            response = await crud.create_field(item_id, field)
        return response

    async def update_field(self, field_id: UUID, field: dict[str, Any]) -> dict[str, Any]:
        if Storage.remote():
            response = await request.put(f'/fields/{field_id}/', headers=auth_h(), body=field, pythonize=True)
        else:
            response = await crud.update_field(field_id, field)
        return response

    async def delete_field(self, field_id: UUID) -> dict[str, Any]:
        if Storage.remote():
            response = await request.delete(f'/fields/{field_id}/', headers=auth_h(), pythonize=True)
        else:
            response = await crud.delete_field(field_id)
        return response

    # ATTACHMENT
    async def add_attachment(self, item_id: int, attachment: dict[str, Any]) -> dict[str, Any]:
        if Storage.remote():
            response = await request.post(f'/items/{item_id}/attachments/', headers=auth_h(), body=attachment, pythonize=True)
        else:
            response = await crud.create_attachment(item_id, attachment)
        return response

    async def update_attachment(self, attachment_id: UUID, attachment: dict[str, Any]) -> dict[str, Any]:
        if Storage.remote():
            response = await request.put(f'/attachments/{attachment_id}/', headers=auth_h(), body=attachment, pythonize=True)
        else:
            response = await crud.update_attachment(attachment_id, attachment)
        return response

    async def delete_attachment(self, attachment_id: UUID) -> dict[str, Any]:
        if Storage.remote():
            response = await request.delete(f'/attachments/{attachment_id}/', headers=auth_h(), pythonize=True)
        else:
            response = await crud.delete_attachment(attachment_id)
        return response

    async def download_attachment(self, filepath: str, attachment: dict[str, Any]):
        with open(filepath, 'wb') as file:
            file.write(eval(attachment['content']))

    async def get_attachment_data(self, filepath: str) -> dict[str, Any]:
        mime = MimeTypes().guess_type(filepath)[0]
        if mime == 'image/jpeg':
            with open(filepath, 'rb') as file:
                content = str(Icon.bytes(Icon(file.read()).icon))
        elif mime == 'text/plain':
            with open(filepath, 'rb') as file:
                content = str(file.read())
        return {'content': content, 'filename': os.path.basename(filepath), 'mime': mime}

    # UTILS
    async def is_connected(self) -> bool:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{request.baseurl}/docs') as response:
                return response.status == 200

    async def save_icon(self, icon: bytes | str) -> None:
        filename = f"{datetime.now().strftime('%d.%m.%Y %H-%M-%S')}.{EXTENSIONS.ICON}"
        with open(os.path.join(PATHS.ICONS, filename), 'wb') as file:
            file.write(icon)
