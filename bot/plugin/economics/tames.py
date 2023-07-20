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
import random

import crescent

from bot.plugin import _plugins
from bot.plugin._locale import _locales
from bot.plugin.economics import _groups
from bot.utility.embed import embeds

plugin = _plugins.Plugin()


@_groups.group.child
@plugin.include
@crescent.command(
    name=_locales.LocaleBuilder(
        "tame",
        russian="приручать",
        ukrainian="приручати",
    ),
    description=_locales.LocaleBuilder(
        "Tame",
        russian="Приручать",
        ukrainian="Приручати",
    ),
)
class Tame:
    # noinspection PyMethodMayBeStatic
    async def callback(self, context: crescent.Context) -> None:
        """
        Parameters
        ----------
        - `context` : `crescent.Context`
        """
        id = str(context.user.id)

        user = await plugin.model.database.find_first(id=id)

        banana = user.banana
        monkey = user.monkey

        fed = (monkey + 1) * 250

        if random.choice(range(1, 10)) != 1:
            await plugin.model.database.update(
                id=id,
                banana=banana - fed,
                monkey=monkey,
            )

            await context.respond(
                embed=embeds.embed(
                    title="Приручать",
                    description=f"""
                        Вы скормили 🍌 `{fed}` бананов
                        и..

                        ❌ Не получилось приручить обезьяну...

                        ```diff\n- {fed} бананов 🍌```

                        :banana: Бананы: `{banana}`
                        :monkey: Обезьяны: `{monkey}`
                    """,
                )
            )

        await plugin.model.database.users.update(
            id=id,
            banana=banana - fed,
            monkey=monkey + 1,
        )

        await context.respond(
            embed=embeds.embed(
                title="Приручать",
                description=f"""
                    Вы скормили 🍌 `{fed}` бананов
                    и..

                    ✅ Получилось приручить обезьяну!!!

                    ```diff\n- {fed} бананов 🍌```
                    ```diff\n+ 1 обезьяна 🐒```

                    :banana: Бананы: `{user.banana}`
                    :monkey: Обезьяны: `{user.monkey}`
                """,
            )
        )
