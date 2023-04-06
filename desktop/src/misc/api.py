from typing import Any
import requests


class API:
    root = 'http://127.0.0.1:8000'
    header_json = {"accept": "application/json", "Content-Type": "application/json"}

    @staticmethod
    def create_user(body: dict[str, Any]):
        url = f'{API.root}/users/'
        headers = API.header_json
        return requests.post(url=url, headers=headers, json=body).json()

    @staticmethod
    def login(body: dict[str, Any]):
        url = f'{API.root}/auth/token/'
        headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
        data = f'grant_type=&username={body["email"]}&password={body["password"]}&scope=&client_id=&client_secret='
        return requests.post(url=url, headers=headers, data=data).json()

    @staticmethod
    def check_email(email: str) -> bool:
        url = f'{API.root}/auth/{email}/'
        headers = {'accept': 'application/json'}
        return requests.get(url=url, headers=headers).json()

    @staticmethod
    def categories(token: str):
        url = f'{API.root}/categories/'
        headers = {'accept': 'application/json', 'Authorization': f'Bearer {token}'}
        return requests.get(url=url, headers=headers).json()
