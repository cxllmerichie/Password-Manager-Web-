from fastapi import APIRouter, Depends, HTTPException
from apidevtools.utils import LIMIT

from .. import crud, schemas
from ..const import db


router = APIRouter(tags=['Category'])


@router.post('/category', name='create_category', response_model=schemas.Category, status_code=201)
async def _(category: schemas.CategoryCreate,
            user: schemas.User = Depends(crud.get_current_user)):
    db_category = await crud.get_category(title=category.title)
    if db_category:
        raise HTTPException(status_code=303, detail=f'Category <{category.title}> already exists')
    db_category = await crud.create_category(user_id=user.id, category=category)
    return db_category


@router.get('/category/{category_id}', name='get_category', response_model=schemas.Category)
async def _(category_id: int, depth: int = 0,
            user: schemas.User = Depends(crud.get_current_user)):
    db_category = await crud.get_category(category_id=category_id, depth=depth)
    if not db_category:
        raise HTTPException(status_code=404, detail=f'Category <{category_id}> does not exist')
    return db_category


@router.get('/categories', name='get_categories', response_model=list[schemas.Category])
async def _(limit: int = LIMIT, offset: int = 0,  depth: int = 0,
            user: schemas.User = Depends(crud.get_current_user)):
    db_categories = await crud.get_categories(user_id=user.id, limit=limit, offset=offset, depth=depth)
    return db_categories


@router.put('/category/{category_id}', name='update_category', response_model=schemas.Category)
async def _(category_id: int, category: schemas.CategoryCreate, depth: int = 0,
            user: schemas.User = Depends(crud.get_current_user)):
    db_category = await crud.update_category(category_id=category_id, category=category, depth=depth)
    if not db_category:
        raise HTTPException(status_code=404, detail=f'Category <{category_id}> does not exist')
    return db_category


@router.delete('/category/{category_id}', name='delete_category', response_model=schemas.Category)
async def _(category_id: int,
            user: schemas.User = Depends(crud.get_current_user)):
    db_category = await crud.delete_category(category_id=category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail=f'Category <{category_id}> does not exist')
    return db_category
