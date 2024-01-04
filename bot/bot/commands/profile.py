from crescent import Context as crescent_Context

from bot.modules.plugin import Plugin
from bot.utilities import command
from bot.utilities.decorate import decorate
from bot.utilities.embed import embed
from bot.utilities.humanize import humanize

plugin = Plugin()

_ = lambda integer: decorate(humanize(integer))  # noqa: E731


@plugin.include
@command.command("профиль", description="Профиль")
class Command(command.Command):
    async def run(self, context: crescent_Context) -> None:
        emoji = plugin.model.emoji

        user = await plugin.model.database.fetch_or_insert_user_by_id(
            str(context.user.id)
        )

        await context.respond(
            embeds=embed(
                "profile",
                title="profile",
                description="\n".join(
                    [
                        f"{emoji.banana} Бананы: {_(user.banana)}",
                        f"{emoji.monkey} Обезьяны: {_(user.monkey)}",
                        f"{emoji.coin} Монеты: {_(user.coin)}",
                        f"{emoji.diamond} Алмазы: {_(user.diamond)}",
                        f"{emoji.netherite} Незерит: {_(user.netherite)}",
                    ]
                ),
            )
        )
