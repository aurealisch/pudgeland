import datetime

import crescent
import flare
import hikari

from bot import cmd, code, embed, emoji, err, handle, humanize, plugins

plugin = plugins.Plugin()

period = datetime.timedelta(seconds=2, milliseconds=500)


@plugin.include
@cmd.cmd("приручение", desc="Приручение", period=period)
class Command(cmd.Command):
    async def cb(self, ctx: crescent.Context) -> None:
        db = plugin.model.db
        config = plugin.model.config

        ratio = config.get("domesticationRatio")

        id_ = str(ctx.user.id)

        user = await db.upsert(id_)

        bananaQuantity = round(user.monkey * ratio)

        style = hikari.ButtonStyle.SECONDARY

        @flare.button(label="ОК", emoji=emoji.Emoji.OK, style=style)
        async def ok(msgCtx: flare.MessageContext) -> None:
            await msgCtx.defer()
            await msg.delete()

            try:
                if user.banana < bananaQuantity:
                    raise err.Error("Недостаточно бананов")

                await db.inc(id_, "monkey", 1)
                await db.dec(id_, "banana", bananaQuantity)

                desc = code.code(
                    "\n".join(
                        [
                            f"+1 обезьяна (Всего: {humanize.humanize(user.monkey + 1)})",
                            f"-{humanize.humanize(bananaQuantity)} бананов (Всего: {humanize.humanize(user.banana - bananaQuantity)})",
                        ]
                    )
                )

                await msgCtx.respond(
                    embeds=embed.embed("monkey", title="domestication", desc=desc)
                )
            except Exception as exception:
                await handle.handle(msgCtx, exception=exception)

        @flare.button(label="Отменить", emoji=emoji.Emoji.CANCEL, style=style)
        async def cancel(msgCtx: flare.MessageContext) -> None:
            flags = hikari.MessageFlag.EPHEMERAL

            await msgCtx.defer(flags=flags)
            await msg.delete()

            desc = "Отменено"

            await msgCtx.respond(
                flags=flags, embeds=embed.embed("monkey", title="domestication", desc=desc)
            )

        comp = await flare.Row(ok(), cancel())

        desc = code.code(f"Стоимость: {humanize.humanize(bananaQuantity)} бананов")

        msg = await ctx.respond(
            ephemeral=True,
            component=comp,
            embeds=embed.embed("monkey", title="domestication", desc=desc),
        )
