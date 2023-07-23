import traceback

import crescent
import hikari

from bot.locale import locales


class Client(crescent.Client):
    async def on_crescent_command_error(
        self, exception: Exception, context: crescent.Context, was_handled: bool
    ) -> None:
        if was_handled:
            return

        locale = context.locale

        exc_class = exception.__class__
        exc_traceback = exception.__traceback__

        title = locales.of(
            locale,
            locale_builder=locales.LocaleBuilder(
                "Exception",
                ru="Исключение",
                uk="Виняток",
            ),
        )
        description = f"`{exception}`"

        embed = hikari.Embed(title=title, description=description)

        # Respond to an interaction.
        # This function can be used multiple times for one interaction
        await context.respond(embed=embed)

        # Print exception up to 'limit' stack trace entries from 'tb' to 'file'.
        traceback.print_exception(exc_class, value=exception, tb=exc_traceback)


# MIT License
#
# Copyright (c) 2023 pudgeland
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
