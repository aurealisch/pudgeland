import typing
from dataclasses import dataclass as dataclasses_dataclass

import asyncpg

Column = typing.Literal["banana", "monkey", "coin", "netherite", "diamond"]


@dataclasses_dataclass
class User:
    id: str = None
    banana: int = None
    monkey: int = None
    coin: int = None
    diamond: int = None
    netherite: int = None


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

        await self._connection.execute(
            """
                CREATE TABLE IF NOT EXISTS "users" (
                    "id" TEXT PRIMARY KEY,
                    "banana" INTEGER DEFAULT 0,
                    "monkey" INTEGER DEFAULT 1,
                    "coin" INTEGER DEFAULT 0,
                    "diamond" INTEGER DEFAULT 0,
                    "netherite" INTEGER DEFAULT 0
                );
            """
        )

    async def close(self) -> None:
        await self._connection.close()

    async def reconnect(self) -> None:
        if self._connection.is_closed:
            await self.connect()

    async def fetch_or_insert_user_by_id(self, id_: str) -> User:
        await self.reconnect()

        record = await self._connection.fetchrow(
            """
                SELECT "users"."banana",
                       "users"."monkey",
                       "users"."coin",
                       "users"."diamond",
                       "users"."netherite"
                  FROM "users"
                 WHERE "users"."id" = $1;
            """,
            id_,
        )

        if isinstance(record, asyncpg.Record):
            return User(**record)

        await self._connection.execute(
            """
                INSERT INTO users ("id")
                VALUES ($1);
            """,
            id_,
        )

        return await self.fetch_or_insert_user_by_id(id_)

    async def select_descending_users_by_column(self, column: Column) -> list[User]:
        await self.reconnect()

        records = await self._connection.fetch(
            f"""
              SELECT "users"."id",
                     "users"."{column}"
                FROM "users"
            ORDER BY "users"."{column}" DESC
               LIMIT 3;
        """
        )

        return list(map(lambda rec: User(**rec), records))

    async def increase_user_column_value_by_id(
        self, id_: str, column: Column, value: int
    ) -> None:
        await self.reconnect()

        await self._connection.execute(
            f"""
                UPDATE "users"
                   SET "{column}" = "{column}" + {value}
                 WHERE "users"."id" = $1;
            """,
            id_,
        )

    async def decrease_user_column_value_by_id(
        self, id_: str, column: Column, value: int
    ) -> None:
        await self.reconnect()

        await self._connection.execute(
            f"""
                UPDATE "users"
                   SET "{column}" = "{column}" - {value}
                 WHERE "users"."id" = $1;
            """,
            id_,
        )
