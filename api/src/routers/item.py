from fastapi import APIRouter, Depends, HTTPException
from apidevtools.utils import LIMIT

from .. import crud, schemas
from ..const import db


router = APIRouter(tags=['Item'])


@router.post('/category/{category_id}/item', name='create_item', response_model=schemas.Item, status_code=201)
async def _(category_id: int, item: schemas.ItemCreate,
            user: schemas.User = Depends(crud.get_current_user)):
    db_category = await crud.get_category(category_id=category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail=f'Category <{category_id}> does not exist')
    db_item = await crud.create_item(category_id=category_id, item=item)
    return db_item


@router.get('/item/{item_id}', name='get_item', response_model=schemas.Item)
async def _(item_id: int, depth: int = 0,
            user: schemas.User = Depends(crud.get_current_user)):
    db_item = await crud.get_item(item_id=item_id, depth=depth)
    if not db_item:
        raise HTTPException(status_code=404, detail=f'Item <{item_id}> does not exist')
    return db_item


@router.get('/category/{category_id}/items', name='get_items', response_model=list[schemas.Item])
async def _(category_id: int, limit: int = LIMIT, offset: int = 0, depth: int = 0,
            user: schemas.User = Depends(crud.get_current_user)):
    db_category = await crud.get_category(category_id=category_id, depth=depth)
    if not db_category:
        raise HTTPException(status_code=404, detail=f'Category <{category_id}> does not exist')
    db_items = await crud.get_items(category_id=category_id, limit=limit, offset=offset)
    return db_items


@router.put('/item/{item_id}', name='update_item', response_model=schemas.Item)
async def _(item_id: int, item: schemas.ItemCreate, depth: int = 0,
            user: schemas.User = Depends(crud.get_current_user)):
    db_item = await crud.update_item(item_id=item_id, item=item, depth=depth)
    if not db_item:
        raise HTTPException(status_code=404, detail=f'Item <{item_id}> does not exist')
    return db_item


@router.delete('/item/{item_id}', name='delete_item', response_model=schemas.Item)
async def _(item_id: int,
            user: schemas.User = Depends(crud.get_current_user)):
    db_item = await crud.delete_item(item_id=item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail=f'Item <{item_id}> does not exist')
    return db_item
