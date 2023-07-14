import crescent

from pudgeland.locales.plugins import locale
from pudgeland.plugins import server
from pudgeland.utilities.plugins import plugins
from pudgeland.components.plugins.server import query

plugin = plugins.Plugin()


@server.group.child
@plugin.include
@crescent.command(
    name=locale.LocaleBuilder(
        "query",
        russian="запрос",
        ukrainian="запит",
    ),
    description=locale.LocaleBuilder(
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
        await query.Component(plugin).callback(context)
