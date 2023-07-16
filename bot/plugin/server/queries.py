import crescent

from bot.plugin import plugins, server
from bot.plugin.locale import locales
from bot.plugin.middleware.server import queries

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
        """\
            Checks the status of a Minecraft Java Edition server
            via the query protocol.
        """,
        russian="""\
            Проверяет статус сервера Minecraft Java Edition
            с помощью протокола запроса.
        """,
        ukrainian="""\
            Перевіряє статус сервера Minecraft Java Edition
            за допомогою протоколу запиту.
        """,
    ),
)
class Query:
    # noinspection PyMethodMayBeStatic
    async def callback(self, context: crescent.Context) -> None:
        await queries.Middleware(plugin).callback(context)
