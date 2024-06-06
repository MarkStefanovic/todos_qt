import dataclasses

from src import domain

__all__ = ("UserService",)


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class UserService(domain.UserService):
    add_result: None | domain.Error = None
    get_current_user_result: domain.User | domain.Error = domain.DEFAULT_USER
    delete_result: None | domain.Error = None
    get_result: domain.User | None | domain.Error = None
    update_result: None | domain.Error = None
    where_result: tuple[domain.User, ...] | domain.Error = ()

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
        if isinstance(self.where_result, domain.Error):
            return self.where_result

        return list(self.where_result)


if __name__ == "__main__":
    svc = UserService()
    print(svc.get(user_id="12345"))
