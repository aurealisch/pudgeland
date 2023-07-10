import crescent
import hikari
import mcstatus

from pudgeland.common import environ
from pudgeland.plugins import server

from ..modules import locales

plugin = crescent.Plugin()


@server.group.child
@plugin.include
@crescent.command(
    name=locales.LocaleBuilder(
        "status",
        russian="статус",
        ukrainian="статус",
    ),
    description=locales.LocaleBuilder(
        "Status",
        russian="Статус",
        ukrainian="Статус",
    ),
)
class Status:
    # noinspection PyMethodMayBeStatic
    async def callback(self, context: crescent.Context) -> None:
        java_server = mcstatus.JavaServer(
            environ.JAVA_SERVER_HOST,
            port=environ.JAVA_SERVER_PORT,
        )
        status = java_server.status()

        latency = status.latency

        players = status.players

        online = players.online
        max = players.max
        sample = players.sample

        version = status.version

        name = version.name
        protocol = version.protocol

        # fmt: off
        embed = hikari.Embed(
            title="Статус",
            description=f"""\
                Задержка: *{latency}*

                Игроки: *{online}*/*{max}* (||Образец: {
                    ", ".join([f"`{player.name}`" for player in sample])
                }||)

                Версия: *{name}* (||Протокол: `{protocol}`||)
            """
        )
        # fmt: on

        await context.respond(embed=embed)
