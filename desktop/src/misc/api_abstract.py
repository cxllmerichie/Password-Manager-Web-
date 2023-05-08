from datetime import datetime
from abc import abstractmethod
from typing import Any
from loguru import logger
from qcontextapi.misc import utils
from copy import deepcopy
import ujson as json
import os

from .api_cache import Cache


class CacheAPI(Cache):
    URL = 'http://127.0.0.1:8000'

    # CATEGORIES
    @abstractmethod
    @logger.catch()
    def get_categories(self) -> list[dict[str, Any]]:
        ...

    @abstractmethod
    @logger.catch()
    def create_category(self, category: dict[str, Any]) -> dict[str, Any]:
        ...

    @abstractmethod
    @logger.catch()
    def get_category(self, category_id: str) -> dict[str, Any]:
        ...

    @abstractmethod
    @logger.catch()
    def set_category_favourite(self, category_id: int, is_favourite: bool) -> dict[str, Any]:
        ...

    @abstractmethod
    @logger.catch()
    def update_category(self, category_id: int, category: dict[str, Any]) -> dict[str, Any]:
        ...

    @abstractmethod
    @logger.catch()
    def delete_category(self, category_id: int) -> dict[str, Any]:
        ...

    # FIELDS
    @abstractmethod
    @logger.catch()
    def add_field(self, item_id: int, field: dict[str, Any]) -> dict[str, Any]:
        ...

    @abstractmethod
    @logger.catch()
    def update_field(self, field_id: int, field: dict[str, Any]) -> dict[str, Any]:
        ...

    @abstractmethod
    @logger.catch()
    def delete_field(self, field_id: str) -> dict[str, Any]:
        ...

    # ITEMS
    @abstractmethod
    @logger.catch()
    def create_item(self, category_id: int, item: dict[str, Any]) -> dict[str, Any]:
        ...

    @abstractmethod
    @logger.catch()
    def delete_item(self, item_id: str) -> dict[str, Any]:
        ...

    @abstractmethod
    @logger.catch()
    def update_item(self, item_id: int, item: dict[str, Any]) -> dict[str, Any]:
        ...

    @abstractmethod
    @logger.catch()
    def set_item_favourite(self, item_id: int, is_favourite: bool) -> dict[str, Any]:
        ...

    @logger.catch()
    def export_item(self, directory: str) -> None:
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
            self.download_attachment(filepath, item['attachments'][index])
            for key in attachment_pop_keys:
                item['attachments'][index].pop(key)
        for key, value in item.items():
            if isinstance(value, datetime):
                item[key] = str(value)
        with open(os.path.join(export_dir, 'item.json'), 'w') as file:
            json.dump(item, file, indent=4)

    @logger.catch()
    def import_item(self, filepath: str) -> dict[str, Any]:
        with open(filepath, 'r') as file:
            item = json.load(file)
        item_pop_keys = ['created_at', 'modified_at', 'fields', 'attachments']
        fields = item['fields']
        for key in item_pop_keys:
            item.pop(key)
        created_item = self.create_item(self.category['id'], utils.serializable(item))
        if item_id := created_item.get('id'):
            for field in fields:
                self.add_field(item_id, field)
        return created_item

    # ATTACHMENT
    @abstractmethod
    @logger.catch()
    def add_attachment(self, item_id: int, attachment: dict[str, Any]) -> dict[str, Any]:
        ...

    @abstractmethod
    @logger.catch()
    def update_attachment(self, attachment_id: int, attachment: dict[str, Any]) -> dict[str, Any]:
        ...

    @abstractmethod
    @logger.catch()
    def delete_attachment(self, attachment_id: str) -> dict[str, Any]:
        ...

    @logger.catch()
    def download_attachment(self, filepath: str, attachment: dict[str, Any]):
        with open(filepath, 'wb') as file:
            file.write(eval(attachment['content']))
