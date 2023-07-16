import crescent
import hikari
import meowy

from bot.plugin.middleware import middlewares


class Middleware(middlewares.Middleware):
    async def callback(self, context: crescent.Context) -> None:
        await context.respond(
            embed=(
                hikari.Embed(
                    title="Кот",
                    description="Изображение кота",
                )
                .set_author(name=context.user.username, icon=context.user.avatar_url)
                .set_image(meowy.Client().images.search()[0].url)
            )
        )
