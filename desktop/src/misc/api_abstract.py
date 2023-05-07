from abc import abstractmethod
from typing import Any
from loguru import logger
from qcontextapi.misc import utils
from copy import copy
import ujson as json

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
    def export_item(self, filepath: str) -> None:
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

    @logger.catch()
    def import_item(self, filepath: str) -> dict[str, Any]:
        with open(filepath, 'r') as file:
            item = json.load(file)
        item_pop_keys = ['created_at', 'modified_at', 'fields']
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
