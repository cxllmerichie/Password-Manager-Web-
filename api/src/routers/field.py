from fastapi import APIRouter, Depends, HTTPException

from .. import crud, schemas


router = APIRouter(tags=['Field'])


@router.post('/fields/', response_model=schemas.Field)
async def _(field: schemas.FieldCreate,
            user: schemas.User = Depends(crud.get_current_user)):
    db_field = await crud.create_field(user_id=user.id, field=field)
    return db_field


@router.get('/fields/{field_id}/', response_model=schemas.Field)
async def _(field_id: int,
            user: schemas.User = Depends(crud.get_current_user)):
    db_field = await crud.get_field(field_id=field_id)
    return db_field


@router.get('/fields/', response_model=schemas.Field)
async def _(user: schemas.User = Depends(crud.get_current_user)):
    db_fields = await crud.get_fields(user_id=user.id)
    return db_fields


@router.put('/fields/', response_model=schemas.Field)
async def _(field_id: int, field: schemas.FieldCreate,
            user: schemas.User = Depends(crud.get_current_user)):
    db_user = await crud.update_field(field_id=field_id, field=field)
    return db_user


@router.delete('/fields/', status_code=200)
async def _(field_id: int,
            user: schemas.User = Depends(crud.get_current_user)):
    await crud.delete_field(field_id=field_id)
    return dict(detail=f'Successfully deleted field <{field_id}>')
