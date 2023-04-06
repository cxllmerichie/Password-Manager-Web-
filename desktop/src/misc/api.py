from typing import Any
import requests
from .utils import clear_json


URL_ROOT = 'http://127.0.0.1:8000'


def auth_headers(token: str) -> dict[str, Any]:
    return {'accept': 'application/json', 'Authorization': f'Bearer {token}'}


def create_user(body: dict[str, Any]):
    url = f'{URL_ROOT}/users/'
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    return requests.post(url=url, headers=headers, json=body).json()


def login(body: dict[str, Any]):
    url = f'{URL_ROOT}/auth/token/'
    headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
    data = f'grant_type=&username={body["email"]}&password={body["password"]}&scope=&client_id=&client_secret='
    return requests.post(url=url, headers=headers, data=data).json()


def check_email(email: str) -> bool:
    url = f'{URL_ROOT}/auth/{email}/'
    headers = {'accept': 'application/json'}
    return requests.get(url=url, headers=headers).json()


def categories(token: str):
    url = f'{URL_ROOT}/categories/'
    return requests.get(url=url, headers=auth_headers(token)).json()


def create_category(body: dict[str, Any], token: str):
    url = f'{URL_ROOT}/categories/'
    return requests.post(url=url, headers=auth_headers(token), json=clear_json(body))
