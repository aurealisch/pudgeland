import dataclasses
import typing

import requests


@dataclasses.dataclass
class User:
    id: typing.Optional[int] = None

    berry: typing.Optional[int] = None
    fox: typing.Optional[int] = None

    coin: typing.Optional[int] = None

    netheriteScrap: typing.Optional[int] = None
    diamond: typing.Optional[int] = None


Field = typing.Literal['berry', 'fox', 'coin', 'netheriteScrap', 'diamond']


class Database:

    def __init__(self, authorization: str) -> None:
        """Description

        Parameters
        ----------
        authorization : str
            Description
        """
        self.__authorization = authorization
        self.__url = "https://panoramic-copper-production.up.railway.app"
        self.__headers = {
            "authorization": self.__authorization,
        }

    async def upsert(self, id_: int) -> User:
        """Description
        
        Parameters
        ----------
        id_ : int
            Description
        
        Returns
        -------
        User
            Description
        """
        json = (requests.get(f"{self.__url}/users/",
                             headers=self.__headers,
                             params={'id': id_})).json()

        return User(**json)

    async def selectLeaders(self, field: Field) -> list[User]:
        """Description

        Parameters
        ----------
        field : Field
            Description
        
        Returns
        -------
        list[User]
            Description
        """
        json = (requests.get(f"{self.__url}/leaders/{field}/",
                             headers=self.__headers,
                             params={'field': field})).json()

        return list(map(lambda json: User(**json), json))

    async def increment(self, id_: str, field: Field, by: int) -> None:
        """Description
        
        Parameters
        ----------
        id_ : str
            Description
        field : Field
            Description
        by : int
            Description
        """
        requests.get(f"{self.__url}/users/{field}/increment/",
                     headers=self.__headers,
                     params={
                         'id': id_,
                         'by': by
                     })

    async def decrement(self, id_: str, field: Field, by: int) -> None:
        """Description
        
        Parameters
        ----------
        id_ : str
            Description
        field : Field
            Description
        by : int
            Description
        """
        requests.get(f"{self.__url}/users/{field}/decrement/",
                     headers=self.__headers,
                     params={
                         'id': id_,
                         'by': by
                     })
