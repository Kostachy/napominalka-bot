import pytest

from db.crud import UserCRUD


class TestUserCrud:
    @pytest.mark.parametrize(
        "user_id",
        [
            1,
            2,
            3,
        ]
    )
    async def test_usercrud_read_user(self, user_id: int):
        user = await UserCRUD.read_user(user_id=user_id)

        assert user
        assert user[0] == user_id
