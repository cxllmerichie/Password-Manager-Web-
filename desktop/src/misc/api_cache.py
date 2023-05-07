from abc import ABC
from typing import Any
from loguru import logger
from qcontextapi.misc import utils
from uuid import UUID


class Cache(ABC):
    __categories: list[dict[str, Any]] = None
    __category: dict[str, Any] = None
    __item: dict[str, Any] = None
    field_identifiers: list[UUID] = []
    attachment_identifiers: list[UUID] = []

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

    # CATEGORIES
    @logger.catch()
    def cache_get_categories(self, response: list[dict[str, Any]]) -> list[dict[str, Any]]:
        self.__categories = response
        return response

    @logger.catch()
    def cache_create_category(self, response: dict[str, Any]) -> dict[str, Any]:
        if category_id := response.get('id'):
            self.__categories.append(response)
            self.category = response
        return response

    @logger.catch()
    def cache_get_category(self, response: dict[str, Any]) -> dict[str, Any]:
        if category_id := response.get('id'):
            c_idx, _ = utils.find(self.categories, 'id', category_id)
            self.category = self.categories[c_idx] = response
        return response

    @logger.catch()
    def cache_update_category(self, response: dict[str, Any]) -> dict[str, Any]:
        if category_id := response.get('id'):
            c_idx, _ = utils.find(self.categories, 'id', category_id)
            self.category = self.categories[c_idx] = response
        return response

    @logger.catch()
    def cache_delete_category(self, response: dict[str, Any]) -> dict[str, Any]:
        if category_id := response.get('id'):
            c_idx, _ = utils.find(self.categories, 'id', category_id)
            self.categories.pop(c_idx)
            self.category = self.item = None
        return response

    # ITEMS
    @logger.catch()
    def cache_create_item(self, response: dict[str, Any]) -> dict[str, Any]:
        if item_id := response.get('id'):
            c_idx, _ = utils.find(self.categories, 'id', self.category['id'])
            self.categories[c_idx]['items'].append(response)
            self.item = response
        return response

    @logger.catch()
    def cache_delete_item(self, response: dict[str, Any]) -> dict[str, Any]:
        if item_id := response.get('id'):
            c_idx, _ = utils.find(self.categories, 'id', self.item['category_id'])
            i_idx, _ = utils.find(self.categories[c_idx]['items'], 'id', item_id)
            self.categories[c_idx]['items'].pop(i_idx)
            self.item = None
        return response

    @logger.catch()
    def cache_update_item(self, response: dict[str, Any]) -> dict[str, Any]:
        if item_id := response.get('id'):
            c_idx, _ = utils.find(self.categories, 'id', self.item['category_id'])
            i_idx, _ = utils.find(self.categories[c_idx]['items'], 'id', item_id)
            self.item = self.categories[c_idx]['items'][i_idx] = response
        return response

    # FIELDS
    @logger.catch()
    def cache_add_field(self, item_id: int, response: dict[str, Any]) -> dict[str, Any]:
        if field_id := response.get('id'):
            c_idx, _ = utils.find(self.categories, 'id', self.item['category_id'])
            i_idx, _ = utils.find(self.items, 'id', item_id)
            self.categories[c_idx]['items'][i_idx]['fields'].append(response)
            self.item = self.categories[c_idx]['items'][i_idx]
        return response

    @logger.catch()
    def cache_update_field(self, response: dict[str, Any]) -> dict[str, Any]:
        if field_id := response.get('id'):
            c_idx, _ = utils.find(self.categories, 'id', self.item['category_id'])
            i_idx, _ = utils.find(self.items, 'id', response['item_id'])
            f_idx, _ = utils.find(self.items[i_idx]['fields'], 'id', field_id)
            self.categories[c_idx]['items'][i_idx]['fields'][f_idx] = response
            self.item = self.categories[c_idx]['items'][i_idx]
        return response

    @logger.catch()
    def cache_delete_field(self, response: dict[str, Any]) -> dict[str, Any]:
        if field_id := response.get('id'):
            c_idx, _ = utils.find(self.categories, 'id', self.item['category_id'])
            i_idx, _ = utils.find(self.items, 'id', response['item_id'])
            self.categories[c_idx]['items'][i_idx]['fields'].remove(response)
            self.item = self.categories[c_idx]['items'][i_idx]
        return response

    # ATTACHMENT
    @logger.catch()
    def cache_add_attachment(self, item_id: int, response: dict[str, Any]) -> dict[str, Any]:
        if attachment_id := response.get('id'):
            c_idx, _ = utils.find(self.categories, 'id', self.item['category_id'])
            i_idx, _ = utils.find(self.categories[c_idx]['items'], 'id', item_id)
            self.categories[c_idx]['items'][i_idx]['attachments'].append(response)
            self.item = self.categories[c_idx]['items'][i_idx]
        return response

    @logger.catch()
    def cache_update_attachment(self, response: dict[str, Any]) -> dict[str, Any]:
        if attachment_id := response.get('id'):
            i_idx, _ = utils.find(self.items, 'id', response['item_id'])
            c_idx, _ = utils.find(self.categories, 'id', self.items[i_idx]['category_id'])
            a_idx, _ = utils.find(self.items[i_idx]['attachments'], 'id', attachment_id)
            self.categories[c_idx]['items'][i_idx]['attachments'][a_idx] = response
            self.item = self.categories[c_idx]['items'][i_idx]
        return response

    @logger.catch()
    def cache_delete_attachment(self, response: dict[str, Any]) -> dict[str, Any]:
        if attachment_id := response.get('id'):
            i_idx, _ = utils.find(self.items, 'id', response['item_id'])
            c_idx, _ = utils.find(self.categories, 'id', self.items[i_idx]['category_id'])
            self.categories[c_idx]['items'][i_idx]['attachments'].remove(response)
            self.item = self.categories[c_idx]['items'][i_idx]
        return response
