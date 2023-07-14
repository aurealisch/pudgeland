import crescent

from pudgeland.locale.plugin import locales
from pudgeland.plugin import server
from pudgeland.utility.plugin import plugins
from pudgeland.component.plugin.server import query

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
        await query.Component(plugin).callback(context)
