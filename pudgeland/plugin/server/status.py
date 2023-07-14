import crescent

from pudgeland.locale.plugin import locales
from pudgeland.plugin import server
from pudgeland.utility.plugin import plugins
from pudgeland.component.plugin.server import status

plugin = plugins.Plugin()


@server.group.child
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
        await status.Component(plugin).callback(context)
