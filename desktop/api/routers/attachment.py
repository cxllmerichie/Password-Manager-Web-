from fastapi import APIRouter, HTTPException
from uuid import UUID

from .. import crud, schemas


router = APIRouter(tags=['Attachment'])


@router.post('/items/{item_id}/attachments/', name='Add new attachment to item by id', response_model=schemas.Attachment, status_code=201)
async def _(item_id: int, attachment: schemas.AttachmentCreate):
    db_item = await crud.get_item(item_id=item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail=f'Item <{item_id}> does not exist')
    db_attachment = await crud.create_attachment(item_id=item_id, attachment=attachment)
    return db_attachment


@router.get('/items/{item_id}/attachments/', name='Get attachment by id', response_model=list[schemas.Attachment])
async def _(item_id: int):
    db_item = await crud.get_item(item_id=item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail=f'Item <{item_id}> does not exist')
    db_attachments = await crud.get_attachments(item_id=item_id)
    return db_attachments


@router.get('/attachments/{attachment_id}/', name='Get attachment by id', response_model=schemas.Attachment)
async def _(attachment_id: UUID):
    db_attachment = await crud.get_attachment(attachment_id=attachment_id)
    return db_attachment


@router.put('/attachments/{attachment_id}/', name='Update attachment by id', response_model=schemas.Attachment)
async def _(attachment_id: UUID, attachment: schemas.AttachmentCreate):
    db_attachment = await crud.update_attachment(attachment_id=attachment_id, attachment=attachment)
    if not db_attachment:
        raise HTTPException(status_code=404, detail=f'Attachment <{db_attachment}> does not exist')
    return db_attachment


@router.delete('/attachments/{attachment_id}/', name='Delete attachment by id', response_model=schemas.Attachment)
async def _(attachment_id: UUID):
    db_attachment = await crud.delete_attachment(attachment_id=attachment_id)
    if not db_attachment:
        raise HTTPException(status_code=404, detail=f'Attachment <{db_attachment}> does not exist')
    return db_attachment
