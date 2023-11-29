import pytest

from db.crud import UserCRUD


class TestUserCRUD:
    @pytest.mark.parametrize(
        "user_id",
        [
            1,
            2,
            3,
        ]
    )
    def test_user_crud(self, user_id: int):
        assert UserCRUD.read_user(user_id=user_id)