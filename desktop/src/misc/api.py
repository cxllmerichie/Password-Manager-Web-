from typing import Any
import requests
from loguru import logger


@logger.catch()
def clear_json(dictionary: dict[str, Any]) -> dict[str, Any]:
    def rule(value):
        if isinstance(value, bool):
            return True
        elif value is None:
            return False
        elif isinstance(value, str):
            return len(value)
    return {key: value for key, value in dictionary.items() if rule(value)}


URL_ROOT = 'http://127.0.0.1:8000'


@logger.catch()
def auth_headers(token: str) -> dict[str, Any]:
    return {'accept': 'application/json', 'Authorization': f'Bearer {token}'}


@logger.catch()
def create_user(user: dict[str, Any]):
    url = f'{URL_ROOT}/users/'
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    return requests.post(url=url, headers=headers, json=user).json()


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


@logger.catch()
def categories(token: str):
    url = f'{URL_ROOT}/categories/'
    return requests.get(url=url, headers=auth_headers(token)).json()


@logger.catch()
def create_category(category: dict[str, Any], token: str):
    url = f'{URL_ROOT}/categories/'
    return requests.post(url=url, headers=auth_headers(token), json=clear_json(category)).json()


@logger.catch()
def update_category(category_id: int, category: dict[str, Any], token: str):
    url = f'{URL_ROOT}/categories/{category_id}/'
    return requests.put(url=url, headers=auth_headers(token), json=clear_json(category)).json()
