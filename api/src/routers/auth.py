from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm as OAuth2Form

from .. import crud, schemas


router = APIRouter(tags=['AUTH'])


@router.post('/auth/token', name='create_token', response_model=schemas.Token)
async def _(form: OAuth2Form = Depends(OAuth2Form)):
    db_user = await crud.authenticate_user(email=form.username, password=form.password)
    if not db_user:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    return await crud.create_token(user=db_user)


@router.get('/auth/user', name='get_current_user', response_model=schemas.User)
async def _(user: schemas.User = Depends(crud.get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail='Unauthorized')
    return user


@router.get('/auth/{email}', name='verify_email', response_model=bool)
async def _(email: str):
    db_user = await crud.get_user(email=email)
    return db_user is not None
