import logging
import typing

import pytest
import sqlalchemy as sa
from PyQt5 import QtWidgets as qtw  # noqa
from sqlalchemy.orm import Session

logger = logging.getLogger("test")

QT_APP = qtw.QApplication([])


@pytest.fixture(scope="function")
def engine() -> sa.engine.Engine:
    eng = sa.create_engine("sqlite://", echo=True)
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
