import crescent

from bot.plugin import economics, plugins
from bot.plugin.locale import locales
from bot.plugin.middleware.economics import statistics

plugin = plugins.Plugin()


@economics.group.child
@plugin.include
@crescent.command(
    name=locales.LocaleBuilder(
        "statistics",
        russian="статистика",
        ukrainian="статистика",
    ),
    description=locales.LocaleBuilder(
        "Statistics",
        russian="Статистика",
        ukrainian="Статистика",
    ),
)
class Statistics:
    # noinspection PyMethodMayBeStatic
    async def callback(self, context: crescent.Context) -> None:
        await statistics.Middleware(plugin).callback(context)
