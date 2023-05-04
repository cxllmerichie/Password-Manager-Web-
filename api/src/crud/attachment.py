from .. import schemas
from ..const import db, keys


async def create_attachment(item_id: int, attachment: schemas.AttachmentCreate) -> schemas.Attachment:
    attachment = schemas.AttachmentCreateCrud(**dict(attachment), item_id=item_id)
    db_attachment = await db.insert(attachment, schemas.Attachment)
    return db_attachment


async def get_attachments(item_id: int, schema: type = schemas.Attachment) -> list[schemas.Attachment]:
    query, args = f'SELECT * FROM "attachment" WHERE "item_id" = $1;', (item_id, )
    db_attachments = await (await db.select(query, args, schema)).all()
    return db_attachments


async def get_attachment(attachment_id: int, schema: type = schemas.Attachment) -> schemas.Attachment | None:
    query, args = f'SELECT * FROM "attachment" WHERE "id" = $1;', (attachment_id, )
    db_attachment = await (await db.select(query, args, schema)).first()
    return db_attachment


async def update_attachment(attachment_id: int, attachment: schemas.AttachmentCreate) -> schemas.Attachment:
    db_attachment = await (await db.update(attachment, dict(id=attachment_id), schemas.Attachment)).first()
    return db_attachment


async def delete_attachment(attachment_id: int) -> schemas.Attachment:
    db_attachment = await (await db.delete(dict(id=attachment_id), schemas.Attachment, 'attachment')).first()
    await keys.delete(db_attachment.id)
    return db_attachment
