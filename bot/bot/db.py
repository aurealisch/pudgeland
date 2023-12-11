import dataclasses
import typing

import asyncpg

from bot import types


@dataclasses.dataclass
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
        db: typing.Any,
    ) -> None:
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password
        self.__db = db

    async def connect(self) -> None:
        self._conn: asyncpg.Connection = await asyncpg.connect(
            host=self.__host,
            port=self.__port,
            user=self.__user,
            password=self.__password,
            database=self.__db,
        )

        await self._conn.execute(
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
        await self._conn.close()

    async def reconnect(self) -> None:
        if self._conn.is_closed:
            await self.connect()

    async def upsert(self, id_: str) -> User:
        await self.reconnect()

        rec = await self._conn.fetchrow(
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

        if isinstance(rec, asyncpg.Record):
            return User(**rec)

        await self._conn.execute(
            """
                INSERT INTO users ("id")
                VALUES ($1);
            """,
            id_,
        )

        return await self.upsert(id_)

    async def sel(self, col: types.Column) -> typing.List[User]:
        await self.reconnect()

        records = await self._conn.fetch(
            f"""
              SELECT "users"."id",
                     "users"."{col}"
                FROM "users"
            ORDER BY "users"."{col}" DESC
               LIMIT 3;
        """
        )

        return list(map(lambda rec: User(**rec), records))

    async def inc(self, id_: str, col: types.Column, val: int) -> None:
        await self.reconnect()

        await self._conn.execute(
            f"""
                UPDATE "users"
                   SET "{col}" = "{col}" + {val}
                 WHERE "users"."id" = $1;
            """,
            id_,
        )

    async def dec(self, id_: str, col: types.Column, val: int) -> None:
        await self.reconnect()

        await self._conn.execute(
            f"""
                UPDATE "users"
                   SET "{col}" = "{col}" - {val}
                 WHERE "users"."id" = $1;
            """,
            id_,
        )
