import dataclasses
import typing

import requests


@dataclasses.dataclass
class User:
    berry: int
    fox: int

    id: int | None = None


Field = typing.Literal['id', 'berry', 'fox']


class Database:

    def __init__(self, authorization: str) -> None:
        self.__authorization = authorization
        self.__url = "https://panoramic-copper-production.up.railway.app"
        self.__headers = {
            "authorization": self.__authorization,
        }

    async def upsert(self, id_: int) -> User:
        json = (requests.get(f"{self.__url}/users/{id_}",
                             headers=self.__headers)).json()

        return User(**json)

    async def selectLeaders(self, field: Field) -> list[User]:
        json = (requests.get(f"{self.__url}/leaders/{field}",
                             headers=self.__headers)).json()

        return list(map(lambda json: User(**json), json))

    async def increment(self, id_: str, field: Field, by: int) -> None:
        requests.get(f"{self.__url}/users/{id_}/increment/{field}/{by}",
                     headers=self.__headers)

    async def decrement(self, id_: str, field: Field, by: int) -> None:
        requests.get(f"{self.__url}/users/{id_}/decrement/{field}/{by}",
                     headers=self.__headers)
