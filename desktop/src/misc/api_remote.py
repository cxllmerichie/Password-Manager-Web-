from typing import Any
import requests as _requests
from loguru import logger as _logger
from qcontextapi import CONTEXT as _CONTEXT

from .utils import clear_json


class Api:
    URL = 'http://127.0.0.1:8000'

    user: dict[str, Any] = None
    __categories: list[dict[str, Any]] = None
    __category: dict[str, Any] = None
    item: dict[str, Any] = None
    field_identifiers = []

    # PROPERTIES
    @property
    def categories(self) -> list[dict[str, Any]]:
        if not self.__categories:
            self.get_categories()
        return self.__categories

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
    @_logger.catch()
    def auth_headers(self) -> dict[str, Any]:
        return {'accept': 'application/json', 'Authorization': f'Bearer {_CONTEXT["token"]}'}

    # AUTH
    @_logger.catch()
    def login(self, auth_data: dict[str, Any]) -> dict[str, Any]:
        url = f'{self.URL}/auth/token/'
        headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
        data = f'grant_type=&username={auth_data["email"]}&password={auth_data["password"]}&scope=&client_id=&client_secret='
        return _requests.post(url=url, headers=headers, data=data).json()

    @_logger.catch()
    def check_email(self, email: str) -> bool:
        url = f'{self.URL}/auth/{email}/'
        headers = {'accept': 'application/json'}
        return _requests.get(url=url, headers=headers).json()

    # USER
    @_logger.catch()
    def create_user(self, user: dict[str, Any]) -> dict[str, Any]:
        url = f'{self.URL}/users/'
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        response = _requests.post(url=url, headers=headers, json=user).json()
        if response.get('id'):
            self.user = response
        return response

    # CATEGORIES
    @_logger.catch()
    def get_categories(self) -> list[dict[str, Any]]:
        url = f'{self.URL}/categories/'
        self.__categories = _requests.get(url=url, headers=self.auth_headers()).json()
        return self.__categories

    @_logger.catch()
    def create_category(self, category: dict[str, Any]) -> dict[str, Any]:
        url = f'{self.URL}/categories/'
        response = _requests.post(url=url, headers=self.auth_headers(), json=clear_json(category)).json()
        if category_id := response.get('id'):
            self.get_categories()
            self.category = response
        return response

    @_logger.catch()
    def get_category(self, category_id: str) -> dict[str, Any]:
        url = f'{self.URL}/categories/{category_id}/'
        response = _requests.get(url=url, headers=self.auth_headers()).json()
        if category_id := response.get('id'):
            self.get_categories()
            self.category = response
        return response

    @_logger.catch()
    def set_category_favourite(self, category_id: int, is_favourite: bool) -> dict[str, Any]:
        url = f'{self.URL}/categories/{category_id}/favourite/?is_favourite={is_favourite}'
        response = _requests.put(url=url, headers=self.auth_headers()).json()
        if category_id := response.get('id'):
            self.get_categories()
            self.category = response
        return response

    @_logger.catch()
    def update_category(self, category_id: int, category: dict[str, Any]) -> dict[str, Any]:
        url = f'{self.URL}/categories/{category_id}/'
        response = _requests.put(url=url, headers=self.auth_headers(), json=clear_json(category)).json()
        if category_id := response.get('id'):
            self.get_categories()
            self.category = response
        return response

    @_logger.catch()
    def delete_category(self, category_id: int) -> dict[str, Any]:
        url = f'{self.URL}/categories/{category_id}/'
        response = _requests.delete(url=url, headers=self.auth_headers()).json()
        if category_id := response.get('id'):
            self.get_categories()  # might be changed to simple list.remove(deleted_category)
            self.category = None
            self.item = None
        return response

    # FIELDS
    @_logger.catch()
    def add_field(self, item_id: int, field: dict[str, Any]) -> dict[str, Any]:
        url = f'{self.URL}/items/{item_id}/fields/'
        return _requests.post(url=url, headers=self.auth_headers(), json=field).json()

    @_logger.catch()
    def update_field(self, field_id: int, field: dict[str, Any]) -> dict[str, Any]:
        url = f'{self.URL}/fields/{field_id}/'
        return _requests.put(url=url, headers=self.auth_headers(), json=field).json()

    @_logger.catch()
    def remove_field(self, field_id: str) -> dict[str, Any]:
        url = f'{self.URL}/fields/{field_id}/'
        return _requests.delete(url=url, headers=self.auth_headers()).json()

    # ITEMS
    @_logger.catch()
    def create_item(self, category_id: int, item: dict[str, Any], fields: list[dict[str, Any]]) -> dict[str, Any]:
        url = f'{self.URL}/categories/{category_id}/items/'
        response = _requests.post(url=url, headers=self.auth_headers(), json=clear_json(item)).json()
        if item_id := response.get('id'):
            response['fields'] = []
            for field in fields:
                if (f := self.add_field(item_id, field)).get('id', None):
                    response['fields'].append(f)
            self.get_categories()
            self.item = response
        return response

    @_logger.catch()
    def delete_item(self, item_id: str) -> dict[str, Any]:
        url = f'{self.URL}/items/{item_id}/'
        response = _requests.delete(url=url, headers=self.auth_headers()).json()
        if item_id := response.get('id'):
            self.get_categories()
            self.item = None
        return response

    @_logger.catch()
    def get_item(self, item_id: str) -> dict[str, Any]:
        url = f'{self.URL}/items/{item_id}/'
        return _requests.get(url=url, headers=self.auth_headers()).json()

    @_logger.catch()
    def update_item(self, item_id: int, item: dict[str, Any]) -> dict[str, Any]:
        url = f'{self.URL}/items/{item_id}/'
        response = _requests.put(url=url, headers=self.auth_headers(), json=clear_json(item, ['expires_at'])).json()
        if item_id := response.get('id'):
            self.get_categories()
            self.item = response
        return response

    @_logger.catch()
    def set_item_favourite(self, item_id: int, is_favourite: bool) -> dict[str, Any]:
        url = f'{self.URL}/items/{item_id}/favourite/?is_favourite={is_favourite}'
        response = _requests.put(url=url, headers=self.auth_headers()).json()
        if item_id := response.get('id'):
            self.get_categories()
            self.item = response
        return response


API = Api()
