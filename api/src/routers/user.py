from fastapi import APIRouter, Depends, HTTPException

from .. import crud, schemas


router = APIRouter(tags=['User'])


@router.post('/user', name='create_user', response_model=schemas.UserToken, status_code=201)
async def _(user: schemas.UserCreate):
    db_user = await crud.get_user(email=user.email, schema=schemas.UserCreate)
    if db_user:
        raise HTTPException(status_code=303, detail=f'Email <{user.email}> already registered')
    db_user = await crud.create_user(user=user)
    return schemas.UserToken(**dict(await crud.create_token(user=db_user)), **dict(db_user))


@router.put('/user', name='update_user', response_model=schemas.User)
async def _(user: schemas.UserUpdate, depth: int = 0,
            _user: schemas.User = Depends(crud.get_current_user)):
    db_user = await crud.update_user(user_id=_user.id, user=user, depth=depth)
    return db_user


@router.delete('/user', name='delete_user', response_model=schemas.User)
async def _(user: schemas.User = Depends(crud.get_current_user)):
    db_user = await crud.delete_user(user_id=user.id)
    return db_user
