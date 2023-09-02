import traceback
import typing

import crescent
import miru

from bot.common.command.utility import embeds


class ErrorHandler:
    @staticmethod
    async def handle(
        error: Exception,
        context: typing.Union[
            crescent.Context,
            miru.context.view.ViewContext,
        ],
    ) -> None:
        value = error
        tb = error.__traceback__

        traceback.print_exception(
            error.__class__,
            value=value,
            tb=tb,
        )

        title = "Ошибка"
        description = f"```{error}```"

        embed = embeds.embed(
            "error",
            context=context,
            title=title,
            description=description,
        )

        await context.respond(embed=embed)
