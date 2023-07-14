import crescent

from pudgeland.locales.plugins import locale
from pudgeland.plugins import server
from pudgeland.utilities.plugins import plugins
from pudgeland.components.plugins.server import status

plugin = plugins.Plugin()


@server.group.child
@plugin.include
@crescent.command(
    name=locale.LocaleBuilder(
        "status",
        russian="статус",
        ukrainian="статус",
    ),
    description=locale.LocaleBuilder(
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
