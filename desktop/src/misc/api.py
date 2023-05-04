from typing import Any
import requests
from loguru import logger
from qcontextapi import CONTEXT
from qcontextapi.misc import utils
from uuid import UUID
import ujson as json
from copy import copy


class Api:
    URL = 'http://127.0.0.1:8000'

    __categories: list[dict[str, Any]] = None
    __category: dict[str, Any] = None
    __item: dict[str, Any] = None
    field_identifiers: list[UUID] = []
    attachments: list[bytes] = []

    # PROPERTIES
    @property
    def categories(self) -> list[dict[str, Any]]:
        if not self.__categories:
            self.get_categories()
        return self.__categories

    @property
    def item(self) -> dict[str, Any]:
        return self.__item

    @item.setter
    def item(self, item: dict[str, Any]):
        self.__item = item

    @property
    def category(self):
        if not self.__category and self.item:
            self.__category = self.get_category(self.item['category_id'])
        return self.__category

    @category.setter
    def category(self, value: dict[str | Any]):
        self.__category = value

    @property
    def items(self) -> list[dict[str, Any]]:
        return self.category['items']

    # GENERAL
    @logger.catch()
    def auth_headers(self) -> dict[str, Any]:
        return {'accept': 'application/json', 'Authorization': f'Bearer {CONTEXT["token"]}'}

    # AUTH
    @logger.catch()
    def login(self, auth_data: dict[str, Any]) -> dict[str, Any]:
        url = f'{self.URL}/auth/token/'
        headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
        data = f'grant_type=&username={auth_data["email"]}&password={auth_data["password"]}&scope=&client_id=&client_secret='
        response = requests.post(url=url, headers=headers, data=data).json()
        if token := response.get('access_token'):
            CONTEXT['token'] = token
        return response

    @logger.catch()
    def check_email(self, email: str) -> bool:
        url = f'{self.URL}/auth/{email}/'
        headers = {'accept': 'application/json'}
        return requests.get(url=url, headers=headers).json()

    # USER
    @logger.catch()
    def create_user(self, user: dict[str, Any]) -> dict[str, Any]:
        url = f'{self.URL}/users/'
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        response = requests.post(url=url, headers=headers, json=user).json()
        if token := response.get('access_token'):
            CONTEXT['token'] = token
        return response

    # CATEGORIES
    @logger.catch()
    def get_categories(self) -> list[dict[str, Any]]:
        url = f'{self.URL}/categories/'
        self.__categories = requests.get(url=url, headers=self.auth_headers()).json()
        return self.__categories

    @logger.catch()
    def create_category(self, category: dict[str, Any]) -> dict[str, Any]:
        url = f'{self.URL}/categories/'
        response = requests.post(url=url, headers=self.auth_headers(), json=utils.serializable(category)).json()
        if category_id := response.get('id'):
            self.__categories.append(response)
            self.category = response
        return response

    @logger.catch()
    def get_category(self, category_id: str) -> dict[str, Any]:
        url = f'{self.URL}/categories/{category_id}/'
        response = requests.get(url=url, headers=self.auth_headers()).json()
        if category_id := response.get('id'):
            c_idx, _ = utils.find(self.categories, 'id', category_id)
            self.category = self.categories[c_idx] = response
        return response

    @logger.catch()
    def set_category_favourite(self, category_id: int, is_favourite: bool) -> dict[str, Any]:
        url = f'{self.URL}/categories/{category_id}/favourite/?is_favourite={is_favourite}'
        response = requests.put(url=url, headers=self.auth_headers()).json()
        if category_id := response.get('id'):
            c_idx, _ = utils.find(self.categories, 'id', category_id)
            self.category = self.categories[c_idx] = response
        return response

    @logger.catch()
    def update_category(self, category_id: int, category: dict[str, Any]) -> dict[str, Any]:
        url = f'{self.URL}/categories/{category_id}/'
        response = requests.put(url=url, headers=self.auth_headers(), json=utils.serializable(category)).json()
        if category_id := response.get('id'):
            c_idx, _ = utils.find(self.categories, 'id', category_id)
            self.category = self.categories[c_idx] = response
        return response

    @logger.catch()
    def delete_category(self, category_id: int) -> dict[str, Any]:
        url = f'{self.URL}/categories/{category_id}/'
        response = requests.delete(url=url, headers=self.auth_headers()).json()
        if category_id := response.get('id'):
            c_idx, _ = utils.find(self.categories, 'id', category_id)
            self.categories.pop(c_idx)
            self.category = self.item = None
        return response

    # FIELDS
    @logger.catch()
    def add_field(self, item_id: int, field: dict[str, Any]) -> dict[str, Any]:
        url = f'{self.URL}/items/{item_id}/fields/'
        response = requests.post(url=url, headers=self.auth_headers(), json=field).json()
        if field_id := response.get('id'):
            c_idx, _ = utils.find(self.categories, 'id', self.item['category_id'])
            i_idx, _ = utils.find(self.categories[c_idx]['items'], 'id', item_id)
            self.categories[c_idx]['items'][i_idx]['fields'].append(response)
            self.item = self.categories[c_idx]['items'][i_idx]
        return response

    @logger.catch()
    def update_field(self, field_id: int, field: dict[str, Any]) -> dict[str, Any]:
        url = f'{self.URL}/fields/{field_id}/'
        return requests.put(url=url, headers=self.auth_headers(), json=field).json()

    @logger.catch()
    def remove_field(self, field_id: str) -> dict[str, Any]:
        url = f'{self.URL}/fields/{field_id}/'
        return requests.delete(url=url, headers=self.auth_headers()).json()

    # ITEMS
    @logger.catch()
    def create_item(self, category_id: int, item: dict[str, Any]) -> dict[str, Any]:
        url = f'{self.URL}/categories/{category_id}/items/'
        response = requests.post(url=url, headers=self.auth_headers(), json=utils.serializable(item)).json()
        if item_id := response.get('id'):
            c_idx, _ = utils.find(self.categories, 'id', self.category['id'])
            self.categories[c_idx]['items'].append(response)
            self.item = response
        return response

    @logger.catch()
    def delete_item(self, item_id: str) -> dict[str, Any]:
        url = f'{self.URL}/items/{item_id}/'
        response = requests.delete(url=url, headers=self.auth_headers()).json()
        if item_id := response.get('id'):
            c_idx, _ = utils.find(self.categories, 'id', self.item['category_id'])
            i_idx, _ = utils.find(self.categories[c_idx]['items'], 'id', item_id)
            self.categories[c_idx]['items'].pop(i_idx)
            self.item = None
        return response

    @logger.catch()
    def update_item(self, item_id: int, item: dict[str, Any]) -> dict[str, Any]:
        url = f'{self.URL}/items/{item_id}/'
        response = requests.put(url=url, headers=self.auth_headers(), json=utils.serializable(item, ['expires_at'])).json()
        if item_id := response.get('id'):
            c_idx, _ = utils.find(self.categories, 'id', self.item['category_id'])
            i_idx, _ = utils.find(self.categories[c_idx]['items'], 'id', item_id)
            self.item = self.categories[c_idx]['items'][i_idx] = response
        return response

    @logger.catch()
    def set_item_favourite(self, item_id: int, is_favourite: bool) -> dict[str, Any]:
        url = f'{self.URL}/items/{item_id}/favourite/?is_favourite={is_favourite}'
        response = requests.put(url=url, headers=self.auth_headers()).json()
        if item_id := response.get('id'):
            c_idx, _ = utils.find(self.categories, 'id', self.item['category_id'])
            i_idx, _ = utils.find(self.categories[c_idx]['items'], 'id', item_id)
            self.item = self.categories[c_idx]['items'][i_idx] = response
        return response

    def export_item(self, filepath: str):
        item = copy(self.item)
        item_pop_keys = ['icon', 'attachments', 'id', 'category_id']
        for key in item_pop_keys:
            item.pop(key)
        field_pop_keys = ['id', 'item_id']
        for index in range(len(item['fields'])):
            for key in field_pop_keys:
                item['fields'][index].pop(key)
        with open(filepath, 'w') as file:
            json.dump(item, file, indent=4)

    def import_item(self, filepath: str):
        with open(filepath, 'r') as file:
            item = json.load(file)
        item_pop_keys = ['created_at', 'modified_at', 'fields']
        fields = item['fields']
        for key in item_pop_keys:
            item.pop(key)
        created_item = self.create_item(self.category['id'], utils.serializable(item))
        if item_id := created_item.get('id'):
            for field in fields:
                API.add_field(item_id, field)
        return created_item

    # ATTACHMENT
    def add_attachment(self, filepath: str):
        if item := API.item:
            with open(filepath, 'rb') as file:
                item['attachments'].append(file.read())
                API.update_item(API.item['id'], item)


API = Api()
