# MIT License
#
# Copyright (c) 2023 elaresai
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
from __future__ import annotations

import typing
import traceback

__all__: typing.Sequence[str] = ("Client",)

import crescent

from bot.utility.embed import embeds


class Client(crescent.Client):
    async def on_crescent_command_error(
        self, exc: Exception, ctx: crescent.Context, was_handled: bool
    ) -> None:
        if not was_handled:
            exc_class = exc.__class__
            exc_class_name = exc_class.__name__
            exc_traceback = exc.__traceback__

            await ctx.respond(
                embed=embeds.embed(
                    title="Исключение",
                    description=f"`{exc_class_name}: {exc}`",
                    color="exception",
                )
            )

            traceback.print_exception(exc_class, value=exc, tb=exc_traceback)
