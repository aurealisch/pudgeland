from trevigiano import plugins

from .constants import groups, periods

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts


@plugin.include
@commands.command("алмазов",
                  description="Лидеры алмазов",
                  period=periods.period,
                  group=groups.group)
class Command(commands.Command):

    async def call(self, context: contexts.Context) -> None:
        """Description

        Parameters
        ----------
        context : contexts.Context
            Description
        """
        emoji = context.emoji

        users = await plugin.model.database.selectLeaders("diamond")

        emojis = {
            1: emoji.Emoji.first,
            2: emoji.Emoji.second,
            3: emoji.Emoji.third
        }

        title = f"{emoji.Emoji.diamond} Лидеры алмазов"

        description = "\n".join([
            f"{emojis[position]} **#{position}** <@{user.id}> {context.decorate.decorate(context.humanize.humanize(user.diamond))}"
            for position, user in enumerate(users, start=1)
        ])

        await context.respond(embed=context.embed.embed(
            "diamonds", title=title, description=description))
