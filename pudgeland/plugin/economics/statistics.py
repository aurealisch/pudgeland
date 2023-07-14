import crescent

from pudgeland.plugin import economics
from pudgeland.locale.plugin import locales
from pudgeland.utility.plugin import plugins
from pudgeland.component.plugin.economics import statistics

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
        await statistics.Component(plugin).callback(context)
