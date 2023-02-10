from fastapi import APIRouter, Depends, HTTPException

from .. import crud, schemas


router = APIRouter(tags=['Category'])


@router.post('/categories/', response_model=schemas.Category)
async def _(category: schemas.CategoryCreate,
            user: schemas.User = Depends(crud.get_current_user)):
    db_category = await crud.create_category(user_id=user.id, category=category)
    return db_category


@router.get('/categories/{category_id}/', response_model=schemas.Category)
async def _(category_id: int,
            user: schemas.User = Depends(crud.get_current_user)):
    db_category = await crud.get_category(category_id=category_id)
    return db_category


@router.get('/categories/', response_model=schemas.Category)
async def _(user: schemas.User = Depends(crud.get_current_user)):
    db_categories = await crud.get_categories(user_id=user.id)
    return db_categories


@router.put('/categories/', response_model=schemas.Category)
async def _(category_id: int, category: schemas.CategoryCreate,
            user: schemas.User = Depends(crud.get_current_user)):
    db_user = await crud.update_category(category_id=category_id, category=category)
    return db_user


@router.delete('/categories/', status_code=200)
async def _(category_id: int,
            user: schemas.User = Depends(crud.get_current_user)):
    await crud.delete_category(category_id=category_id)
    return dict(detail=f'Successfully deleted category <{category_id}>')
