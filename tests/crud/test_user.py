
from api.tests.utils import utils


def test_create_user(db: utils.db_session) -> None:
    user_name = 
    user = crud.create_user(session=db, user_create=user_in)
    assert user.email == email
    assert hasattr(user, "hashed_password")