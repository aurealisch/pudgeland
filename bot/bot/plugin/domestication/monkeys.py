import datetime

import crescent
import flare
import hikari

from bot import cmd, code, embed, emoji, err, handle, humanize, plugins

plugin = plugins.Plugin()

period = datetime.timedelta(seconds=2, milliseconds=500)

group = crescent.Group("приручение", description="Приручение")


@plugin.include
@cmd.cmd("обезьяны", desc="Приручение обезьяны", period=period, group=group)
class Command(cmd.Command):

    async def cb(self, ctx: crescent.Context) -> None:
        db = plugin.model.db
        config = plugin.model.config

        ratio = config.get("plugins").get("ratio").get("tame")

        id_ = str(ctx.user.id)

        user = await db.upsert(id_)

        berryQuantity = round(user.fox * ratio)

        style = hikari.ButtonStyle.SECONDARY

        title = f"{emoji.Emoji.MONKEY} Приручение обезьяны"

        @flare.button(label="ОК", emoji=emoji.Emoji.OK, style=style)
        async def ok(msgCtx: flare.MessageContext) -> None:
            await msgCtx.defer()
            await msg.delete()

            try:
                if user.berry < berryQuantity:
                    raise err.Error("Недостаточно ягод")

                await db.inc(id_, "fox", 1)
                await db.dec(id_, "berry", berryQuantity)

                desc = code.code("\n".join([
                    f"+1 обезьяна (Всего: {humanize.humanize(user.fox + 1)})",
                    f"-{humanize.humanize(berryQuantity)} бананов (Всего: {humanize.humanize(user.berry - berryQuantity)})",
                ]))

                await msgCtx.respond(
                    embed=embed.embed("monkeys", title=title, desc=desc))
            except Exception as exception:
                await handle.handle(msgCtx, exception=exception)

        @flare.button(label="Отменить", emoji=emoji.Emoji.CANCEL, style=style)
        async def cancel(msgCtx: flare.MessageContext) -> None:
            flags = hikari.MessageFlag.EPHEMERAL

            await msgCtx.defer(flags=flags)
            await msg.delete()

            desc = "Отменено"

            await msgCtx.respond(flags=flags,
                                 embed=embed.embed("monkeys",
                                                   title=title,
                                                   desc=desc))

        comp = await flare.Row(ok(), cancel())

        desc = code.code(
            f"Стоимость: {humanize.humanize(berryQuantity)} бананов")

        msg = await ctx.respond(ephemeral=True,
                                component=comp,
                                embed=embed.embed("monkeys",
                                                  title=title,
                                                  desc=desc))
