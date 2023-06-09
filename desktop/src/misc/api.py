from aioqui.misc.utils import serializable, find
from aioqui.misc.aiorequest import request
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
from . import crud


class Api:
    class Storage:
        LOCAL = 'local'
        REMOTE = 'remote'
        HYBRID = 'hybrid'

    @staticmethod
    def local():
        return CONTEXT['storage'] == Api.Storage.LOCAL

    @staticmethod
    def remote():
        return CONTEXT['storage'] == Api.Storage.REMOTE

    def __init__(self):
        request.base_url = self.URL

    URL: str = 'https://pmapi.cxllmerichie.com/'

    __categories: list[dict[str, Any]] = None
    __category: dict[str, Any] = None
    __item: dict[str, Any] = None
    field_identifiers: list[str] = []
    attachment_identifiers: list[str] = []

    # PROPERTIES
    @property
    def categories(self) -> list[dict[str, Any]]:
        return self.__categories

    @categories.setter
    def categories(self, categories: list[dict[str, Any]]):
        self.__categories = categories

    @property
    def item(self) -> dict[str, Any]:
        return self.__item

    @item.setter
    def item(self, item: dict[str, Any]):
        self.__item = item

    @property
    def category(self):
        if not self.__category and self.item:
            for index, item in enumerate(self.categories):
                if item.get('id') == self.item['category_id']:
                    self.__category = self.categories[index]
                    break
        return self.__category

    @category.setter
    def category(self, category: dict[str | Any]):
        self.__category = category

    @property
    def items(self) -> list[dict[str, Any]]:
        return self.category['items']

    # GENERAL
    @property
    def headers_auth(self) -> dict[str, Any]:
        return self.headers_accept_json | {'Authorization': f"Bearer {CONTEXT['token']}"}

    @property
    def headers_accept_json(self) -> dict[str, Any]:
        return {'accept': 'application/json'}

    @property
    def headers_content_json(self) -> dict[str, Any]:
        return {'Content-Type': 'application/json'}

    @property
    def headers_login(self) -> dict[str, Any]:
        return self.headers_accept_json | {'Content-Type': 'application/x-www-form-urlencoded'}

    # AUTH
    async def login(self, auth_data: dict[str, Any]) -> dict[str, Any]:
        params = dict(username=auth_data['email'], password=auth_data['password'],
                      grant_type='', scope='', client_id='', client_secret='')
        response = await request('post', '/auth/token/', headers=self.headers_login, data=params)
        if token := response.get('access_token'):
            CONTEXT['token'] = token
        return response

    async def check_email(self, email: str) -> bool:
        return await request('get', f'/auth/{email}/', headers=self.headers_accept_json)

    # USER
    async def create_user(self, user: dict[str, Any]) -> dict[str, Any]:
        response = await request('post', '/users/', headers=self.headers_accept_json | self.headers_content_json, body=user)
        if token := response.get('access_token'):
            CONTEXT['token'] = token
        return response

    # CATEGORIES
    async def get_categories(self) -> list[dict[str, Any]]:
        if self.remote():
            response = await request('get', '/categories/', headers=self.headers_auth)
        else:
            response = await crud.get_categories()
        self.__categories = response
        return response

    async def create_category(self, category: dict[str, Any]) -> dict[str, Any]:
        if self.remote():
            response = await request('post', '/categories/', headers=self.headers_auth, body=await serializable(category))
        else:
            response = await crud.create_category(category)
        if category_id := response.get('id'):
            self.__categories.append(response)
            self.category = response
        return response

    async def get_category(self, category_id: int) -> dict[str, Any]:
        if self.remote():
            response = await request('get', f'/categories/{category_id}/', headers=self.headers_auth)
        else:
            response = await crud.get_category(category_id)
        if category_id := response.get('id'):
            c_idx, _ = await find(self.categories, 'id', category_id)
            self.category = self.categories[c_idx] = response
        return response

    async def set_category_favourite(self, category_id: int, is_favourite: bool) -> dict[str, Any]:
        if self.remote():
            response = await request('put', f'/categories/{category_id}/favourite/', headers=self.headers_auth, params=dict(is_favourite=is_favourite))
        else:
            response = await crud.set_category_favourite(category_id, is_favourite)
        if category_id := response.get('id'):
            c_idx, _ = await find(self.categories, 'id', category_id)
            self.category = self.categories[c_idx] = response
        return response

    async def update_category(self, category_id: int, category: dict[str, Any]) -> dict[str, Any]:
        if self.remote():
            response = await request('put', f'/categories/{category_id}/', headers=self.headers_auth, body=await serializable(category))
        else:
            response = await crud.update_category(category_id, category)
        if category_id := response.get('id'):
            c_idx, _ = await find(self.categories, 'id', category_id)
            self.category = self.categories[c_idx] = response
        return response

    async def delete_category(self, category_id: int) -> dict[str, Any]:
        if self.remote():
            response = await request('delete', f'/categories/{category_id}/', headers=self.headers_auth)
        else:
            response = await crud.delete_category(category_id)
        if category_id := response.get('id'):
            c_idx, _ = await find(self.categories, 'id', category_id)
            self.categories.pop(c_idx)
            self.category = self.item = None
        return response

    # ITEMS
    async def create_item(self, category_id: int, item: dict[str, Any]) -> dict[str, Any]:
        if self.remote():
            response = await request('post', f'/categories/{category_id}/items/', headers=self.headers_auth, body=await serializable(item))
        else:
            response = await crud.create_item(category_id, item)
        if item_id := response.get('id'):
            c_idx, _ = await find(self.categories, 'id', self.category['id'])
            self.categories[c_idx]['items'].append(response)
            self.item = response
        return response

    async def delete_item(self, item_id: int) -> dict[str, Any]:
        if self.remote():
            response = await request('delete', f'/items/{item_id}/', headers=self.headers_auth)
        else:
            response = await crud.delete_item(item_id)
        if item_id := response.get('id'):
            c_idx, _ = await find(self.categories, 'id', self.item['category_id'])
            i_idx, _ = await find(self.categories[c_idx]['items'], 'id', item_id)
            self.categories[c_idx]['items'].pop(i_idx)
            self.item = None
        return response

    async def update_item(self, item_id: int, item: dict[str, Any]) -> dict[str, Any]:
        if self.remote():
            response = await request('put', f'/items/{item_id}/', headers=self.headers_auth, body=await serializable(item, ['expires_at']))
        else:
            response = await crud.update_item(item_id, item)
        if item_id := response.get('id'):
            c_idx, _ = await find(self.categories, 'id', self.item['category_id'])
            i_idx, _ = await find(self.categories[c_idx]['items'], 'id', item_id)
            self.item = self.__categories[c_idx]['items'][i_idx] = response
        return response

    async def set_item_favourite(self, item_id: int, is_favourite: bool) -> dict[str, Any]:
        if self.remote():
            response = await request('put', f'/items/{item_id}/favourite/', headers=self.headers_auth, params=dict(is_favourite=is_favourite))
        else:
            response = await crud.set_item_favourite(item_id, is_favourite)
        if item_id := response.get('id'):
            c_idx, _ = await find(self.categories, 'id', self.item['category_id'])
            i_idx, _ = await find(self.categories[c_idx]['items'], 'id', item_id)
            self.item = self.__categories[c_idx]['items'][i_idx] = response
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
        created_item = await self.create_item(self.category['id'], await serializable(item))
        if item_id := created_item.get('id'):
            for field in fields:
                await self.add_field(item_id, field)
            for attachment in attachments:
                await self.add_attachment(item_id, await self.get_attachment_data(attachment['file']))
        return created_item

    # FIELDS
    async def add_field(self, item_id: int, field: dict[str, Any]) -> dict[str, Any]:
        if self.remote():
            response = await request('post', f'/items/{item_id}/fields/', headers=self.headers_auth, body=field)
        else:
            response = await crud.create_field(item_id, field)
        if field_id := response.get('id'):
            c_idx, _ = await find(self.categories, 'id', self.item['category_id'])
            i_idx, _ = await find(self.items, 'id', item_id)
            self.categories[c_idx]['items'][i_idx]['fields'].append(response)
            self.item = self.categories[c_idx]['items'][i_idx]
        return response

    async def update_field(self, field_id: UUID, field: dict[str, Any]) -> dict[str, Any]:
        if self.remote():
            response = await request('put', f'/fields/{field_id}/', headers=self.headers_auth, body=field)
        else:
            response = await crud.update_field(field_id, field)
        if field_id := response.get('id'):
            c_idx, _ = await find(self.categories, 'id', self.item['category_id'])
            i_idx, _ = await find(self.items, 'id', response['item_id'])
            f_idx, _ = await find(self.items[i_idx]['fields'], 'id', field_id)
            self.categories[c_idx]['items'][i_idx]['fields'][f_idx] = response
            self.item = self.categories[c_idx]['items'][i_idx]
        return response

    async def delete_field(self, field_id: UUID) -> dict[str, Any]:
        if self.remote():
            response = await request('delete', f'/fields/{field_id}/', headers=self.headers_auth)
        else:
            response = await crud.delete_field(field_id)
        if field_id := response.get('id'):
            c_idx, _ = await find(self.categories, 'id', self.item['category_id'])
            i_idx, _ = await find(self.items, 'id', response['item_id'])
            self.categories[c_idx]['items'][i_idx]['fields'].remove(response)
            self.item = self.categories[c_idx]['items'][i_idx]
        return response

    # ATTACHMENT
    async def add_attachment(self, item_id: int, attachment: dict[str, Any]) -> dict[str, Any]:
        if self.remote():
            response = await request('post', f'/items/{item_id}/attachments/', headers=self.headers_auth, body=attachment)
        else:
            response = await crud.create_attachment(item_id, attachment)
        if attachment_id := response.get('id'):
            c_idx, _ = await find(self.categories, 'id', self.item['category_id'])
            i_idx, _ = await find(self.categories[c_idx]['items'], 'id', item_id)
            self.categories[c_idx]['items'][i_idx]['attachments'].append(response)
            self.item = self.categories[c_idx]['items'][i_idx]
        return response

    async def update_attachment(self, attachment_id: UUID, attachment: dict[str, Any]) -> dict[str, Any]:
        if self.remote():
            response = await request('put', f'/attachments/{attachment_id}/', headers=self.headers_auth, body=attachment)
        else:
            response = await crud.update_attachment(attachment_id, attachment)
        if attachment_id := response.get('id'):
            i_idx, _ = await find(self.items, 'id', response['item_id'])
            c_idx, _ = await find(self.categories, 'id', self.items[i_idx]['category_id'])
            a_idx, _ = await find(self.items[i_idx]['attachments'], 'id', attachment_id)
            self.categories[c_idx]['items'][i_idx]['attachments'][a_idx] = response
            self.item = self.categories[c_idx]['items'][i_idx]
        return response

    async def delete_attachment(self, attachment_id: UUID) -> dict[str, Any]:
        if self.remote():
            response = await request('delete', f'/attachments/{attachment_id}/', headers=self.headers_auth)
        else:
            response = await crud.delete_attachment(attachment_id)
        if attachment_id := response.get('id'):
            i_idx, _ = await find(self.items, 'id', response['item_id'])
            c_idx, _ = await find(self.categories, 'id', self.items[i_idx]['category_id'])
            self.categories[c_idx]['items'][i_idx]['attachments'].remove(response)
            self.item = self.categories[c_idx]['items'][i_idx]
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
            async with session.get(f'{self.URL}/docs') as response:
                return response.status == 200

    async def save_icon(self, icon: bytes | str) -> None:
        filename = f"{datetime.now().strftime('%d.%m.%Y %H-%M-%S')}.{EXTENSIONS.ICON}"
        with open(os.path.join(PATHS.ICONS, filename), 'wb') as file:
            file.write(eval(icon))
