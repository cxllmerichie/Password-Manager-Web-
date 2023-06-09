from uuid import UUID

from .. import schemas
from ..const import db


async def create_attachment(item_id: int, attachment: dict) -> schemas.Attachment:
    attachment = schemas.AttachmentCreateCrud(**attachment, item_id=item_id)
    db_attachment = await db.insert(attachment, schemas.Attachment)
    return db_attachment.dict()


async def get_attachments(item_id: int, schema: type = schemas.Attachment) -> list[schemas.Attachment]:
    query, args = f'SELECT * FROM "attachment" WHERE "item_id" = $1;', (item_id, )
    db_attachments = await (await db.select(query, args, schema)).all()
    return [a.dict() for a in db_attachments]


async def get_attachment(attachment_id: UUID, schema: type = schemas.Attachment) -> schemas.Attachment | None:
    query, args = f'SELECT * FROM "attachment" WHERE "id" = $1;', (str(attachment_id), )
    db_attachment = await (await db.select(query, args, schema)).first()
    return db_attachment.dict()


async def update_attachment(attachment_id: UUID, attachment: dict) -> schemas.Attachment:
    attachment['id'] = attachment_id
    db_attachment = await (await db.update(schemas.AttachmentCreate(**attachment), dict(id=str(attachment_id)), schemas.Attachment)).first()
    return db_attachment.dict()


async def delete_attachment(attachment_id: UUID) -> schemas.Attachment:
    db_attachment = await (await db.delete(dict(id=str(attachment_id)), schemas.Attachment, 'attachment')).first()
    await db.remove(db_attachment.id)
    return db_attachment.dict()
