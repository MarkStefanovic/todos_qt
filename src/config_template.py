from src import domain

__all__ = ("config",)

config = domain.Config(
    sqlalchemy_url="postgresql+psycopg2://test:mypassword@localhost/testdb",
    schema_name="test",
    add_holidays=False,
    admin_usernames=["testuser1", "testuser2"],
)
