from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from .. import crud, schemas


router = APIRouter(tags=['Field'])


@router.post('/items/{item_id}/fields/', name='Add new field to item by id', response_model=schemas.Field, status_code=201)
async def _(item_id: int, field: schemas.FieldCreate,
            user: schemas.User = Depends(crud.get_current_user)):
    db_item = await crud.get_item(item_id=item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail=f'Item <{item_id}> does not exist')
    db_field = await crud.create_field(item_id=item_id, field=field)
    return db_field


@router.get('/items/{item_id}/fields/', name='Get field by id', response_model=list[schemas.Field])
async def _(item_id: int,
            user: schemas.User = Depends(crud.get_current_user)):
    db_item = await crud.get_item(item_id=item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail=f'Item <{item_id}> does not exist')
    db_fields = await crud.get_fields(item_id=item_id)
    return db_fields


@router.get('/fields/{field_id}/', name='Get field by id', response_model=schemas.Field)
async def _(field_id: UUID,
            user: schemas.User = Depends(crud.get_current_user)):
    db_field = await crud.get_field(field_id=field_id)
    return db_field


@router.put('/fields/{field_id}/', name='Update field by id', response_model=schemas.Field)
async def _(field_id: UUID, field: schemas.FieldCreate,
            user: schemas.User = Depends(crud.get_current_user)):
    db_field = await crud.update_field(field_id=field_id, field=field)
    if not db_field:
        raise HTTPException(status_code=404, detail=f'Field <{db_field}> does not exist')
    return db_field


@router.delete('/fields/{field_id}/', name='Delete field by id', response_model=schemas.Field)
async def _(field_id: UUID,
            user: schemas.User = Depends(crud.get_current_user)):
    db_field = await crud.delete_field(field_id=field_id)
    if not db_field:
        raise HTTPException(status_code=404, detail=f'Field <{db_field}> does not exist')
    return db_field
