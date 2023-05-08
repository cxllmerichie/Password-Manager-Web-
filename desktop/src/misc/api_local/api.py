from typing import Any, Coroutine
import asyncio
from loguru import logger
from qcontextapi.misc import utils
from uuid import UUID

from ..api_abstract import CacheAPI
from . import crud


def prepare(coroutine: Coroutine) -> Any:
    return asyncio.get_event_loop().run_until_complete(coroutine)


class APILocal(CacheAPI):
    # CATEGORIES
    @logger.catch()
    def get_categories(self) -> list[dict[str, Any]]:
        response = prepare(crud.get_categories())
        return super().cache_get_categories(response)

    @logger.catch()
    def create_category(self, category: dict[str, Any]) -> dict[str, Any]:
        response = prepare(crud.create_category(utils.serializable(category)))
        return super().cache_create_category(response)

    @logger.catch()
    def get_category(self, category_id: int) -> dict[str, Any]:
        response = prepare(crud.get_category(int(category_id)))
        return super().cache_get_category(response)

    @logger.catch()
    def set_category_favourite(self, category_id: int, is_favourite: bool) -> dict[str, Any]:
        response = prepare(crud.set_category_favourite(int(category_id), is_favourite))
        return super().cache_update_category(response)

    @logger.catch()
    def update_category(self, category_id: int, category: dict[str, Any]) -> dict[str, Any]:
        response = prepare(crud.update_category(int(category_id), utils.serializable(category)))
        return super().cache_update_category(response)

    @logger.catch()
    def delete_category(self, category_id: int) -> dict[str, Any]:
        response = prepare(crud.delete_category(int(category_id)))
        return super().cache_delete_category(response)

    # ITEMS
    @logger.catch()
    def create_item(self, category_id: int, item: dict[str, Any]) -> dict[str, Any]:
        response = prepare(crud.create_item(int(category_id), utils.serializable(item)))
        return super().cache_create_item(response)

    @logger.catch()
    def delete_item(self, item_id: int) -> dict[str, Any]:
        response = prepare(crud.delete_item(int(item_id)))
        return super().cache_delete_item(response)

    @logger.catch()
    def update_item(self, item_id: int, item: dict[str, Any]) -> dict[str, Any]:
        response = prepare(crud.update_item(int(item_id), utils.serializable(item, ['expires_at'])))
        return super().cache_update_item(response)

    @logger.catch()
    def set_item_favourite(self, item_id: int, is_favourite: bool) -> dict[str, Any]:
        response = prepare(crud.set_item_favourite(int(item_id), is_favourite))
        return super().cache_update_item(response)

    # FIELDS
    @logger.catch()
    def add_field(self, item_id: int, field: dict[str, Any]) -> dict[str, Any]:
        response = prepare(crud.create_field(int(item_id), field))
        return super().cache_add_field(item_id, response)

    @logger.catch()
    def update_field(self, field_id: UUID, field: dict[str, Any]) -> dict[str, Any]:
        response = prepare(crud.update_field(field_id, field))
        return super().cache_update_field(response)

    @logger.catch()
    def delete_field(self, field_id: UUID) -> dict[str, Any]:
        response = prepare(crud.delete_field(field_id))
        return super().cache_delete_field(response)

    # ATTACHMENT
    @logger.catch()
    def add_attachment(self, item_id: int, attachment: dict[str, Any]) -> dict[str, Any]:
        response = prepare(crud.create_attachment(item_id, attachment))
        return super().cache_add_attachment(item_id, response)

    @logger.catch()
    def update_attachment(self, attachment_id: UUID, attachment: dict[str, Any]) -> dict[str, Any]:
        response = prepare(crud.update_attachment(attachment_id, attachment))
        return super().cache_update_attachment(response)

    @logger.catch()
    def delete_attachment(self, attachment_id: UUID) -> dict[str, Any]:
        response = prepare(crud.delete_attachment(attachment_id))
        return super().cache_delete_attachment(response)
