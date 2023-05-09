from uuid import UUID
from typing import Any

from .. import schemas
from ..utils import db


async def create_attachment(item_id: int, attachment: dict[str, Any]) -> dict[str, Any]:
    attachment = schemas.AttachmentCreateCrud(**attachment, item_id=item_id)
    db_attachment = await db.insert(attachment, schemas.Attachment)
    return db_attachment.dict()


async def get_attachments(item_id: int) -> list[dict[str, Any]]:
    query, args = f'SELECT * FROM "attachment" WHERE "item_id" = $1;', (item_id, )
    db_attachments = await (await db.select(query, args, schemas.Attachment)).all()
    return [db_attachment.dict() for db_attachment in db_attachments]


async def get_attachment(attachment_id: UUID) -> dict[str, Any] | None:
    query, args = f'SELECT * FROM "attachment" WHERE "id" = $1;', (attachment_id, )
    db_attachment = await (await db.select(query, args, schemas.Attachment)).first()
    return db_attachment.dict()


async def update_attachment(attachment_id: UUID, attachment: dict[str, Any]) -> dict[str, Any]:
    attachment = schemas.AttachmentCreate(**attachment)
    attachment.id = str(attachment_id)
    db_attachment = await (await db.update(attachment, dict(id=attachment_id), schemas.Attachment)).first()
    return db_attachment.dict()


async def delete_attachment(attachment_id: UUID) -> dict[str, Any]:
    db_attachment = await (await db.delete(dict(id=attachment_id), schemas.Attachment, 'attachment')).first()
    await db.remove(db_attachment.id)
    return db_attachment.dict()
