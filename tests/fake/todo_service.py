import dataclasses

from src import domain

__all__ = ("TodoService",)


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class TodoService(domain.TodoService):
    add_result: None | domain.Error = None
    delete_result: None | domain.Error = None
    get_result: domain.Todo | None | domain.Error = domain.DEFAULT_TODO
    get_by_template_id_and_user_id_result: None | domain.Error = None
    mark_as_completed_result: None | domain.Error = None
    where_result: tuple[domain.Todo, ...] | domain.Error = (domain.DEFAULT_TODO,)
    mark_incomplete_result: None | domain.Error = None
    update_result: None | domain.Error = None

    def add(self, *, todo: domain.Todo) -> None | domain.Error:
        return self.add_result

    def delete(self, *, todo_id: str) -> None | domain.Error:
        return self.delete_result

    def get(self, *, todo_id: str) -> domain.Todo | None | domain.Error:
        return self.get_result

    def get_by_template_id_and_user_id(
        self,
        *,
        template_todo_id: str,
        user_id: str,
    ) -> domain.Todo | None | domain.Error:
        return self.get_by_template_id_and_user_id_result

    def mark_complete(
        self,
        *,
        todo_id: str,
        user: domain.User | None,
    ) -> None | domain.Error:
        return self.mark_as_completed_result

    def where(
        self,
        *,
        due_filter: bool | domain.Unspecified,
        description_like: str | domain.Unspecified,
        category_id_filter: str | domain.Unspecified,
        user_id_filter: str | domain.Unspecified,
    ) -> list[domain.Todo] | domain.Error:
        if isinstance(self.where_result, domain.Error):
            return self.where_result

        return list(self.where_result)

    def mark_incomplete(self, *, todo_id: str) -> None | domain.Error:
        return self.mark_incomplete_result

    def update(self, *, todo: domain.Todo) -> None | domain.Error:
        return self.update_result
