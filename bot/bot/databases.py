import dataclasses
import typing

import asyncpg


@dataclasses.dataclass
class User:
    id: typing.Optional[str] = None
    berry: typing.Optional[int] = None
    fox: typing.Optional[int] = None
    coin: typing.Optional[int] = None
    netheriteScrap: typing.Optional[int] = None
    diamond: typing.Optional[int] = None


Identifier = str
Column = typing.Literal["berry", "fox", "coin", "netheriteScrap", "diamond"]
Value = int


class Database:

    def __init__(self, host: typing.Any, port: typing.Any, user: typing.Any,
                 password: typing.Any, database: typing.Any) -> None:
        """Description"""
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password
        self.__database = database

    async def connect(self) -> None:
        """Description"""
        self._connection: asyncpg.Connection = await asyncpg.connect(
            host=self.__host,
            port=self.__port,
            user=self.__user,
            password=self.__password,
            database=self.__database)

    async def close(self) -> None:
        """Description"""
        await self._connection.close()

    async def reconnect(self) -> None:
        """Description"""
        if self._connection.is_closed:
            await self.connect()

    async def upsert(self, identifier: Identifier) -> User:
        """Description"""
        await self.reconnect()

        query = """
            SELECT "users"."berry",
                   "users"."fox",
                   "users"."coin",
                   "users"."netheriteScrap",
                   "users"."diamond"
              FROM "users"
             WHERE "users"."id" = $1;
        """

        record = await self._connection.fetchrow(query, identifier)

        if isinstance(record, asyncpg.Record):
            return User(**record)

        query = """
            INSERT INTO users ("id")
            VALUES ($1);
        """

        await self._connection.execute(query, identifier)

        return await self.upsert(identifier)

    async def selectLeaders(self, column: Column) -> typing.List[User]:
        """Description"""
        await self.reconnect()

        query = f"""
              SELECT "users"."id",
                     "users"."{column}"
                FROM "users"
            ORDER BY "users"."{column}" DESC
               LIMIT 3;
        """

        records = await self._connection.fetch(query)

        return list(map(lambda record: User(**record), records))

    async def increment(self, identifier: Identifier, column: Column,
                        value: Value) -> None:
        """Description"""
        await self.reconnect()

        query = f"""
            UPDATE "users"
               SET "{column}" = "{column}" + {value}
             WHERE "users"."id" = $1;
        """

        await self._connection.execute(query, identifier)

    async def decrement(self, identifier: Identifier, column: Column,
                        value: Value) -> None:
        """Description"""
        await self.reconnect()

        query = f"""
            UPDATE "users"
               SET "{column}" = "{column}" - {value}
             WHERE "users"."id" = $1;
        """

        await self._connection.execute(query, identifier)
