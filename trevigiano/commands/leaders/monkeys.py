from trevigiano import plugins

from .constants import groups, periods

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts


@plugin.include
@commands.command("обезьян",
                  description="Лидеры обезьян",
                  period=periods.period,
                  group=groups.group)
class Command(commands.Command):

    async def call(self, context: contexts.Context) -> None:
        """Description"""
        emoji = context.emoji

        users = await plugin.model.database.selectLeaders("fox")

        emojis = {
            1: emoji.Emoji.first,
            2: emoji.Emoji.second,
            3: emoji.Emoji.third
        }

        title = f"{emoji.Emoji.monkey} Лидеры обезьян"

        description = "\n".join([
            f"{emojis[position]} **#{position}** <@{user.id}> {context.decorate.decorate(context.humanize.humanize(user.fox))}"
            for position, user in enumerate(users, start=1)
        ])

        await context.respond(embed=context.embed.embed(
            "monkeys", title=title, description=description))
