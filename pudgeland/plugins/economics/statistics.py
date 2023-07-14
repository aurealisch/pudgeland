import crescent

from pudgeland.plugins import economics
from pudgeland.locales.plugins import locale
from pudgeland.utilities.plugins import plugins
from pudgeland.components.plugins.economics import statistics

plugin = plugins.Plugin()


@economics.group.child
@plugin.include
@crescent.command(
    name=locale.LocaleBuilder(
        "statistics",
        russian="статистика",
        ukrainian="статистика",
    ),
    description=locale.LocaleBuilder(
        "Statistics",
        russian="Статистика",
        ukrainian="Статистика",
    ),
)
class Statistics:
    # noinspection PyMethodMayBeStatic
    async def callback(self, context: crescent.Context) -> None:
        await statistics.Component(plugin).callback(context)
