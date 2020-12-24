import logging
import pathlib
import typing

import pytest

logger = logging.getLogger("test")


@pytest.fixture(scope="function")
def db_path() -> typing.Generator[pathlib.Path, None, None]:
    fp = pathlib.Path("testdb.sqlite")
    fp.unlink(missing_ok=True)
    yield fp
    fp.unlink(missing_ok=True)
