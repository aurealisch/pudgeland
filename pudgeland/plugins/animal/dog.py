import crescent

from pudgeland.plugins import animal
from pudgeland.locales.plugins import locale
from pudgeland.utilities.plugins import plugins
from pudgeland.components.plugins.animal import dog

plugin = plugins.Plugin()


@animal.group.child
@plugin.include
@crescent.command(
    name=locale.LocaleBuilder(
        "dog",
        russian="собака",
        ukrainian="пес",
    ),
    description=locale.LocaleBuilder(
        "Image of a dog",
        russian="Изображение собаки",
        ukrainian="Зображення собаки",
    ),
)
class Dog:
    # noinspection PyMethodMayBeStatic
    async def callback(self, context: crescent.Context) -> None:
        await dog.Component(plugin).callback(context)
