import collei
import crescent
import hikari

from bot.plugin.middleware import middlewares


class Middleware(middlewares.Middleware):
    async def callback(self, context: crescent.Context) -> None:
        await context.respond(
            embed=(
                hikari.Embed(
                    title="Обнять",
                    description=f"<@{context.user.id}> обнял(а) <@{self.user.id}>",
                )
                .set_author(name=context.user.username, icon=context.user.avatar_url)
                .set_image(collei.Client().sfw.get(collei.SfwCategory.HUG).url)
            )
        )
