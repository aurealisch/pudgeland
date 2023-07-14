import crescent
import hikari

from pudgeland.components import components


class Component(components.Component):
    async def callback(self, context: crescent.Context) -> None:
        user = await self.plugin.model.database.users.find(id=str(context.user.id))

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
