import crescent
import hikari
import mcstatus

from pudgeland.common import config
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
    async def callback(self, context: crescent.Context) -> None:
        java_server = mcstatus.JavaServer(
            config.java_server_host,
            port=config.java_server_port,
        )
        status = java_server.status()

        # Players
        players = status.players

        online = players.online
        max = players.max
        sample = players.sample

        # Version
        version = status.version

        name = version.name
        protocol = version.protocol

        # fmt: off
        embed = (
            hikari.Embed()
            .add_field(
                "Игроки",
                value=f"""\
                    Онлайн: `{online}` (||{
                        ', '.join([
                            f"`{player.name}`"

                            for player in sample
                        ])
                    }||)
                    Максимум: `{max}`
                """,
            )
            .add_field(
                "Версия",
                value=f"""\
                    Имя: `{name}`
                    Протокол: `{protocol}`
                """,
            )
        )
        # fmt: on

        await context.respond(embed=embed)
