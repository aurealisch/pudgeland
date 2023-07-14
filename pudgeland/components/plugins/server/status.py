import crescent
import hikari
import mcstatus

from pudgeland.environments import environment
from pudgeland.components import components


class Component(components.Component):
    async def callback(self, context: crescent.Context) -> None:
        java_status_response = mcstatus.JavaServer(
            environment.java_server_host,
            port=environment.java_server_port,
        ).status()

        java_status_players = java_status_response.players
        java_status_version = java_status_response.version

        await context.respond(
            embed=(
                hikari.Embed(
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
