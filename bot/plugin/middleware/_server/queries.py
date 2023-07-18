# MIT License
#
# Copyright (c) 2023 elaresai
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from __future__ import annotations

__all__: typing.Sequence[str] = ("Middleware",)

import typing

import crescent
import hikari
import mcstatus

from bot.plugin.middleware import middlewares


class Middleware(middlewares.Middleware):
    async def callback(self, context: crescent.Context) -> None:
        """
        Parameters
        ----------
        - `context` : `crescent.Context`
        """
        query_response = mcstatus.JavaServer(
            self.plugin.model.environment.java_server_host,
            port=self.plugin.model.environment.java_server_port,
        ).query()

        players = query_response.players
        software = query_response.software

        await context.respond(
            embed=(
                hikari.Embed(
                    title="Запрос",
                    description="""\
                        Проверяет статус сервера Minecraft Java Edition
                        с помощью протокола запроса.
                    """,
                )
                .add_field(
                    "Игроки",
                    value=f"""\
                        Онлайн: *{players.online}*
                        Максимум: *{players.max}*
                        Имена: ||{
                            ", ".join(
                                [
                                    f"`{name}`"

                                    for name in players.names
                                ]
                            )
                        }||
                    """,
                )
                .add_field(
                    "Программное обеспечение",
                    value=f"""\
                        Марка: *{software.brand}*
                        Плагины: ||{
                            ", ".join(
                                [
                                    f"`{plugin}`"

                                    for plugin in software.plugins
                                ]
                            )
                        }||
                        Версия: *{software.version}*
                    """,
                )
            )
        )
