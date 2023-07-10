import crescent

from pudgeland.plugins import voice

from ..modules import locales

plugin = crescent.Plugin()


@voice.group.child
@plugin.include
@crescent.command(
    name=locales.LocaleBuilder(
        "delete",
        russian="удалить",
        ukrainian="видалити",
    ),
    description=locales.LocaleBuilder(
        "Delete",
        russian="Удалить",
        ukrainian="Видалити",
    ),
)
class Delete:
    # noinspection PyMethodMayBeStatic
    async def callback(self, context: crescent.Context) -> None:
        await context.respond("Hello, world!")
