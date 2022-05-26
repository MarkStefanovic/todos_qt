from __future__ import annotations

import datetime

import sqlalchemy as sa
import sqlmodel as sm

from src import adapter, domain
from src.domain import User

__all__ = ("DbUserService",)


class DbUserService(domain.UserService):
    def __init__(
        self,
        *,
        engine: sa.engine.Engine,
        username: str,
        min_seconds_between_refreshes: int = 300,
    ):
        self._engine = engine
        self._username = username.lower().strip()
        self._min_seconds_between_refreshes = min_seconds_between_refreshes

        self._users: dict[str, domain.User] = {}
        self._last_refresh: datetime.datetime | None = None
        self._current_user: domain.User | None = None
        self._last_current_user_scan: datetime.datetime | None = None

    def add(self, *, user: User) -> None:
        self._refresh()

        with sm.Session(self._engine) as session:
            repo = adapter.DbUserRepository(session=session)
            repo.add(user=user)
            session.commit()

            self._users[user.user_id] = user

    def all(self) -> list[User]:
        self._refresh()

        return list(self._users.values())

    def current_user(self) -> domain.User | None:
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

        return self._current_user

    def delete(self, *, user_id: str) -> None:
        self._refresh()

        with sm.Session(self._engine) as session:
            repo = adapter.DbUserRepository(session=session)
            repo.delete(user_id=user_id)
            session.commit()

            del self._users[user_id]

    def get(self, *, user_id: str) -> User | None:
        self._refresh()

        return self._users.get(user_id)

    def get_user_by_username(self, *, username: str) -> User | None:
        self._refresh()

        return next(
            (
                user for user in self._users.values()
                if user.username.lower() == username.lower()
            ),
            None
        )

    def refresh(self) -> None:
        with sm.Session(self._engine) as session:
            repo = adapter.DbUserRepository(session=session)
            self._users = {
                user.user_id: user
                for user in repo.all()
            }
            self._last_refresh = datetime.datetime.now()

    def update(self, *, user: User) -> None:
        self._refresh()

        with sm.Session(self._engine) as session:
            repo = adapter.DbUserRepository(session=session)
            repo.update(user=user)
            session.commit()

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
