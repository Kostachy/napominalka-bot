import pytest

from db.crud import UserCRUD


@pytest.mark.parametrize(
    "user_id",
    [
        1,
    ]
)
async def test_user_crud(user_id: int):
    user = await UserCRUD.read_user(user_id=user_id)
    assert user
