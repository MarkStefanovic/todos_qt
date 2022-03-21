import pydantic

__all__ = ("Config",)


class Config(pydantic.BaseModel):
    sqlalchemy_url: str

    class Config:
        extra = pydantic.Extra.ignore
        frozen = True
