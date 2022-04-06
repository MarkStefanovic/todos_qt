import datetime

import sqlmodel as sm

from src import domain
from src.adapter import db
from src.domain import User

__all__ = ("DbUserRepository",)


# noinspection DuplicatedCode
class DbUserRepository(domain.UserRepository):
    def __init__(self, session: sm.Session):
        self._session = session

    def add(self, *, user: User) -> None:
        user_orm = db.User(
            user_id=user.user_id,
            display_name=user.display_name,
            username=user.username,
            is_admin=user.is_admin,
            date_added=datetime.datetime.now(),
            date_updated=None,
            date_deleted=None,
        )
        self._session.add(user_orm)

    def all(self) -> list[User]:
        result = self._session.exec(
            sm.select(db.User)
            .where(db.User.date_deleted == None)  # noqa
        ).all()
        return [
            domain.User(
                user_id=row.user_id,
                username=row.username,
                display_name=row.display_name,
                is_admin=row.is_admin,
                date_added=row.date_added,
                date_updated=row.date_updated,
            )
            for row in result
        ]

    def delete(self, *, user_id: str) -> None:
        if todo_orm := self._session.exec(
            sm.select(db.Todo)
            .where(db.Todo.date_deleted == None)  # noqa
            .where(db.Todo.user_id == user_id)
            .limit(1)
        ).one_or_none():
            raise Exception(
                f"Cannot delete user, as the todo, {todo_orm.description!r}, uses it."
            )

        if orm := self._session.exec(
            sm.select(db.User)
            .where(db.User.user_id == user_id)
        ).one_or_none():
            orm.date_deleted = datetime.datetime.now()
            self._session.add(orm)

    def get(self, *, user_id: str) -> domain.User | None:
        if orm := self._session.exec(
            sm.select(db.User)
            .where(db.User.user_id == user_id)
        ).one_or_none():
            return domain.User(
                user_id=orm.user_id,
                username=orm.username,
                display_name=orm.display_name,
                is_admin=orm.is_admin,
                date_added=orm.date_added,
                date_updated=orm.date_updated,
            )

        return None

    def update(self, *, user: User) -> None:
        if orm := self._session.exec(
            sm.select(db.User)
            .where(db.User.user_id == user.user_id)
        ).one_or_none():
            orm.username = user.username
            orm.display_name = user.display_name
            orm.date_updated = datetime.datetime.now()
            orm.is_admin = user.is_admin
            self._session.add(orm)
