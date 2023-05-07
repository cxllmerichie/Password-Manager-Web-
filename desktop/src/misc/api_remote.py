from typing import Any
import requests
from loguru import logger
from qcontextapi import CONTEXT
from qcontextapi.misc import utils

from .api_abstract import CacheAPI


class APIRemote(CacheAPI):
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
        response = requests.get(url=url, headers=self.auth_headers()).json()
        return super().cache_get_categories(response)

    @logger.catch()
    def create_category(self, category: dict[str, Any]) -> dict[str, Any]:
        url = f'{self.URL}/categories/'
        response = requests.post(url=url, headers=self.auth_headers(), json=utils.serializable(category)).json()
        return super().cache_create_category(response)

    @logger.catch()
    def get_category(self, category_id: str) -> dict[str, Any]:
        url = f'{self.URL}/categories/{category_id}/'
        response = requests.get(url=url, headers=self.auth_headers()).json()
        return super().cache_get_category(response)

    @logger.catch()
    def set_category_favourite(self, category_id: int, is_favourite: bool) -> dict[str, Any]:
        url = f'{self.URL}/categories/{category_id}/favourite/?is_favourite={is_favourite}'
        response = requests.put(url=url, headers=self.auth_headers()).json()
        return super().cache_update_category(response)

    @logger.catch()
    def update_category(self, category_id: int, category: dict[str, Any]) -> dict[str, Any]:
        url = f'{self.URL}/categories/{category_id}/'
        response = requests.put(url=url, headers=self.auth_headers(), json=utils.serializable(category)).json()
        return super().cache_update_category(response)

    @logger.catch()
    def delete_category(self, category_id: int) -> dict[str, Any]:
        url = f'{self.URL}/categories/{category_id}/'
        response = requests.delete(url=url, headers=self.auth_headers()).json()
        return super().cache_delete_category(response)

    # ITEMS
    @logger.catch()
    def create_item(self, category_id: int, item: dict[str, Any]) -> dict[str, Any]:
        url = f'{self.URL}/categories/{category_id}/items/'
        response = requests.post(url=url, headers=self.auth_headers(), json=utils.serializable(item)).json()
        return super().cache_create_item(response)

    @logger.catch()
    def delete_item(self, item_id: str) -> dict[str, Any]:
        url = f'{self.URL}/items/{item_id}/'
        response = requests.delete(url=url, headers=self.auth_headers()).json()
        return super().cache_delete_item(response)

    @logger.catch()
    def update_item(self, item_id: int, item: dict[str, Any]) -> dict[str, Any]:
        url = f'{self.URL}/items/{item_id}/'
        response = requests.put(url=url, headers=self.auth_headers(), json=utils.serializable(item, ['expires_at'])).json()
        return super().cache_update_item(response)

    @logger.catch()
    def set_item_favourite(self, item_id: int, is_favourite: bool) -> dict[str, Any]:
        url = f'{self.URL}/items/{item_id}/favourite/?is_favourite={is_favourite}'
        response = requests.put(url=url, headers=self.auth_headers()).json()
        return super().cache_update_item(response)

    # FIELDS
    @logger.catch()
    def add_field(self, item_id: int, field: dict[str, Any]) -> dict[str, Any]:
        url = f'{self.URL}/items/{item_id}/fields/'
        response = requests.post(url=url, headers=self.auth_headers(), json=field).json()
        return super().cache_add_field(item_id, response)

    @logger.catch()
    def update_field(self, field_id: int, field: dict[str, Any]) -> dict[str, Any]:
        url = f'{self.URL}/fields/{field_id}/'
        response = requests.put(url=url, headers=self.auth_headers(), json=field).json()
        return super().cache_update_field(response)

    @logger.catch()
    def delete_field(self, field_id: str) -> dict[str, Any]:
        url = f'{self.URL}/fields/{field_id}/'
        response = requests.delete(url=url, headers=self.auth_headers()).json()
        return super().cache_delete_field(response)

    # ATTACHMENT
    @logger.catch()
    def add_attachment(self, item_id: int, attachment: dict[str, Any]) -> dict[str, Any]:
        url = f'{self.URL}/items/{item_id}/attachments/'
        response = requests.post(url=url, headers=self.auth_headers(), json=attachment).json()
        return super().cache_add_attachment(item_id, response)

    @logger.catch()
    def update_attachment(self, attachment_id: int, attachment: dict[str, Any]) -> dict[str, Any]:
        url = f'{self.URL}/attachments/{attachment_id}/'
        response = requests.put(url=url, headers=self.auth_headers(), json=attachment).json()
        return super().cache_update_attachment(response)

    @logger.catch()
    def delete_attachment(self, attachment_id: str) -> dict[str, Any]:
        url = f'{self.URL}/attachments/{attachment_id}/'
        response = requests.delete(url=url, headers=self.auth_headers()).json()
        return super().cache_delete_attachment(response)
