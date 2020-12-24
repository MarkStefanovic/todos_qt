import pathlib
import sqlite3

from src import domain, adapter


def test_execute_with_no_params(db_path: pathlib.Path) -> None:
    db = adapter.SqliteDb(db_path)
    with db:
        result = db.execute("SELECT 1 AS dummy")
    assert result.column_names == ["dummy"]
    assert result.first_value == 1


def test_execute_with_single_param(db_path: pathlib.Path) -> None:
    db = adapter.SqliteDb(db_path)
    with db:
        result = db.execute("SELECT :dummy AS col", dummy="test")
    assert result.column_names == ["col"]
    assert result.first_value == "test"


def test_executemany_with_multiple_params(db_path: pathlib.Path) -> None:
    db = adapter.SqliteDb(db_path)
    with db:
        assert db._con is not None
        db._con.execute("CREATE TABLE dummy (name TEXT);")
        db._con.execute(
            "INSERT INTO dummy (name) VALUES ('test1'), ('test2'), ('test3')"
        )
        db._con.commit()
        db.executemany(
            "DELETE FROM dummy WHERE name = :name",
            {"name": "test1"},
            {"name": "test2"},
        )

        result = db._con.execute("SELECT name FROM dummy ORDER BY name").fetchall()

    assert result == [("test3",)]
