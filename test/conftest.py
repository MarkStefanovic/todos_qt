import logging
import typing

import pytest
import sqlalchemy as sa
from PyQt5 import QtWidgets as qtw  # noqa
from sqlalchemy.orm import Session

from src import adapter, domain

logger = logging.getLogger("test")

QT_APP = qtw.QApplication([])


@pytest.fixture(scope="function")
def engine() -> sa.engine.Engine:
    eng = sa.create_engine("sqlite://", echo=True)
    create_tables_result = adapter.db.create_tables(schema=None, engine=eng)
    if isinstance(create_tables_result, domain.Error):
        raise Exception(f"Error creating tables: {create_tables_result!s}")

    return eng


@pytest.fixture(scope="function")
def session(engine: sa.engine.Engine) -> typing.Generator[Session, None, None]:
    session = Session(engine)
    yield session
    session.close()
    #
    # sm.SQLModel.metadata.create_all
    # fp = pathlib.Path("testdb.sqlite")
    # fp.unlink(missing_ok=True)
    # yield fp
    # fp.unlink(missing_ok=True)
