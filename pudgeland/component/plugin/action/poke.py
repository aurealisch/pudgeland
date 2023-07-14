import crescent
import hikari
import collei

from pudgeland.component import components


class Component(components.Component):
    async def callback(self, context: crescent.Context) -> None:
        await context.respond(
            embed=(
                hikari.Embed(
                    title="Тыкнуть",
                    description=f"<@{context.user.id}> тыкнул(а) <@{self.user.id}>",
                )
                .set_author(name=context.user.username, icon=context.user.avatar_url)
                .set_image(collei.Client().sfw.get(collei.SfwCategory.POKE).url)
            )
        )
