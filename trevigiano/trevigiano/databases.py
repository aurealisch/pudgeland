import dataclasses
import typing

import requests


@dataclasses.dataclass
class User:
    id: int
    berry: int
    fox: int


Field = typing.Literal['id', 'berry', 'fox']


class Database:

    def __init__(self, uri: str) -> None:
        self.__uri = uri

    async def upsert(self, id_: int) -> User:
        return User(**requests.get(f"{self.__uri}/users/{id_}").json())

    async def selectLeaders(self, field: Field) -> list[User]:
        return list(
            map(lambda json: User(**json),
                requests.get(f"{self.__uri}/leaders/{field}").json()))

    async def increase(self, id_: str, field: Field, by: int) -> None:
        requests.get(f"{self.__uri}/users/{id_}/increment/{field}/{by}")

    async def decrease(self, id_: str, field: Field, by: int) -> None:
        requests.get(f"{self.__uri}/users/{id_}/decrement/{field}/{by}")
