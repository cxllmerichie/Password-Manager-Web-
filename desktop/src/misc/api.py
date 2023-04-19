from typing import Any
import requests
from loguru import logger

from ..widgets import ui
from .utils import clear_json


URL_ROOT = 'http://127.0.0.1:8000'


# GENERAL
@logger.catch()
def auth_headers() -> dict[str, Any]:
    return {'accept': 'application/json', 'Authorization': f'Bearer {ui.token}'}


# AUTH
@logger.catch()
def login(auth_data: dict[str, Any]):
    url = f'{URL_ROOT}/auth/token/'
    headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
    data = f'grant_type=&username={auth_data["email"]}&password={auth_data["password"]}&scope=&client_id=&client_secret='
    return requests.post(url=url, headers=headers, data=data).json()


@logger.catch()
def check_email(email: str) -> bool:
    url = f'{URL_ROOT}/auth/{email}/'
    headers = {'accept': 'application/json'}
    return requests.get(url=url, headers=headers).json()


# USER
@logger.catch()
def create_user(user: dict[str, Any]):
    url = f'{URL_ROOT}/users/'
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    return requests.post(url=url, headers=headers, json=user).json()


# CATEGORY
@logger.catch()
def get_categories():
    url = f'{URL_ROOT}/categories/'
    return requests.get(url=url, headers=auth_headers()).json()


@logger.catch()
def create_category(category: dict[str, Any]):
    url = f'{URL_ROOT}/categories/'
    return requests.post(url=url, headers=auth_headers(), json=clear_json(category)).json()


@logger.catch()
def get_category(category_id: str):
    url = f'{URL_ROOT}/categories/{category_id}/'
    return requests.get(url=url, headers=auth_headers()).json()


@logger.catch()
def update_category(category_id: int, category: dict[str, Any]):
    url = f'{URL_ROOT}/categories/{category_id}/'
    return requests.put(url=url, headers=auth_headers(), json=clear_json(category)).json()


@logger.catch()
def delete_category(category_id: int):
    url = f'{URL_ROOT}/categories/{category_id}/'
    return requests.delete(url=url, headers=auth_headers()).json()


# FIELD
@logger.catch()
def add_field(item_id: int, field: dict[str, Any]):
    url = f'{URL_ROOT}/items/{item_id}/fields/'
    return requests.post(url=url, headers=auth_headers(), json=field).json()


@logger.catch()
def update_field(field_id: int, field: dict[str, Any]):
    url = f'{URL_ROOT}/fields/{field_id}/'
    return requests.put(url=url, headers=auth_headers(), json=field).json()


@logger.catch()
def remove_field(field_id: str):
    url = f'{URL_ROOT}/fields/{field_id}/'
    return requests.delete(url=url, headers=auth_headers()).json()


# ITEM
@logger.catch()
def create_item(category_id: int, item: dict[str, Any], fields: list[dict[str, Any]]):
    url = f'{URL_ROOT}/categories/{category_id}/items/'
    response = requests.post(url=url, headers=auth_headers(), json=clear_json(item)).json()
    response['fields'] = []
    for field in fields:
        if (f := add_field(response['id'], field)).get('id', None):
            response['fields'].append(f)
    return response

@logger.catch()
def delete_item(item_id: str):
    url = f'{URL_ROOT}/items/{item_id}/'
    return requests.delete(url=url, headers=auth_headers()).json()


@logger.catch()
def get_item(item_id: str):
    url = f'{URL_ROOT}/items/{item_id}/'
    return requests.get(url=url, headers=auth_headers()).json()


@logger.catch()
def get_items(category_id: str):
    url = f'{URL_ROOT}/categories/{category_id}/items/'
    return requests.get(url=url, headers=auth_headers()).json()


@logger.catch()
def update_item(item_id: int, item: dict[str, Any]):
    url = f'{URL_ROOT}/items/{item_id}/'
    return requests.put(url=url, headers=auth_headers(), json=clear_json(item)).json()
