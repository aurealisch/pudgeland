import dataclasses
import typing

import asyncpg


@dataclasses.dataclass
class User:
    id: str
    berry: int
    fox: int
    reputation: int


Field = typing.Literal[
    'berry',
    'fox',
    'reputation',
]


class Database:

    def __init__(self, host: typing.Any, port: typing.Any, user: typing.Any,
                 password: typing.Any, database: typing.Any) -> None:
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password
        self.__database = database

    async def connect(self) -> None:
        self._connection: asyncpg.Connection = await asyncpg.connect(
            host=self.__host,
            port=self.__port,
            user=self.__user,
            password=self.__password,
            database=self.__database,
        )

    async def close(self) -> None:
        await self._connection.close()

    async def reconnect(self) -> typing.Callable:
        if self._connection.is_closed:
            await self.connect()

    async def createTableIfNotExists(self) -> None:
        await self.reconnect()

        query = """
            CREATE TABLE IF NOT EXISTS "users" (
                "id"         TEXT  PRIMARY KEY,
                "berry"      INTEGER NOT NULL DEFAULT 0,
                "fox"        INTEGER NOT NULL DEFAULT 1,
                "reputation" INTEGER NOT NULL DEFAULT 0
            );
        """

        await self._connection.execute(query)

    async def upsert(self, id_: int) -> User:
        await self.reconnect()

        query = """
            SELECT "users"."id",
                   "users"."berry",
                   "users"."fox",
                   "users"."reputation"
              FROM "users"
             WHERE "users"."id" = $1;
        """

        record = await self._connection.fetchrow(query, id_)

        if isinstance(record, asyncpg.Record):
            return User(**record)

        query = """
            INSERT INTO users ("id")
            VALUES ($1);
        """

        await self._connection.execute(query, id_)

        return await self.upsert(id_)

    async def selectLeaders(self, field: Field) -> list[User]:
        await self.reconnect()

        query = f"""
              SELECT "users"."id",
                     "users"."berry",
                     "users"."fox",
                     "users"."reputation"
                FROM "users"
            ORDER BY "users"."{field}" DESC
               LIMIT 6;
        """

        records = await self._connection.fetch(query)

        return list(map(lambda record: User(**record), records))

    async def increase(self, id_: str, field: Field, value: int) -> None:
        await self.reconnect()

        query = f"""
            UPDATE "users"
               SET "{field}" = "{field}" + {value}
             WHERE "users"."id" = $1;
        """

        await self._connection.execute(query, id_)

    async def decrease(self, id_: str, field: Field, value: int) -> None:
        await self.reconnect()

        query = f"""
            UPDATE "users"
               SET "{field}" = "{field}" - {value}
             WHERE "users"."id" = $1;
        """

        await self._connection.execute(query, id_)
