from typing import Any, Final

from pydantic import Field
from pydantic_settings import BaseSettings

print("initialized from this")


class C(BaseSettings):

    url: str = Field(default="http://wsere", alias="URL")

    # def __init__(self) -> None:
    #     print("C initialzied")
    print("initailized", url)

    async def set_up(self) -> None:
        print("set up", self.url)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields from .env to avoid validation errors


c: Final[C] = C()

print("initialize 12321321d")
