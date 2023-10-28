from trevigiano import plugins

from .constants import groups, periods

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts


@plugin.include
@commands.command("монет",
                  description="Лидеры монет",
                  period=periods.period,
                  group=groups.group)
class Command(commands.Command):

    async def call(self, context: contexts.Context) -> None:
        """Description"""
        emoji = context.emoji

        users = await plugin.model.database.selectLeaders("coin")

        emojis = {
            1: emoji.Emoji.first,
            2: emoji.Emoji.second,
            3: emoji.Emoji.third
        }

        title = f"{emoji.Emoji.coin} Лидеры монет"

        description = "\n".join([
            f"{emojis[position]} **#{position}** <@{user.id}> {context.decorate.decorate(context.humanize.humanize(user.coin))}"
            for position, user in enumerate(users, start=1)
        ])

        await context.respond(embed=context.embed.embed(
            "coins", title=title, description=description))
