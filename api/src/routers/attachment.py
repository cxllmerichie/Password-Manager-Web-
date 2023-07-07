from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from .. import crud, schemas


router = APIRouter(tags=['Attachment'])


@router.post('/item/{item_id}/attachment', name='create_attachment', response_model=schemas.Attachment, status_code=201)
async def _(item_id: int, attachment: schemas.AttachmentCreate,
            user: schemas.User = Depends(crud.get_current_user)):
    db_item = await crud.get_item(item_id=item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail=f'Item <{item_id}> does not exist')
    db_attachment = await crud.create_attachment(item_id=item_id, attachment=attachment)
    return db_attachment


@router.get('/item/{item_id}/attachments', name='get_attachments', response_model=list[schemas.Attachment])
async def _(item_id: int,
            user: schemas.User = Depends(crud.get_current_user)):
    db_item = await crud.get_item(item_id=item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail=f'Item <{item_id}> does not exist')
    db_attachments = await crud.get_attachments(item_id=item_id)
    return db_attachments


@router.get('/attachment/{attachment_id}', name='get_attachment', response_model=schemas.Attachment)
async def _(attachment_id: UUID,
            user: schemas.User = Depends(crud.get_current_user)):
    db_attachment = await crud.get_attachment(attachment_id=attachment_id)
    if not db_attachment:
        raise HTTPException(status_code=404, detail=f'Attachment <{db_attachment}> does not exist')
    return db_attachment


@router.put('/attachment/{attachment_id}', name='update_attachment', response_model=schemas.Attachment)
async def _(attachment_id: UUID, attachment: schemas.AttachmentCreate,
            user: schemas.User = Depends(crud.get_current_user)):
    db_attachment = await crud.update_attachment(attachment_id=attachment_id, attachment=attachment)
    if not db_attachment:
        raise HTTPException(status_code=404, detail=f'Attachment <{db_attachment}> does not exist')
    return db_attachment


@router.delete('/attachment/{attachment_id}', name='delete_attachment', response_model=schemas.Attachment)
async def _(attachment_id: UUID,
            user: schemas.User = Depends(crud.get_current_user)):
    db_attachment = await crud.delete_attachment(attachment_id=attachment_id)
    if not db_attachment:
        raise HTTPException(status_code=404, detail=f'Attachment <{db_attachment}> does not exist')
    return db_attachment
