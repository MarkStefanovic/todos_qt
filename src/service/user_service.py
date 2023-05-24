import datetime
import typing

import sqlalchemy as sa

from src import adapter, domain

__all__ = ("UserService",)


class UserService(domain.UserService):
    def __init__(
        self,
        *,
        engine: sa.engine.Engine,
        username: str,
        min_seconds_between_refreshes: int = 300,
    ):
        self._engine: typing.Final[sa.engine.Engine] = engine
        self._username: typing.Final[str] = username.lower().strip()
        self._min_seconds_between_refreshes: typing.Final[int] = min_seconds_between_refreshes

        self._users: dict[str, domain.User] = {}
        self._last_refresh: datetime.datetime | None = None
        self._current_user: domain.User | None = None
        self._last_current_user_scan: datetime.datetime | None = None

    def add(self, *, user: domain.User) -> None:
        self._refresh()

        repo = adapter.DbUserRepository(engine=self._engine)
        repo.add(user=user)

        self._users[user.user_id] = user

    def all(self) -> list[domain.User]:
        self._refresh()

        return list(self._users.values())

    def current_user(self) -> domain.User:
        if self._current_user:
            return self._current_user

        self._refresh()

        if self._last_current_user_scan is None:
            time_to_scan = True
        else:
            if (datetime.datetime.now() - self._last_current_user_scan).seconds > self._min_seconds_between_refreshes:
                time_to_scan = True
            else:
                time_to_scan = False

        if time_to_scan:
            for user in self._users.values():
                if user.username.lower().strip() == self._username:
                    self._current_user = user
                    break

            if self._current_user is None:
                repo = adapter.DbUserRepository(engine=self._engine)

                new_user = domain.User(
                    user_id=domain.create_uuid(),
                    username=self._username.lower().strip(),
                    display_name=self._username.lower().strip(),
                    is_admin=False,
                    date_added=datetime.datetime.now(),
                    date_updated=None,
                )

                repo.add(user=new_user)

                self._current_user = new_user

        assert self._current_user is not None

        return self._current_user

    def delete(self, *, user_id: str) -> None:
        self._refresh()

        repo = adapter.DbUserRepository(engine=self._engine)
        repo.delete(user_id=user_id)

        del self._users[user_id]

    def get(self, *, user_id: str) -> domain.User | None:
        self._refresh()

        return self._users.get(user_id)

    def get_user_by_username(self, *, username: str) -> domain.User | None:
        self._refresh()

        return next(
            (
                user for user in self._users.values()
                if user.username.lower() == username.lower()
            ),
            None
        )

    def refresh(self) -> None:
        repo = adapter.DbUserRepository(engine=self._engine)
        self._users = {
            user.user_id: user
            for user in repo.all()
        }
        self._last_refresh = datetime.datetime.now()

    def update(self, *, user: domain.User) -> None:
        self._refresh()

        repo = adapter.DbUserRepository(engine=self._engine)
        repo.update(user=user)

        self._users[user.user_id] = user

    def _refresh(self) -> None:
        if self._last_refresh is None:
            time_to_refresh = True
        else:
            seconds_since_last_refresh = (datetime.datetime.now() - self._last_refresh).total_seconds()
            if seconds_since_last_refresh >= self._min_seconds_between_refreshes:
                time_to_refresh = True
            else:
                time_to_refresh = False

        if time_to_refresh:
            self.refresh()


if __name__ == '__main__':
    eng = adapter.db.create_engine()
    svc = UserService(engine=eng, username="test")
    for r in svc.all():
        print(r)
