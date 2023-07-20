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
import crescent
import mcstatus

from bot.plugin import _plugins
from bot.plugin.locale import locales
from bot.plugin.server import _groups
from bot.utility.embed import embeds

plugin = _plugins.Plugin()


@_groups.group.child
@plugin.include
@crescent.command(
    name=locales.LocaleBuilder(
        "status",
        russian="статус",
        ukrainian="статус",
    ),
    description=locales.LocaleBuilder(
        """\
            Checks the status of a Minecraft Java Edition server
            via the status protocol.
        """,
        russian="""\
            Проверяет статус сервера Minecraft Java Edition
            с помощью протокола статуса.
        """,
        ukrainian="""\
            Перевіряє статус сервера Minecraft Java Edition
            за допомогою протоколу статуса.
        """,
    ),
)
class Status:
    # noinspection PyMethodMayBeStatic
    async def callback(self, context: crescent.Context) -> None:
        """
        Parameters
        ----------
        context : crescent.Context
        """
        java_status_response = mcstatus.JavaServer(
            plugin.model.configuration.java_server_host,
            port=plugin.model.configuration.java_server_port,
        ).status()

        java_status_players = java_status_response.players
        java_status_version = java_status_response.version

        await context.respond(
            embed=(
                embeds.embed(
                    title="Статус",
                    description="""\
                        Проверяет статус сервера Minecraft Java Edition
                        с помощью протокола статуса.
                    """,
                    color="default",
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
