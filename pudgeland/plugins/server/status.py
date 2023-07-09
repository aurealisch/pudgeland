import crescent

from pudgeland.plugins.server import group

from ..modules import locales

plugin = crescent.Plugin()


@group.child
@plugin.include
@crescent.command(
    name=locales.LocaleBuilder(
        "status",
        russian="статус",
        ukrainian="статус",
    ),
    description=locales.LocaleBuilder(
        "Status",
        russian="Статус",
        ukrainian="Статус",
    ),
)
class Status:
    async def callback(self, context: crescent.Context) -> None:
        await context.respond("Hello, world!")
