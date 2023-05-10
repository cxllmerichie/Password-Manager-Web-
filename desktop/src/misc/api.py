from qcontextapi.misc import utils, Icon
from qcontextapi import CONTEXT
from mimetypes import MimeTypes
from datetime import datetime
from copy import deepcopy
from loguru import logger
from typing import Any
from uuid import UUID
import ujson as json
import requests
import os

from . import crud
from .utils import Storage


class Api:
    URL = 'http://127.0.0.1:8000'
    __categories: list[dict[str, Any]] = None
    __category: dict[str, Any] = None
    __item: dict[str, Any] = None
    field_identifiers: list[UUID] = []
    attachment_identifiers: list[UUID] = []

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
    @logger.catch()
    def auth_headers(self) -> dict[str, Any]:
        return {'accept': 'application/json', 'Authorization': f'Bearer {CONTEXT["token"]}'}

    # AUTH
    @logger.catch()
    async def login(self, auth_data: dict[str, Any]) -> dict[str, Any]:
        url = f'{self.URL}/auth/token/'
        headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
        data = f'grant_type=&username={auth_data["email"]}&password={auth_data["password"]}&scope=&client_id=&client_secret='
        response = requests.post(url=url, headers=headers, data=data).json()
        if token := response.get('access_token'):
            CONTEXT['token'] = token
        return response

    @logger.catch()
    async def check_email(self, email: str) -> bool:
        url = f'{self.URL}/auth/{email}/'
        headers = {'accept': 'application/json'}
        return requests.get(url=url, headers=headers).json()

    # USER
    @logger.catch()
    async def create_user(self, user: dict[str, Any]) -> dict[str, Any]:
        url = f'{self.URL}/users/'
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        response = requests.post(url=url, headers=headers, json=user).json()
        if token := response.get('access_token'):
            CONTEXT['token'] = token
        return response

    # CATEGORIES
    @logger.catch()
    async def get_categories(self) -> list[dict[str, Any]]:
        if CONTEXT['storage'] == Storage.REMOTE:
            url = f'{self.URL}/categories/'
            response = requests.get(url=url, headers=self.auth_headers()).json()
        else:
            response = await crud.get_categories()
        self.__categories = response
        return response

    @logger.catch()
    async def create_category(self, category: dict[str, Any]) -> dict[str, Any]:
        if CONTEXT['storage'] == Storage.REMOTE:
            url = f'{self.URL}/categories/'
            response = requests.post(url=url, headers=self.auth_headers(), json=await utils.serializable(category)).json()
        else:
            response = await crud.create_category(await utils.serializable(category))
        if category_id := response.get('id'):
            self.__categories.append(response)
            self.category = response
        return response

    @logger.catch()
    async def get_category(self, category_id: str) -> dict[str, Any]:
        if CONTEXT['storage'] == Storage.REMOTE:
            url = f'{self.URL}/categories/{category_id}/'
            response = requests.get(url=url, headers=self.auth_headers()).json()
        else:
            response = await crud.get_category(int(category_id))
        if category_id := response.get('id'):
            c_idx, _ = await utils.find(self.categories, 'id', category_id)
            self.category = self.categories[c_idx] = response
        return response

    @logger.catch()
    async def set_category_favourite(self, category_id: int, is_favourite: bool) -> dict[str, Any]:
        if CONTEXT['storage'] == Storage.REMOTE:
            url = f'{self.URL}/categories/{category_id}/favourite/?is_favourite={is_favourite}'
            response = requests.put(url=url, headers=self.auth_headers()).json()
        else:
            response = await crud.set_category_favourite(int(category_id), is_favourite)
        if category_id := response.get('id'):
            c_idx, _ = await utils.find(self.categories, 'id', category_id)
            self.category = self.categories[c_idx] = response
        return response

    @logger.catch()
    async def update_category(self, category_id: int, category: dict[str, Any]) -> dict[str, Any]:
        if CONTEXT['storage'] == Storage.REMOTE:
            url = f'{self.URL}/categories/{category_id}/'
            response = requests.put(url=url, headers=self.auth_headers(), json=await utils.serializable(category)).json()
        else:
            response = await crud.update_category(int(category_id), await utils.serializable(category))
        if category_id := response.get('id'):
            c_idx, _ = await utils.find(self.categories, 'id', category_id)
            self.category = self.categories[c_idx] = response
        return response

    @logger.catch()
    async def delete_category(self, category_id: int) -> dict[str, Any]:
        if CONTEXT['storage'] == Storage.REMOTE:
            url = f'{self.URL}/categories/{category_id}/'
            response = requests.delete(url=url, headers=self.auth_headers()).json()
        else:
            response = await crud.delete_category(int(category_id))
        if category_id := response.get('id'):
            c_idx, _ = await utils.find(self.categories, 'id', category_id)
            self.categories.pop(c_idx)
            self.category = self.item = None
        return response

    # ITEMS
    @logger.catch()
    async def create_item(self, category_id: int, item: dict[str, Any]) -> dict[str, Any]:
        if CONTEXT['storage'] == Storage.REMOTE:
            url = f'{self.URL}/categories/{category_id}/items/'
            response = requests.post(url=url, headers=self.auth_headers(), json=await utils.serializable(item)).json()
        else:
            response = await crud.create_item(int(category_id), await utils.serializable(item))
        if item_id := response.get('id'):
            c_idx, _ = await utils.find(self.categories, 'id', self.category['id'])
            self.categories[c_idx]['items'].append(response)
            self.item = response
        return response

    @logger.catch()
    async def delete_item(self, item_id: str) -> dict[str, Any]:
        if CONTEXT['storage'] == Storage.REMOTE:
            url = f'{self.URL}/items/{item_id}/'
            response = requests.delete(url=url, headers=self.auth_headers()).json()
        else:
            response = await crud.delete_item(int(item_id))
        if item_id := response.get('id'):
            c_idx, _ = await utils.find(self.categories, 'id', self.item['category_id'])
            i_idx, _ = await utils.find(self.categories[c_idx]['items'], 'id', item_id)
            self.categories[c_idx]['items'].pop(i_idx)
            self.item = None
        return response

    @logger.catch()
    async def update_item(self, item_id: int, item: dict[str, Any]) -> dict[str, Any]:
        if CONTEXT['storage'] == Storage.REMOTE:
            url = f'{self.URL}/items/{item_id}/'
            response = requests.put(url=url, headers=self.auth_headers(), json=await utils.serializable(item, ['expires_at'])).json()
        else:
            response = await crud.update_item(int(item_id), await utils.serializable(item, ['expires_at']))
        if item_id := response.get('id'):
            c_idx, _ = await utils.find(self.categories, 'id', self.item['category_id'])
            i_idx, _ = await utils.find(self.categories[c_idx]['items'], 'id', item_id)
            self.item = self.categories[c_idx]['items'][i_idx] = response
        return response

    @logger.catch()
    async def set_item_favourite(self, item_id: int, is_favourite: bool) -> dict[str, Any]:
        if CONTEXT['storage'] == Storage.REMOTE:
            url = f'{self.URL}/items/{item_id}/favourite/?is_favourite={is_favourite}'
            response = requests.put(url=url, headers=self.auth_headers()).json()
        else:
            response = await crud.set_item_favourite(int(item_id), is_favourite)
        if item_id := response.get('id'):
            c_idx, _ = await utils.find(self.categories, 'id', self.item['category_id'])
            i_idx, _ = await utils.find(self.categories[c_idx]['items'], 'id', item_id)
            self.item = self.categories[c_idx]['items'][i_idx] = response
        return response

    @logger.catch()
    async def export_item(self, directory: str) -> None:
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

    @logger.catch()
    async def import_item(self, filepath: str) -> dict[str, Any]:
        with open(filepath, 'r') as file:
            item = json.load(file)
        item_pop_keys = ['created_at', 'modified_at', 'fields', 'attachments']
        fields, attachments = item['fields'], item['attachments']
        for key in item_pop_keys:
            item.pop(key)
        created_item = await self.create_item(self.category['id'], await utils.serializable(item))
        if item_id := created_item.get('id'):
            for field in fields:
                await self.add_field(item_id, field)
            for attachment in attachments:
                await self.add_attachment(item_id, await self.get_attachment_data(attachment['file']))
        return created_item

    # FIELDS
    @logger.catch()
    async def add_field(self, item_id: int, field: dict[str, Any]) -> dict[str, Any]:
        if CONTEXT['storage'] == Storage.REMOTE:
            url = f'{self.URL}/items/{item_id}/fields/'
            response = requests.post(url=url, headers=self.auth_headers(), json=field).json()
        else:
            response = await crud.create_field(int(item_id), field)
        if field_id := response.get('id'):
            c_idx, _ = await utils.find(self.categories, 'id', self.item['category_id'])
            i_idx, _ = await utils.find(self.items, 'id', item_id)
            self.categories[c_idx]['items'][i_idx]['fields'].append(response)
            self.item = self.categories[c_idx]['items'][i_idx]
        return response

    @logger.catch()
    async def update_field(self, field_id: int, field: dict[str, Any]) -> dict[str, Any]:
        if CONTEXT['storage'] == Storage.REMOTE:
            url = f'{self.URL}/fields/{field_id}/'
            response = requests.put(url=url, headers=self.auth_headers(), json=field).json()
        else:
            response = await crud.update_field(field_id, field)
        if field_id := response.get('id'):
            c_idx, _ = await utils.find(self.categories, 'id', self.item['category_id'])
            i_idx, _ = await utils.find(self.items, 'id', response['item_id'])
            f_idx, _ = await utils.find(self.items[i_idx]['fields'], 'id', field_id)
            self.categories[c_idx]['items'][i_idx]['fields'][f_idx] = response
            self.item = self.categories[c_idx]['items'][i_idx]
        return response

    @logger.catch()
    async def delete_field(self, field_id: str) -> dict[str, Any]:
        if CONTEXT['storage'] == Storage.REMOTE:
            url = f'{self.URL}/fields/{field_id}/'
            response = requests.delete(url=url, headers=self.auth_headers()).json()
        else:
            response = await crud.delete_field(field_id)
        if field_id := response.get('id'):
            c_idx, _ = await utils.find(self.categories, 'id', self.item['category_id'])
            i_idx, _ = await utils.find(self.items, 'id', response['item_id'])
            self.categories[c_idx]['items'][i_idx]['fields'].remove(response)
            self.item = self.categories[c_idx]['items'][i_idx]
        return response

    # ATTACHMENT
    @logger.catch()
    async def add_attachment(self, item_id: int, attachment: dict[str, Any]) -> dict[str, Any]:
        if CONTEXT['storage'] == Storage.REMOTE:
            url = f'{self.URL}/items/{item_id}/attachments/'
            response = requests.post(url=url, headers=self.auth_headers(), json=attachment).json()
        else:
            response = await crud.create_attachment(item_id, attachment)
        if attachment_id := response.get('id'):
            c_idx, _ = await utils.find(self.categories, 'id', self.item['category_id'])
            i_idx, _ = await utils.find(self.categories[c_idx]['items'], 'id', item_id)
            self.categories[c_idx]['items'][i_idx]['attachments'].append(response)
            self.item = self.categories[c_idx]['items'][i_idx]
        return response

    @logger.catch()
    async def update_attachment(self, attachment_id: int, attachment: dict[str, Any]) -> dict[str, Any]:
        if CONTEXT['storage'] == Storage.REMOTE:
            url = f'{self.URL}/attachments/{attachment_id}/'
            response = requests.put(url=url, headers=self.auth_headers(), json=attachment).json()
        else:
            response = await crud.update_attachment(attachment_id, attachment)
        if attachment_id := response.get('id'):
            i_idx, _ = await utils.find(self.items, 'id', response['item_id'])
            c_idx, _ = await utils.find(self.categories, 'id', self.items[i_idx]['category_id'])
            a_idx, _ = await utils.find(self.items[i_idx]['attachments'], 'id', attachment_id)
            self.categories[c_idx]['items'][i_idx]['attachments'][a_idx] = response
            self.item = self.categories[c_idx]['items'][i_idx]
        return response

    @logger.catch()
    async def delete_attachment(self, attachment_id: str) -> dict[str, Any]:
        if CONTEXT['storage'] == Storage.REMOTE:
            url = f'{self.URL}/attachments/{attachment_id}/'
            response = requests.delete(url=url, headers=self.auth_headers()).json()
        else:
            response = await crud.delete_attachment(attachment_id)
        if attachment_id := response.get('id'):
            i_idx, _ = await utils.find(self.items, 'id', response['item_id'])
            c_idx, _ = await utils.find(self.categories, 'id', self.items[i_idx]['category_id'])
            self.categories[c_idx]['items'][i_idx]['attachments'].remove(response)
            self.item = self.categories[c_idx]['items'][i_idx]
        return response

    @logger.catch()
    async def download_attachment(self, filepath: str, attachment: dict[str, Any]):
        with open(filepath, 'wb') as file:
            file.write(eval(attachment['content']))

    @logger.catch()
    async def get_attachment_data(self, filepath: str) -> dict[str, Any]:
        mime = MimeTypes().guess_type(filepath)[0]
        if mime == 'image/jpeg':
            with open(filepath, 'rb') as file:
                content = str(Icon.bytes(Icon(file.read()).icon))
        elif mime == 'text/plain':
            with open(filepath, 'rb') as file:
                content = str(file.read())
        return {'content': content, 'filename': os.path.basename(filepath), 'mime': mime}
