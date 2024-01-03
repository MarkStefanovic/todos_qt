import uuid

__all__ = ("create_uuid",)


def create_uuid() -> str:
    return uuid.uuid4().hex


if __name__ == "__main__":
    print(create_uuid())
