import crescent
import hikari
import mcstatus

from pudgeland.common import env
from pudgeland.plugins import server

from ..modules import locales
from ..utilities import plugins

plugin = plugins.Plugin()


@server.group.child
@plugin.include
@crescent.command(
    name=locales.LocaleBuilder(
        "query",
        russian="запрос",
        ukrainian="запит",
    ),
    description=locales.LocaleBuilder(
        "Checks the status of a Minecraft Java Edition server via the query protocol.",
        russian="Проверяет статус сервера Minecraft Java Edition с помощью протокола запроса.",  # noqa: E501
        ukrainian="Перевіряє статус сервера Minecraft Java Edition за допомогою протоколу запиту.",  # noqa: E501
    ),
)
class Query:
    # noinspection PyMethodMayBeStatic
    async def callback(self, context: crescent.Context) -> None:
        java_server = mcstatus.JavaServer(
            env.java_server_host,
            port=env.java_server_port,
        )
        query_response = java_server.query()

        # Players
        players = query_response.players

        online = players.online
        max = players.max
        names = players.names

        # Software
        software = query_response.software

        brand = software.brand
        plugins = software.plugins
        version = software.version

        # fmt: off
        embed = (
            hikari.Embed(
                title="Запрос",
            )
            .add_field(
                "Игроки",
                value=f"""\
                    Онлайн: *{online}*
                    Максимум: *{max}*
                    Имена: ||{
                        ", ".join([
                            f"`{name}`"

                            for name in names
                        ])
                    }||
                """
            )
            .add_field(
                "Программное обеспечение",
                value=f"""\
                    Марка: *{brand}*
                    Плагины: ||{
                        ", ".join([
                            f"`{plugin}`"

                            for plugin in plugins
                        ])
                    }||
                    Версия: *{version}*
                """
            )
        )
        # fmt: on

        await context.respond(embed=embed)
