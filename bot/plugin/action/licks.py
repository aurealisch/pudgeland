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
import collei
import crescent
import hikari

from bot.plugin import _plugins
from bot.plugin.action import _groups
from bot.plugin.locale import locales
from bot.utility.embed import embeds

plugin = _plugins.Plugin()


@_groups.group.child
@plugin.include
@crescent.command(
    name=locales.LocaleBuilder(
        "lick",
        russian="лизнуть",
        ukrainian="лизнути",
    ),
    description=locales.LocaleBuilder(
        "Lick the user",
        russian="Лизнуть пользователя",
        ukrainian="Лизнути користувача",
    ),
)
class Lick:
    user = crescent.option(
        hikari.User,
        name=locales.LocaleBuilder(
            "user",
            russian="пользователь",
            ukrainian="користувач",
        ),
        description=locales.LocaleBuilder(
            "User",
            russian="Пользователь",
            ukrainian="Користувач",
        ),
    )

    # noinspection PyMethodMayBeStatic
    async def callback(self, context: crescent.Context) -> None:
        """
        Parameters
        ----------
        - `context` : `crescent.Context`
        """
        await context.respond(
            embed=(
                embeds.embed(
                    title="Лизнуть",
                    description=f"<@{context.user.id}> лизнул(а) <@{self.user.id}>",
                    color="default",
                )
                .set_author(name=context.user.username, icon=context.user.avatar_url)
                .set_image(collei.Client().sfw.get(collei.SfwCategory.LICK).url)
            )
        )
