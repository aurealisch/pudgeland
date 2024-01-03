from crescent import Context as crescent_Context

from bot.modules.plugin import Plugin
from bot.utilities import command
from bot.utilities.decorate import decorate as d
from bot.utilities.embed import embed
from bot.utilities.emoji import Emoji
from bot.utilities.humanize import humanize as h

plugin = Plugin()


@plugin.include
@command.command("профиль", description="Профиль")
class Command(command.Command):
    async def run(self, ctx: crescent_Context) -> None:
        user = await plugin.model.database.fetch_or_insert_user_by_id(str(ctx.user.id))

        await ctx.respond(
            embeds=embed(
                "profile",
                title="profile",
                description="\n".join(
                    [
                        f"{Emoji.banana} Бананы: {d(h(user.banana))}",
                        f"{Emoji.monkey} Обезьяны: {d(h(user.monkey))}",
                        f"{Emoji.coin} Монеты: {d(h(user.coin))}",
                        f"{Emoji.diamond} Алмазы: {d(h(user.diamond))}",
                        f"{Emoji.netherite} Незерит: {d(h(user.netherite))}",
                    ]
                ),
            )
        )
