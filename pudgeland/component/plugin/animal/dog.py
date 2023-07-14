import crescent
import hikari
import woofy

from pudgeland.component import components


class Component(components.Component):
    async def callback(self, context: crescent.Context) -> None:
        await context.respond(
            embed=(
                hikari.Embed(
                    title="Собака",
                    description="Изображение собаки",
                )
                .set_author(name=context.user.username, icon=context.user.avatar_url)
                .set_image(woofy.Client().images.search()[0].url)
            )
        )
