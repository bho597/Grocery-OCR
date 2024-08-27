from sqlalchemy.orm import Session

from api.postgres_models.users import Users

async def upload_user(db: Session, user_dict):
    new_user = Users(**user_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

async def get_user_by_id(db: Session, id: int):
    user = db.query(Users).filter_by(id=id).first()
    return user

async def update_user(db: Session, update_post, data) -> bool:
    for key, value in data.items():
        setattr(update_post, key, value)
    db.commit()
    return True


async def delete_user(db: Session, delete_post) -> bool:
    db.delete(delete_post)
    db.commit()
    return True