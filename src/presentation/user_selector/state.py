import dataclasses

from src import domain

__all__ = ("UserSelectorState",)


@dataclasses.dataclass(frozen=True, kw_only=True)
class UserSelectorState:
    users: tuple[domain.User, ...] | domain.Unspecified = domain.Unspecified()
    selected_category: domain.User | domain.Unspecified = domain.Unspecified()
    error: domain.Error | None = None
