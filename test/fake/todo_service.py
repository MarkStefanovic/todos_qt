from src import domain

__all__ = ("TodoService",)


class TodoService(domain.TodoService):
    def __init__(self):  # type: ignore
        self.add_result: None | domain.Error = None
        self.delete_result: None | domain.Error = None
        self.get_result: None | domain.Error = None
        self.get_by_template_id_and_user_id_result: None | domain.Error = None
        self.mark_as_completed_result: None | domain.Error = None
        self.where_result: list[domain.Todo] | domain.Error = []
        self.mark_incomplete_result: None | domain.Error = None
        self.update_result: None | domain.Error = None

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
        return self.where_result

    def mark_incomplete(self, *, todo_id: str) -> None | domain.Error:
        return self.mark_incomplete_result

    def update(self, *, todo: domain.Todo) -> None | domain.Error:
        return self.update_result
