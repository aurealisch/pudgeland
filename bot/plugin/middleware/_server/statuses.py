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
import mcstatus

from bot.plugin.middleware import middlewares
from bot.utility.embed import embeds


class Middleware(middlewares.Middleware):
    async def callback(self, context: crescent.Context) -> None:
        """
        Parameters
        ----------
        - `context` : `crescent.Context`
        """
        java_status_response = mcstatus.JavaServer(
            self.plugin.model.environment.java_server_host,
            port=self.plugin.model.environment.java_server_port,
        ).status()

        java_status_players = java_status_response.players
        java_status_version = java_status_response.version

        await context.respond(
            embed=(
                embeds.embed(
                    mode="default",
                    title="Статус",
                    description="""\
                        Проверяет статус сервера Minecraft Java Edition
                        с помощью протокола статуса.
                    """,
                )
                .add_field(
                    "Игроки",
                    value=f"""\
                        Онлайн: *{java_status_players.online}*
                        Максимум: *{java_status_players.max}*
                        Образец: {
                            ", ".join(
                                [
                                    f"*{java_status_player.name}"
                                    f"(||{java_status_player.id}||)"

                                    for java_status_player in java_status_players.sample
                                ]
                            )
                        }
                    """,
                )
                .add_field(
                    "Версия",
                    value=f"""\
                        Имя: *{java_status_version.name}*
                        Протокол: *{java_status_version.protocol}*
                    """,
                )
            )
        )
