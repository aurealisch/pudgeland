import crescent
import hikari
import mcstatus

from bot.common.environment import environments
from bot.plugin.middleware import middlewares


class Middleware(middlewares.Middleware):
    async def callback(self, context: crescent.Context) -> None:
        query_response = mcstatus.JavaServer(
            environments.java_server_host,
            port=environments.java_server_port,
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
