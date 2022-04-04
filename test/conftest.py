import logging
import typing

import pytest
import sqlalchemy as sa
import sqlmodel as sm
from PyQt5 import QtWidgets as qtw

logger = logging.getLogger("test")

QT_APP = qtw.QApplication([])


@pytest.fixture(scope="function")
def engine() -> sa.engine.Engine:
    eng = sm.create_engine("sqlite://", echo=True)
    sm.SQLModel.metadata.create_all(eng)
    return eng


@pytest.fixture(scope="function")
def session(engine: sa.engine.Engine) -> typing.Generator[sm.Session, None, None]:
    session = sm.Session(engine)
    yield session
    session.close()
    #
    # sm.SQLModel.metadata.create_all
    # fp = pathlib.Path("testdb.sqlite")
    # fp.unlink(missing_ok=True)
    # yield fp
    # fp.unlink(missing_ok=True)
