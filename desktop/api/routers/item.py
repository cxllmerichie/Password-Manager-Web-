from fastapi import APIRouter, Depends, HTTPException
from apidevtools.utils import LIMIT

from .. import crud, schemas
from ..const import db


router = APIRouter(tags=['Item'])


@router.post('/categories/{category_id}/items/', name='Create item by category id', response_model=schemas.Item, status_code=201)
async def _(category_id: int, item: schemas.ItemCreate,
            user: schemas.User = Depends(crud.get_current_user)):
    db_category = await crud.get_category(category_id=category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail=f'Category <{category_id}> does not exist')
    db_item = await crud.create_item(category_id=category_id, item=item)
    return db_item


@router.get('/items/{item_id}/', name='Get item by id', response_model=schemas.Item)
async def _(item_id: int,
            user: schemas.User = Depends(crud.get_current_user)):
    db_item = await crud.get_item(item_id=item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail=f'Item <{item_id}> does not exist')
    return db_item


@router.get('/categories/{category_id}/items/', name='Get items by category id', response_model=list[schemas.Item])
async def _(category_id: int, limit: int = LIMIT, offset: int = 0,
            user: schemas.User = Depends(crud.get_current_user)):
    db_items = await crud.get_items(category_id=category_id, limit=limit, offset=offset)
    return db_items


@router.put('/items/{item_id}/', name='Update item by id', response_model=schemas.Item)
async def _(item_id: int, item: schemas.ItemCreate,
            user: schemas.User = Depends(crud.get_current_user)):
    db_item = await crud.update_item(item_id=item_id, item=item)
    if not db_item:
        raise HTTPException(status_code=404, detail=f'Item <{item_id}> does not exist')
    return db_item


@router.put('/items/{item_id}/favourite/', name='Set item favourite by id', response_model=schemas.Item)
async def _(item_id: int, is_favourite: bool,
            user: schemas.User = Depends(crud.get_current_user)):
    db_item = await (await db.update(dict(is_favourite=is_favourite), dict(id=item_id), schemas.Item, 'item', rel_depth=1)).first()
    if not db_item:
        raise HTTPException(status_code=404, detail=f'Item <{item_id}> does not exist')
    return db_item


@router.delete('/items/{item_id}/', name='Delete item by id', response_model=schemas.Item)
async def _(item_id: int,
            user: schemas.User = Depends(crud.get_current_user)):
    db_item = await crud.delete_item(item_id=item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail=f'Item <{item_id}> does not exist')
    return db_item
