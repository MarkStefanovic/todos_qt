from src import domain

__all__ = ("UserService",)


class UserService(domain.UserService):
    def __init__(self):  # type: ignore
        self.add_result: None | domain.Error = None
        self.get_current_user_result: domain.User | domain.Error = domain.DEFAULT_USER
        self.delete_result: None | domain.Error = None
        self.get_result: domain.User | None | domain.Error = None
        self.update_result: None | domain.Error = None
        self.where_result: list[domain.User] | domain.Error = []

    def add(self, *, user: domain.User) -> None | domain.Error:
        return self.add_result

    def get_current_user(self) -> domain.User | domain.Error:
        return self.get_current_user_result

    def delete(self, *, user_id: str) -> None | domain.Error:
        return self.delete_result

    def get(self, *, user_id: str) -> domain.User | None | domain.Error:
        return self.get_result

    def update(self, *, user: domain.User) -> None | domain.Error:
        return self.update_result

    def where(self, *, active: bool) -> list[domain.User] | domain.Error:
        return self.where_result
