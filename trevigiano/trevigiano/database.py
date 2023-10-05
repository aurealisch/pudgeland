import dataclasses
import typing

import asyncpg


@dataclasses.dataclass
class User:
    id: str
    berry: int
    fox: int
    reputation: int

class Database:
    def __init__(
        self,
        host: typing.Any,
        port: typing.Any,
        user: typing.Any,
        password: typing.Any,
        database: typing.Any,
    ) -> None:
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

        await self._connection.execute(
            """
                CREATE TABLE IF NOT EXISTS users (
                    id         TEXT  PRIMARY KEY,
                    berry      INTEGER NOT NULL DEFAULT 0,
                    fox        INTEGER NOT NULL DEFAULT 0,
                    reputation INTEGER NOT NULL DEFAULT 0
                );
            """
        )

    async def selectOrInsertUser(self, id__: int) -> User:
        await self.reconnect()

        record = await self._connection.fetchrow(
            """
                SELECT users.id,
                       users.berry,
                       users.fox,
                       users.reputation
                  FROM users
                 WHERE users.id = $1;
            """,
            id__,
        )

        if type(record) is not asyncpg.Record:
            await self._connection.execute(
                """
                    INSERT INTO users (id)
                    VALUES ($1);
                """,
                id__,
            )

            return await self.selectOrInsert(id__)

        return User(**record)

    async def selectLeaders(
        self,
        field: typing.Literal[
            "berry",
            "fox",
            "reputation",
        ],
    ) -> list[User]:
        await self.reconnect()

        records = await self._connection.fetch(
            f"""
                  SELECT "users"."id",
                         "users"."berry",
                         "users"."fox",
                         "users"."reputation"
                    FROM "users"
                ORDER BY "users"."{field}" DESC
                   LIMIT 6;
            """
        )

        return list(map(lambda record: User(**record), records))

    async def increase(
        self,
        id__: str,
        key: typing.Literal[
            "berry",
            "fox",
            "reputation",
        ],
        value: int
    ) -> None:
        await self.reconnect()

        await self._connection.execute(
            f"""
                UPDATE "users"
                   SET "{key}" = "{key}" + {value}
                 WHERE "users"."id" = $1;
            """,
            id__,
        )

    async def decrease(
        self,
        id__: str,
        key: typing.Literal[
            "berry",
            "fox",
            "reputation",
        ],
        value: int
    ) -> None:
        await self.reconnect()

        await self._connection.execute(
            f"""
                UPDATE "users"
                   SET "{key}" = "{key}" - {value}
                 WHERE "users"."id" = $1;
            """,
            id__,
        )
