import crescent

from pudgeland.plugins import voice

from ..modules import locales

plugin = crescent.Plugin()


@voice.group.child
@plugin.include
@crescent.command(
    name=locales.LocaleBuilder(
        "create",
        russian="создать",
        ukrainian="утворити",
    ),
    description=locales.LocaleBuilder(
        "Create",
        russian="Создать",
        ukrainian="Утворити",
    ),
)
class Create:
    async def callback(self, context: crescent.Context) -> None:
        await context.respond("Hello, world!")
