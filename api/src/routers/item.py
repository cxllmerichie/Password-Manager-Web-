from fastapi import APIRouter, Depends, HTTPException

from .. import crud, schemas


router = APIRouter(tags=['Item'])


@router.post('/items/', response_model=schemas.Item)
async def _(item: schemas.ItemCreate,
            user: schemas.User = Depends(crud.get_current_user)):
    db_item = await crud.create_item(user_id=user.id, item=item)
    return db_item


@router.get('/items/{item_id}/', response_model=schemas.Item)
async def _(item_id: int,
            user: schemas.User = Depends(crud.get_current_user)):
    db_item = await crud.get_item(item_id=item_id)
    return db_item


@router.get('/items/', response_model=schemas.Item)
async def _(user: schemas.User = Depends(crud.get_current_user)):
    db_items = await crud.get_items(user_id=user.id)
    return db_items


@router.put('/items/', response_model=schemas.Item)
async def _(item_id: int, item: schemas.ItemCreate,
            user: schemas.User = Depends(crud.get_current_user)):
    db_user = await crud.update_item(item_id=item_id, item=item)
    return db_user


@router.delete('/items/', status_code=200)
async def _(item_id: int,
            user: schemas.User = Depends(crud.get_current_user)):
    await crud.delete_item(item_id=item_id)
    return dict(detail=f'Successfully deleted item <{item_id}>')
