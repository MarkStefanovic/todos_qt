import datetime
import typing

import sqlalchemy as sa
from loguru import logger

from src import adapter, domain

__all__ = ("UserService",)


class UserService(domain.UserService):
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
            logger.error(f"{self.__class__.__name__}.add({user=!r}): {e!s}")

            return domain.Error.new(str(e), user=user)

    def get_current_user(self) -> domain.User | domain.Error:
        try:
            def get_user_by_username(*, cn: sa.Connection) -> domain.User | None | domain.Error:
                users = adapter.user_repo.where(con=cn, active=True)
                if isinstance(users, domain.Error):
                    return users

                return next(
                    (user for user in users if user.username.lower().strip() == self._username),
                    None,
                )

            with self._engine.begin() as con:
                initial_current_user = get_user_by_username(cn=con)
                if isinstance(initial_current_user, domain.Error):
                    return initial_current_user

                if initial_current_user:
                    return initial_current_user
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
            return domain.Error.new(str(e))

    def delete(self, *, user_id: str) -> None | domain.Error:
        with self._engine.begin() as con:
            delete_result = adapter.user_repo.delete_user(con=con, user_id=user_id)
            if isinstance(delete_result, domain.Error):
                return delete_result

            return None

    def get(self, *, user_id: str) -> domain.User | None | domain.Error:
        return self._users.get(user_id)

    def get_user_by_username(self, *, username: str) -> domain.User | None:
        return next((user for user in self._users.values() if user.username.lower() == username.lower()), None)

    def update(self, *, user: domain.User) -> None | domain.Error:
        self._refresh()

        repo = adapter.DbUserRepository(engine=self._engine)
        repo.update(user=user)

        self._users[user.user_id] = user

    def where(self, *, active_only: bool) -> list[domain.User]:
        return list(self._users.values())


if __name__ == "__main__":
    eng = adapter.db.create_engine()
    svc = UserService(engine=eng, username="test")
    for r in svc.where():
        print(r)
