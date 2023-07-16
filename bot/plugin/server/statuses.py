import crescent

from bot.plugin import plugins, server
from bot.plugin.locale import locales
from bot.plugin.middleware.server import statuses

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
        await statuses.Middleware(plugin).callback(context)
