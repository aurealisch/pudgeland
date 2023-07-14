import crescent
import hikari

from pudgeland.plugin import economics
from pudgeland.locale import locales

from ..utility import plugins

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
        user = await plugin.model.database.users.find(id=str(context.user.id))

        await context.respond(
            embed=(
                hikari.Embed(
                    title="Статистика",
                    description=f"""\
                        :banana: Бананы: *{user.banana}*
                        :monkey: Обезьяны: *{user.monkey}*
                    """,
                )
            )
        )
