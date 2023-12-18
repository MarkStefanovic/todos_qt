import datetime
import typing

import sqlalchemy as sa
from loguru import logger

from src import adapter, domain

__all__ = ("UserService",)


class UserService:
    def __init__(
        self,
        *,
        engine: sa.engine.Engine,
        username: str,
    ):
        self._engine: typing.Final[sa.engine.Engine] = engine
        self._username: typing.Final[str] = username.lower().strip()

    def add(self, *, user: domain.User) -> None | domain.Error:
        try:
            with self._engine.begin() as con:
                adapter.user_repo.add(con=con, user=user)

            return None
        except Exception as e:
            logger.error(f"{self.__class__.__name__}.add({user=!r}) failed: {e!s}")

            return domain.Error.new(str(e), user=user)

    def get_current_user(self) -> domain.User | domain.Error:
        try:
            with self._engine.begin() as con:
                users = adapter.user_repo.where(con=con, active=True)
                if isinstance(users, domain.Error):
                    return users

                if user := next(
                    (user for user in users if user.username.lower().strip() == self._username),
                    None,
                ):
                    return user
                else:
                    new_user = domain.User(
                        user_id=domain.create_uuid(),
                        username=self._username,
                        display_name=self._username,
                        is_admin=False,
                        date_added=datetime.datetime.now(),
                        date_updated=None,
                    )

                    add_result = adapter.user_repo.add(con=con, user=new_user)
                    if isinstance(add_result, domain.Error):
                        return add_result

                    return new_user
        except Exception as e:
            logger.error(f"{self.__class__.__name__}.get_current_user() failed: {e!s}")

            return domain.Error.new(str(e))

    def delete(self, *, user_id: str) -> None | domain.Error:
        try:
            with self._engine.begin() as con:
                delete_result = adapter.user_repo.delete_user(con=con, user_id=user_id)
                if isinstance(delete_result, domain.Error):
                    return delete_result

                return None
        except Exception as e:
            logger.error(f"{self.__class__.__name__}.delete({user_id=!r}) failed: {e!s}")

            return domain.Error.new(str(e), user_id=user_id)

    def get(self, *, user_id: str) -> domain.User | None | domain.Error:
        try:
            with self._engine.begin() as con:
                user = adapter.user_repo.get(con=con, user_id=user_id)
                return user
        except Exception as e:
            logger.error(f"{self.__class__.__name__}.get({user_id=!r}) failed: {e!s}")

            return domain.Error.new(str(e), user_id=user_id)

    def update(self, *, user: domain.User) -> None | domain.Error:
        try:
            with self._engine.begin() as con:
                return adapter.user_repo.update(con=con, user=user)
        except Exception as e:
            logger.error(f"{self.__class__.__name__}.update({user=!r}) failed: {e!s}")

            return domain.Error.new(str(e), user=user)

    def where(self, *, active: bool) -> list[domain.User] | domain.Error:
        try:
            with self._engine.begin() as con:
                return adapter.user_repo.where(con=con, active=active)
        except Exception as e:
            logger.error(f"{self.__class__}.where({active=!r}) failed: {e!s}")

            return domain.Error.new(str(e), active=active)


if __name__ == "__main__":
    eng = adapter.db.create_engine()
    svc = UserService(engine=eng, username="test")
    for r in svc.where():
        print(r)
