from fastapi import APIRouter
from fastapi import status, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from api.config.postgresql import get_db
from api.schemas.users import User
from api.services import users as users_service

usersRoute = APIRouter()
base = '/users'



@usersRoute.post(base)
async def create_user(user: User, db: Session = Depends(get_db)):
    return await users_service.upload_user(db=db, user_dict=user.model_dump())


@usersRoute.get(base+'/{user_id}')
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = await users_service.get_user_by_id(db=db, id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"Could not find user with the given Id: {user_id}.")
    return user


@usersRoute.put(base+'/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_user(user_id, data: User, db: Session = Depends(get_db)):
    result = await users_service.get_user_by_id(db=db, id=user_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Could not find user with the given Id: {user_id}.")
    await users_service.update_user(db=db, update_post=result, data=data.model_dump())
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@usersRoute.delete(base+'/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    result = await users_service.get_user_by_id(db=db, id=user_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Could not find user with the given Id: {user_id}.")
    await users_service.delete_user(db=db, delete_post=result)
    return Response(status_code=status.HTTP_204_NO_CONTENT)